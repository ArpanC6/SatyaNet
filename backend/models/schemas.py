"""Pydantic schemas."""
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from backend.models.enums import (
    TrustLevel,
    SignalType,
    SignalStatus,
)


class SignalScore(BaseModel):
    signal: SignalType
    score: float = Field(..., ge=0.0, le=1.0)
    status: SignalStatus
    weight: float = Field(..., ge=0.0, le=1.0)
    reason: Optional[str] = None


class TruthScoreResult(BaseModel):
    trust_score: float = Field(..., ge=0.0, le=100.0)
    trust_level: TrustLevel
    signals: List[SignalScore]
    reasons: List[str] = Field(default_factory=list)
    flags: List[str] = Field(default_factory=list)
    computed_at: datetime = Field(default_factory=datetime.utcnow)
    methodology: str = Field(default="Bayesian weighted fusion of 5 weak signals (v1.0)")


class GeoLocation(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)


class ExifMetadata(BaseModel):
    has_exif: bool
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    datetime_original: Optional[datetime] = None
    gps: Optional[GeoLocation] = None
    software: Optional[str] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    raw_tags: Dict[str, str] = Field(default_factory=dict)


class CloudinaryAsset(BaseModel):
    url: str
    public_id: str
    folder: str
    format: str
    width: Optional[int] = None
    height: Optional[int] = None
    bytes: int = 0
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EvidenceMetadata(BaseModel):
    evidence_id: str
    project: str
    location_label: str
    claimed_date: datetime
    media_type: str
    file_name: str
    file_size_bytes: int
    sha256_hash: str
    phash: Optional[str] = None
    exif: ExifMetadata
    cloudinary: CloudinaryAsset
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VerifyRequest(BaseModel):
    project: str = Field(..., min_length=1, max_length=120)
    location_label: str = Field(..., min_length=1, max_length=200)
    claimed_date: datetime
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class VerifyResponse(BaseModel):
    evidence: EvidenceMetadata
    verification: TruthScoreResult
    report_url: Optional[str] = None


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    project: Optional[str] = None
    top_k: int = Field(default=10, ge=1, le=50)


class SearchHit(BaseModel):
    evidence_id: str
    project: str
    location_label: str
    trust_score: float
    similarity: float
    cloudinary_url: str


class SearchResponse(BaseModel):
    query: str
    hits: List[SearchHit]
    took_ms: float


class ProjectSummary(BaseModel):
    project: str
    total_evidence: int
    verified_count: int
    needs_review_count: int
    likely_fake_count: int
    first_seen: datetime
    last_seen: datetime


class ProjectListResponse(BaseModel):
    projects: List[ProjectSummary]
    total: int


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Dict[str, object] = Field(default_factory=dict)
    request_id: Optional[str] = None
