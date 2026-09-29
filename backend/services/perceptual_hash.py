"""Perceptual hash."""
from __future__ import annotations
import json
from pathlib import Path

import imagehash
from PIL import Image

from backend.config import settings
from backend.utils.logger import logger


class PerceptualHashService:
    def __init__(self, known_fakes_db=None):
        self.log = logger.bind(service="perceptual_hash")
        self.db_path = Path(known_fakes_db or settings.known_fakes_db)
        self._known_fakes = []
        self._load_db()

    def compute_phash(self, image_path):
        with Image.open(image_path) as img:
            return str(imagehash.phash(img.convert("RGB"), hash_size=8))

    def find_matches(self, image_path, hamming_threshold=6):
        query = imagehash.hex_to_hash(self.compute_phash(image_path))
        matches = []
        for entry in self._known_fakes:
            try:
                known = imagehash.hex_to_hash(entry["phash"])
                distance = query - known
                if distance <= hamming_threshold:
                    matches.append({
                        "id": entry["id"],
                        "distance": int(distance),
                        "similarity": round(1 - distance / 64.0, 4),
                        "source": entry.get("source", "unknown"),
                    })
            except Exception:
                pass
        matches.sort(key=lambda m: m["distance"])
        return matches

    def duplicate_score(self, image_path, hamming_threshold=6):
        matches = self.find_matches(image_path, hamming_threshold)
        if not matches:
            return 1.0, []
        best = matches[0]
        normalized = min(best["distance"] / max(hamming_threshold, 1), 1.0)
        return round(0.2 + 0.8 * normalized, 3), matches

    def _load_db(self):
        if not self.db_path.exists():
            return
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                self._known_fakes = json.load(f).get("entries", [])
        except Exception:
            pass
