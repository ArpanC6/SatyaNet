"""Domain enums."""
from enum import Enum


class TrustLevel(str, Enum):
    VERIFIED = "verified"
    NEEDS_REVIEW = "needs_review"
    LIKELY_FAKE = "likely_fake"

    @classmethod
    def from_score(cls, score):
        if score >= 80:
            return cls.VERIFIED
        if score >= 50:
            return cls.NEEDS_REVIEW
        return cls.LIKELY_FAKE


class SignalType(str, Enum):
    EXIF_INTEGRITY = "exif_integrity"
    TEMPORAL_PLAUSIBILITY = "temporal_plausibility"
    SATELLITE_CONSISTENCY = "satellite_consistency"
    DUPLICATE_CHECK = "duplicate_check"
    IMAGE_QUALITY = "image_quality"


class SignalStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    UNKNOWN = "unknown"


class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"


class VerdictReason(str, Enum):
    EXIF_INTACT = "exif_intact"
    EXIF_STRIPPED = "exif_stripped"
    GPS_PRESENT = "gps_present"
    GPS_MISSING = "gps_missing"
    TIMESTAMP_MATCHES = "timestamp_matches"
    TIMESTAMP_MISMATCH = "timestamp_mismatch"
    SATELLITE_MATCH = "satellite_match"
    SATELLITE_MISMATCH = "satellite_mismatch"
    DUPLICATE_FOUND = "duplicate_found"
    LOW_QUALITY = "low_quality"
    HIGH_QUALITY = "high_quality"


class ReportFormat(str, Enum):
    PDF = "pdf"
    JSON = "json"
