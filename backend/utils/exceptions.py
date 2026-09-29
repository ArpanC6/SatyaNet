"""Custom exception hierarchy."""
from typing import Any, Dict, Optional


class SatyaNetError(Exception):
    status_code = 500
    error_code = "SATYANET_ERROR"

    def __init__(self, message, *, details=None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self):
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details,
        }


class MediaValidationError(SatyaNetError):
    status_code = 400
    error_code = "MEDIA_VALIDATION_ERROR"


class UnsupportedMediaTypeError(SatyaNetError):
    status_code = 415
    error_code = "UNSUPPORTED_MEDIA_TYPE"


class ExifExtractionError(SatyaNetError):
    status_code = 422
    error_code = "EXIF_EXTRACTION_ERROR"


class CloudinaryUploadError(SatyaNetError):
    status_code = 502
    error_code = "CLOUDINARY_UPLOAD_ERROR"


class SatelliteFetchError(SatyaNetError):
    status_code = 502
    error_code = "SATELLITE_FETCH_ERROR"


class VectorStoreError(SatyaNetError):
    status_code = 502
    error_code = "VECTOR_STORE_ERROR"


class DuplicateEvidenceError(SatyaNetError):
    status_code = 409
    error_code = "DUPLICATE_EVIDENCE_ERROR"


class ReportGenerationError(SatyaNetError):
    status_code = 500
    error_code = "REPORT_GENERATION_ERROR"


class ConfigurationError(SatyaNetError):
    status_code = 500
    error_code = "CONFIGURATION_ERROR"
