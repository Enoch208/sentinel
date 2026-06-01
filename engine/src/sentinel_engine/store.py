from __future__ import annotations

from typing import Any, cast

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client import models as qm

from sentinel_engine.types import Neighbor, Vector


class PerceptionStore:
    def __init__(
        self,
        client: QdrantClient,
        collection: str,
        vector_name: str,
        dim: int,
        quantize: bool,
    ) -> None:
        self._client = client
        self._collection = collection
        self._name = vector_name
        self._dim = dim
        self._quantize = quantize
        self.quantization_active: bool = False
        self._ensure(quantize)

    @classmethod
    def open(
        cls,
        path: str,
        collection: str,
        vector_name: str,
        dim: int,
        quantize: bool = True,
    ) -> PerceptionStore:
        return cls(QdrantClient(path=path), collection, vector_name, dim, quantize)

    @classmethod
    def in_memory(
        cls,
        collection: str,
        vector_name: str,
        dim: int,
        quantize: bool = False,
    ) -> PerceptionStore:
        client = QdrantClient(location=":memory:")
        return cls(client, collection, vector_name, dim, quantize)

    def _vectors_config(self) -> dict[str, qm.VectorParams]:
        return {
            self._name: qm.VectorParams(
                size=self._dim, distance=qm.Distance.COSINE
            )
        }

    def _ensure(self, quantize: bool) -> None:
        if not self._client.collection_exists(self._collection):
            quantization = (
                qm.ScalarQuantization(
                    scalar=qm.ScalarQuantizationConfig(
                        type=qm.ScalarType.INT8, always_ram=True
                    )
                )
                if quantize
                else None
            )
            try:
                self._client.create_collection(
                    self._collection,
                    vectors_config=self._vectors_config(),
                    quantization_config=quantization,
                )
            except (TypeError, ValueError):
                self._client.create_collection(
                    self._collection,
                    vectors_config=self._vectors_config(),
                )
        self.quantization_active = self._quantization_in_effect()

    def _quantization_in_effect(self) -> bool:
        info = self._client.get_collection(self._collection)
        return getattr(info.config, "quantization_config", None) is not None

    def upsert(self, point_id: int, vector: Vector, payload: dict[str, Any]) -> None:
        self._client.upsert(
            self._collection,
            points=[
                qm.PointStruct(
                    id=point_id,
                    vector={self._name: vector.tolist()},
                    payload=payload,
                )
            ],
        )

    def query(self, vector: Vector, k: int) -> list[Neighbor]:
        response = self._client.query_points(
            self._collection,
            query=vector.tolist(),
            using=self._name,
            limit=k,
            with_payload=False,
        )
        return [Neighbor(id=int(p.id), score=float(p.score)) for p in response.points]

    def recommend(
        self, positive: list[int], negative: list[int], k: int
    ) -> list[Neighbor]:
        response = self._client.query_points(
            self._collection,
            query=qm.RecommendQuery(
                recommend=qm.RecommendInput(
                    positive=cast("list[Any]", positive),
                    negative=cast("list[Any]", negative),
                )
            ),
            using=self._name,
            limit=k,
            with_payload=False,
        )
        return [Neighbor(id=int(p.id), score=float(p.score)) for p in response.points]

    def get_vector(self, point_id: int) -> Vector | None:
        records = self._client.retrieve(
            self._collection, ids=[point_id], with_vectors=True
        )
        if not records:
            return None
        stored = records[0].vector
        raw = stored[self._name] if isinstance(stored, dict) else stored
        return np.asarray(raw, dtype=np.float32)

    def delete(self, point_id: int) -> None:
        self._client.delete(
            self._collection, points_selector=qm.PointIdsList(points=[point_id])
        )

    def reset(self) -> None:
        self._client.delete_collection(self._collection)
        self._ensure(self._quantize)

    def facet(self, key: str) -> dict[str, int]:
        response = self._client.facet(collection_name=self._collection, key=key)
        return {str(hit.value): int(hit.count) for hit in response.hits}

    def sample(self, limit: int) -> list[tuple[int, Vector, str]]:
        points, _ = self._client.scroll(
            self._collection,
            limit=limit,
            with_vectors=True,
            with_payload=True,
        )
        out: list[tuple[int, Vector, str]] = []
        for point in points:
            stored = point.vector
            raw = stored[self._name] if isinstance(stored, dict) else stored
            payload = point.payload or {}
            zone = str(payload.get("zone", "default"))
            out.append((int(point.id), np.asarray(raw, dtype=np.float32), zone))
        return out

    def count(self) -> int:
        return int(self._client.count(self._collection).count)
