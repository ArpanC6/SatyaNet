"""EXIF forensics."""
from __future__ import annotations
import hashlib
from datetime import datetime
from pathlib import Path

import piexif
from PIL import Image

from backend.models.schemas import ExifMetadata, GeoLocation
from backend.utils.exceptions import ExifExtractionError
from backend.utils.logger import logger


class ExifForensics:
    def __init__(self):
        self.log = logger.bind(service="exif_forensics")

    def extract(self, image_path):
        path = Path(image_path)
        if not path.exists():
            raise ExifExtractionError("File not found: " + str(path))
        with Image.open(path) as img:
            width, height = img.size
            exif_bytes = img.info.get("exif", b"")
        if not exif_bytes:
            return ExifMetadata(has_exif=False, image_width=width, image_height=height)
        try:
            exif_dict = piexif.load(exif_bytes)
        except Exception:
            return ExifMetadata(has_exif=False, image_width=width, image_height=height)
        gps = self._extract_gps(exif_dict)
        dt = self._extract_datetime(exif_dict)
        return ExifMetadata(
            has_exif=True,
            datetime_original=dt,
            gps=gps,
            image_width=width,
            image_height=height,
        )

    def compute_sha256(self, file_path):
        sha = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha.update(chunk)
        return sha.hexdigest()

    def _extract_datetime(self, exif_dict):
        dt_bytes = exif_dict.get("Exif", {}).get(piexif.ExifIFD.DateTimeOriginal)
        if not dt_bytes:
            return None
        try:
            return datetime.strptime(dt_bytes.decode("utf-8", errors="ignore").strip(), "%Y:%m:%d %H:%M:%S")
        except Exception:
            return None

    def _extract_gps(self, exif_dict):
        gps_ifd = exif_dict.get("GPS", {})
        if not gps_ifd:
            return None
        lat = self._gps(gps_ifd.get(piexif.GPSIFD.GPSLatitude), gps_ifd.get(piexif.GPSIFD.GPSLatitudeRef))
        lon = self._gps(gps_ifd.get(piexif.GPSIFD.GPSLongitude), gps_ifd.get(piexif.GPSIFD.GPSLongitudeRef))
        if lat is None or lon is None:
            return None
        return GeoLocation(latitude=lat, longitude=lon)

    def _gps(self, coord, ref):
        if not coord or not ref:
            return None
        try:
            d = coord[0][0] / coord[0][1]
            m = coord[1][0] / coord[1][1]
            s = coord[2][0] / coord[2][1]
            dec = d + m / 60.0 + s / 3600.0
            if ref.decode("utf-8", errors="ignore").upper() in ("S", "W"):
                dec = -dec
            return round(dec, 6)
        except Exception:
            return None
