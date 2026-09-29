"""Projects route."""
from __future__ import annotations
from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from backend.models.schemas import ProjectListResponse, ProjectSummary
from backend.services.vector_store import VectorStore
from backend.utils.logger import logger

router = APIRouter(prefix="/projects", tags=["projects"])
_vector_store = VectorStore()


@router.get("", response_model=ProjectListResponse, status_code=status.HTTP_200_OK)
async def list_projects() -> ProjectListResponse:
    log = logger.bind(endpoint="projects")

    if _vector_store.client is None:
        return ProjectListResponse(projects=[], total=0)

    try:
        result = _vector_store.client.scroll(
            collection_name=_vector_store.collection,
            limit=1000,
            with_payload=True,
            with_vectors=False,
        )
        points = result[0] if result else []
    except Exception as e:
        log.error("Scroll failed: " + str(e))
        return ProjectListResponse(projects=[], total=0)

    buckets = defaultdict(list)
    for p in points:
        payload = p.payload or {}
        buckets[payload.get("project", "unknown")].append(payload)

    summaries = []
    for project, items in buckets.items():
        verified = sum(1 for i in items if i.get("verdict") == "verified")
        needs_review = sum(1 for i in items if i.get("verdict") == "needs_review")
        likely_fake = sum(1 for i in items if i.get("verdict") == "likely_fake")
        summaries.append(ProjectSummary(
            project=project,
            total_evidence=len(items),
            verified_count=verified,
            needs_review_count=needs_review,
            likely_fake_count=likely_fake,
            first_seen=datetime.utcnow(),
            last_seen=datetime.utcnow(),
        ))

    summaries.sort(key=lambda s: s.total_evidence, reverse=True)
    return ProjectListResponse(projects=summaries, total=len(summaries))


@router.get("/{project_name}", response_model=ProjectSummary, status_code=status.HTTP_200_OK)
async def get_project(project_name: str) -> ProjectSummary:
    if _vector_store.client is None:
        raise HTTPException(status_code=503, detail="Vector store unavailable")

    try:
        result = _vector_store.client.scroll(
            collection_name=_vector_store.collection,
            limit=1000,
            with_payload=True,
            with_vectors=False,
        )
        points = result[0] if result else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    matching = [p.payload for p in points if (p.payload or {}).get("project") == project_name]
    if not matching:
        raise HTTPException(status_code=404, detail="Project not found: " + project_name)

    verified = sum(1 for i in matching if i.get("verdict") == "verified")
    needs_review = sum(1 for i in matching if i.get("verdict") == "needs_review")
    likely_fake = sum(1 for i in matching if i.get("verdict") == "likely_fake")

    return ProjectSummary(
        project=project_name,
        total_evidence=len(matching),
        verified_count=verified,
        needs_review_count=needs_review,
        likely_fake_count=likely_fake,
        first_seen=datetime.utcnow(),
        last_seen=datetime.utcnow(),
    )
