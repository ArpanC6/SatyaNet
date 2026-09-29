"""Cloudinary service."""
from __future__ import annotations
import re

import cloudinary
import cloudinary.uploader

from backend.config import settings
from backend.models.schemas import CloudinaryAsset
from backend.utils.exceptions import CloudinaryUploadError
from backend.utils.logger import logger


class CloudinaryService:
    def __init__(self):
        self.log = logger.bind(service="cloudinary")
        self._configured = False
        if settings.cloudinary_cloud_name:
            cloudinary.config(
                cloud_name=settings.cloudinary_cloud_name,
                api_key=settings.cloudinary_api_key,
                api_secret=settings.cloudinary_api_secret,
                secure=True,
            )
            self._configured = True

    def upload_evidence(self, file_path, project, location):
        if not self._configured:
            raise CloudinaryUploadError("Cloudinary not configured")
        folder = settings.cloudinary_upload_folder + "/" + self._slug(project) + "/" + self._slug(location)
        try:
            result = cloudinary.uploader.upload(str(file_path), folder=folder, resource_type="auto")
        except Exception as e:
            raise CloudinaryUploadError(str(e))
        return CloudinaryAsset(
            url=result["secure_url"],
            public_id=result["public_id"],
            folder=folder,
            format=result.get("format", "unknown"),
            width=result.get("width"),
            height=result.get("height"),
            bytes=result.get("bytes", 0),
            tags=result.get("tags", []),
        )

    def _slug(self, text):
        return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
