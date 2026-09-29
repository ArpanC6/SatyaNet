"""Bayesian Truth Score Engine."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image

from backend.config import settings
from backend.models.enums import SignalStatus, SignalType, TrustLevel
from backend.models.schemas import ExifMetadata, SignalScore, TruthScoreResult
from backend.services.exif_forensics import ExifForensics
from backend.services.perceptual_hash import PerceptualHashService
from backend.services.satellite_crosscheck import SatelliteCrossCheck
from backend.utils.logger import logger


class TruthScoreEngine:
    def __init__(self, exif_service=None, hash_service=None, satellite_service=None):
        self.log = logger.bind(service="truth_score")
        self.exif = exif_service or ExifForensics()
        self.hasher = hash_service or PerceptualHashService()
        self.satellite = satellite_service or SatelliteCrossCheck()
        self.weights = settings.weights
        total = sum(self.weights.values())
        if abs(total - 1.0) > 1e-6:
            self.weights = {k: v / total for k, v in self.weights.items()}

    def score(self, image_path, claimed_date, claimed_lat=None, claimed_lon=None):
        path = Path(image_path)
        signals = []
        reasons = []
        flags = []

        exif_meta = self.exif.extract(path)
        s_exif, r_exif = self._score_exif(exif_meta)
        signals.append(self._make_signal(SignalType.EXIF_INTEGRITY, s_exif, r_exif))
        reasons.extend(r_exif)

        s_time, r_time = self._score_temporal(exif_meta, claimed_date)
        signals.append(self._make_signal(SignalType.TEMPORAL_PLAUSIBILITY, s_time, r_time))
        reasons.extend(r_time)

        s_sat, r_sat = self._score_satellite(exif_meta, claimed_lat, claimed_lon, claimed_date)
        signals.append(self._make_signal(SignalType.SATELLITE_CONSISTENCY, s_sat, r_sat))
        reasons.extend(r_sat)

        s_dup, r_dup, dup_matches = self._score_duplicate(path)
        signals.append(self._make_signal(SignalType.DUPLICATE_CHECK, s_dup, r_dup))
        reasons.extend(r_dup)
        if dup_matches and dup_matches[0]["distance"] <= 3:
            flags.append("Match: " + dup_matches[0]["source"])

        s_qual, r_qual = self._score_quality(path)
        signals.append(self._make_signal(SignalType.IMAGE_QUALITY, s_qual, r_qual))
        reasons.extend(r_qual)

        trust_score = self._fuse(signals)
        trust_level = TrustLevel.from_score(trust_score)

        if trust_level == TrustLevel.LIKELY_FAKE:
            flags.append("Recommend manual verification before action")
        elif trust_level == TrustLevel.NEEDS_REVIEW:
            flags.append("Partial confidence - corroborate with second source")

        return TruthScoreResult(
            trust_score=round(trust_score, 1),
            trust_level=trust_level,
            signals=signals,
            reasons=reasons,
            flags=flags,
        )

    def _score_exif(self, exif):
        reasons = []
        if not exif.has_exif:
            reasons.append("EXIF metadata stripped - possible screenshot")
            return 0.2, reasons
        score = 0.5
        reasons.append("EXIF metadata present")
        if exif.datetime_original:
            score += 0.2
            reasons.append("Original timestamp present")
        else:
            reasons.append("No original timestamp in EXIF")
        if exif.gps:
            score += 0.2
            reasons.append("GPS present: ({0:.4f}, {1:.4f})".format(exif.gps.latitude, exif.gps.longitude))
        else:
            reasons.append("No GPS coordinates")
        return min(score, 1.0), reasons

    def _score_temporal(self, exif, claimed):
        reasons = []
        if not exif.datetime_original:
            reasons.append("Cannot validate temporal plausibility")
            return 0.4, reasons
        delta = abs((exif.datetime_original - claimed).days)
        if delta <= 1:
            reasons.append("Timestamp matches claim")
            return 1.0, reasons
        if delta <= 7:
            reasons.append("Timestamp within a week")
            return 0.8, reasons
        if delta <= 30:
            reasons.append("Image is " + str(delta) + " days older than claim")
            return 0.5, reasons
        reasons.append("Image is " + str(delta) + " days old - likely recycled")
        return 0.1, reasons

    def _score_satellite(self, exif, lat, lon, claimed):
        lat = lat or (exif.gps.latitude if exif.gps else None)
        lon = lon or (exif.gps.longitude if exif.gps else None)
        if lat is None or lon is None:
            return 0.5, ["No coordinates - satellite cross-check skipped"]
        result = self.satellite.check_consistency(lat, lon, claimed)
        score = result.get("score", 0.5)
        return score, [result.get("reason", "Satellite check")]

    def _score_duplicate(self, path):
        score, matches = self.hasher.duplicate_score(path)
        reasons = []
        if not matches:
            reasons.append("No duplicate matches in known-fake database")
        else:
            best = matches[0]
            reasons.append("Matches known fake: " + best["source"])
        return score, reasons, matches

    def _score_quality(self, path):
        reasons = []
        try:
            with Image.open(path) as img:
                gray = np.array(img.convert("L"), dtype=np.float32)
        except Exception:
            return 0.5, ["Quality check unavailable"]
        contrast = float(gray.std()) / 128.0
        contrast = min(contrast, 1.0)
        if contrast < 0.15:
            reasons.append("Low contrast ({0:.2f})".format(contrast))
            return max(contrast, 0.2), reasons
        reasons.append("Acceptable contrast ({0:.2f})".format(contrast))
        return contrast, reasons

    def _fuse(self, signals):
        total = 0.0
        for s in signals:
            w = self.weights.get(s.signal.value, 0.0)
            total += s.score * w
        return round(total * 100.0, 2)

    def _make_signal(self, signal_type, score, reasons):
        if score >= 0.75:
            status = SignalStatus.PASS
        elif score >= 0.4:
            status = SignalStatus.WARN
        else:
            status = SignalStatus.FAIL
        return SignalScore(
            signal=signal_type,
            score=round(score, 3),
            status=status,
            weight=self.weights.get(signal_type.value, 0.0),
            reason="; ".join(reasons[:2]) if reasons else None,
        )
