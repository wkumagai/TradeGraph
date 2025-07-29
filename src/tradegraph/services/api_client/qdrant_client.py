import os
from logging import getLogger
from typing import Any

from tradegraph.services.api_client.base_http_client import BaseHTTPClient
from tradegraph.services.api_client.response_parser import ResponseParser
from tradegraph.services.api_client.retry_policy import raise_for_status

logger = getLogger(__name__)


class QdrantClient(BaseHTTPClient):
    def __init__(
        self,
        base_url: str = "https://06e0f5e0-2a43-41fe-913c-82fce00a7bd2.us-east4-0.gcp.cloud.qdrant.io:6333",
        default_headers: dict[str, str] | None = None,
    ):
        api_key = os.getenv("QDRANT_API_KEY")
        if not api_key:
            raise EnvironmentError("QDRANT_API_KEY is not set")

        auth_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        super().__init__(
            base_url=base_url,
            default_headers={**auth_headers, **(default_headers or {})},
        )
        self._parser = ResponseParser()

    def create_a_collection(
        self,
        collection_name: str,
        vector_size: int,
        distance: str = "Cosine",
        timeout: float = 60,
    ):
        # https://api.qdrant.tech/api-reference/collections/create-collection
        payload = {"vectors": {"size": vector_size, "distance": distance}}
        response = self.put(
            path=f"/collections/{collection_name}", json=payload, timeout=timeout
        )
        return self._parser.parse(response, as_="json")

    def upsert_points(
        self,
        collection_name: str,
        data_sets: list[dict[str, Any]],
        timeout: float = 600,
    ):
        # https://api.qdrant.tech/api-reference/points/upsert-points
        payload = {"points": data_sets}
        response = self.put(
            path=f"/collections/{collection_name}/points", json=payload, timeout=timeout
        )
        return self._parser.parse(response, as_="json")

    def query_points(
        self,
        collection_name: str,
        query_vector: list[float],
        limit: int = 10,
        timeout: float = 15.0,
    ) -> Any:
        # https://api.qdrant.tech/api-reference/search/query-points
        payload = {
            "query": {
                "nearest": query_vector,
            },
            "limit": limit,
            "with_payload": True,
        }
        response = self.post(
            path=f"/collections/{collection_name}/points/query",
            json=payload,
            timeout=timeout,
        )
        raise_for_status(response, path="search")

        return self._parser.parse(response, as_="json")

    def retrieve_a_points(
        self, collection_name: str, id: int | str, timeout: float = 15.0
    ):
        # https://api.qdrant.tech/api-reference/points/get-point
        response = self.get(
            path=f"/collections/{collection_name}/points/{id}", timeout=timeout
        )
        raise_for_status(response, path="retrieve")
        return self._parser.parse(response, as_="json")
