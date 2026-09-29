"""Verify route."""
from __future__ import annotations
import shutil
import tempfile
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from backend.models.schemas import EvidenceMetadata, ExifMetadata, VerifyResponse, CloudinaryAsset
from backend.services.cloudinary_service import CloudinaryService
from backend.services.exif_forensics import ExifForensics
from backend.services.truth_score import TruthScoreEngine
from backend.services.vector_store import VectorStore
from backend.utils.exceptions import CloudinaryUploadError, ExifExtractionError, SatyaNetError
from backend.utils.logger import logger

router = APIRouter(prefix="/verify", tags=["verification"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov"}
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024

_truth_engine = TruthScoreEngine()
_cloudinary = CloudinaryService()
_exif = ExifForensics()
_vector_store = VectorStore()


@router.post("", response_model=VerifyResponse, status_code=status.HTTP_201_CREATED)
async def verify_evidence(
    file: UploadFile = File(...),
    project: str = Form(...),
    location_label: str = Form(...),
    claimed_date: str = Form(...),
    latitude: float = Form(default=None),
    longitude: float = Form(default=None),
) -> VerifyResponse:
    log = logger.bind(endpoint="verify", project=project)

    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Unsupported file type: " + suffix)

    try:
        claimed_dt = datetime.fromisoformat(claimed_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid claimed_date: " + str(e))

    evidence_id = str(uuid.uuid4())
    tmp_dir = Path(tempfile.mkdtemp(prefix="satyanet_"))
    tmp_path = tmp_dir / (evidence_id + suffix)

    try:
        with tmp_path.open("wb") as out:
            shutil.copyfileobj(file.file, out, length=1024 * 1024)

        file_size = tmp_path.stat().st_size
        if file_size > MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=413, detail="File too large")

        sha256_hash = _exif.compute_sha256(tmp_path)

        try:
            exif_meta = _exif.extract(tmp_path)
        except ExifExtractionError:
            exif_meta = ExifMetadata(has_exif=False)

        try:
            asset = _cloudinary.upload_evidence(tmp_path, project, location_label)
        except CloudinaryUploadError as e:
            log.warning("Cloudinary skipped: " + str(e))
            asset = None

        verification = _truth_engine.score(
            image_path=tmp_path,
            claimed_date=claimed_dt,
            claimed_lat=latitude,
            claimed_lon=longitude,
        )

        if asset is None:
            asset = CloudinaryAsset(
                url="https://res.cloudinary.com/placeholder/image/upload/sample.jpg",
                public_id="offline/" + evidence_id,
                folder="satyanet/offline",
                format=suffix.lstrip("."),
                bytes=file_size,
                tags=[],
            )

        evidence = EvidenceMetadata(
            evidence_id=evidence_id,
            project=project,
            location_label=location_label,
            claimed_date=claimed_dt,
            media_type="video" if suffix in {".mp4", ".mov"} else "image",
            file_name=file.filename or "unknown",
            file_size_bytes=file_size,
            sha256_hash=sha256_hash,
            exif=exif_meta,
            cloudinary=asset,
        )

        _vector_store.upsert_evidence(
            evidence_id=evidence_id,
            text=project + " " + location_label + " " + claimed_date + " " + (file.filename or ""),
            payload={
                "project": project,
                "location_label": location_label,
                "trust_score": verification.trust_score,
                "verdict": verification.trust_level.value,
                "cloudinary_url": str(asset.url),
            },
        )

        return VerifyResponse(evidence=evidence, verification=verification)

    except SatyaNetError as e:
        log.error("Verification failed: " + e.message)
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
