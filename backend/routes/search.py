"""Search route."""
from __future__ import annotations
import time

from fastapi import APIRouter, HTTPException, status

from backend.models.schemas import SearchHit, SearchRequest, SearchResponse
from backend.services.vector_store import VectorStore
from backend.utils.logger import logger

router = APIRouter(prefix="/search", tags=["search"])
_vector_store = VectorStore()


@router.post("", response_model=SearchResponse, status_code=status.HTTP_200_OK)
async def semantic_search(request: SearchRequest) -> SearchResponse:
    log = logger.bind(endpoint="search")
    started = time.perf_counter()

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    raw_results = _vector_store.search(
        query=request.query,
        top_k=request.top_k,
        project_filter=request.project,
    )

    hits = []
    for r in raw_results:
        try:
            hits.append(SearchHit(
                evidence_id=r.get("evidence_id", "unknown"),
                project=r.get("project", "unknown"),
                location_label=r.get("location_label", "unknown"),
                trust_score=float(r.get("trust_score", 0.0)),
                similarity=float(r.get("score", 0.0)),
                cloudinary_url=r.get("cloudinary_url", "https://example.com/img.jpg"),
            ))
        except Exception as e:
            log.warning("Skipping malformed hit: " + str(e))

    took_ms = (time.perf_counter() - started) * 1000
    return SearchResponse(query=request.query, hits=hits, took_ms=round(took_ms, 2))
