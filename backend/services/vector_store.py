"""Qdrant vector store."""
from __future__ import annotations
import hashlib

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from backend.config import settings
from backend.utils.logger import logger


class VectorStore:
    VECTOR_SIZE = 64

    def __init__(self):
        self.log = logger.bind(service="vector_store")
        try:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key or None,
                timeout=5.0,
            )
            self.collection = settings.qdrant_collection
            self._ensure_collection()
        except Exception as e:
            self.log.warning("Qdrant unavailable: " + str(e))
            self.client = None
            self.collection = settings.qdrant_collection

    def _ensure_collection(self):
        if self.client is None:
            return
        try:
            names = [c.name for c in self.client.get_collections().collections]
            if self.collection not in names:
                self.client.create_collection(
                    collection_name=self.collection,
                    vectors_config=qmodels.VectorParams(
                        size=self.VECTOR_SIZE,
                        distance=qmodels.Distance.COSINE,
                    ),
                )
        except Exception as e:
            self.log.warning("Collection ensure failed: " + str(e))

    def upsert_evidence(self, evidence_id, text, payload):
        if self.client is None:
            return False
        try:
            self.client.upsert(
                collection_name=self.collection,
                points=[qmodels.PointStruct(
                    id=self._stable_id(evidence_id),
                    vector=self._embed(text),
                    payload={"evidence_id": evidence_id, **payload},
                )],
            )
            return True
        except Exception as e:
            self.log.error("Upsert failed: " + str(e))
            return False

    def search(self, query, top_k=10, project_filter=None):
        if self.client is None:
            return []
        try:
            qfilter = None
            if project_filter:
                qfilter = qmodels.Filter(must=[qmodels.FieldCondition(
                    key="project",
                    match=qmodels.MatchValue(value=project_filter),
                )])
            results = self.client.search(
                collection_name=self.collection,
                query_vector=self._embed(query),
                limit=top_k,
                query_filter=qfilter,
            )
            return [{"score": r.score, **(r.payload or {})} for r in results]
        except Exception as e:
            self.log.error("Search failed: " + str(e))
            return []

    def _embed(self, text):
        h = hashlib.sha256(text.encode("utf-8")).digest()
        vec = [((b / 255.0) * 2.0 - 1.0) for b in h]
        if len(vec) < self.VECTOR_SIZE:
            vec += [0.0] * (self.VECTOR_SIZE - len(vec))
        return vec[: self.VECTOR_SIZE]

    def _stable_id(self, evidence_id):
        return int(hashlib.sha256(evidence_id.encode()).hexdigest()[:15], 16)
