import asyncio
import time
from logging import getLogger
from typing import Any

import httpx

logger = getLogger(__name__)


async def fetch_one_url(
    client: httpx.AsyncClient, url: str
) -> list[dict[str, Any]] | None:
    logger.info(f"Fetching data from '{url}'...")
    try:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        data_dict = response.json()  # keys: (['count', 'next', 'previous', 'results'])
        return data_dict.get("results", [])
    except httpx.RequestError as e:
        logger.error(
            f"  -> An HTTP error occurred while fetching '{url}': {e}. Skipping this URL."
        )
        return None
    except Exception as e:
        logger.error(
            f"  -> An unexpected error occurred while processing '{url}': {e}. Skipping this URL."
        )
        return None


async def _load_papers_from_urls(json_urls: list[str]) -> list[dict[str, Any]]:
    combined_papers = []
    logger.info("Starting to load paper data asynchronously...")

    async with httpx.AsyncClient() as client:
        tasks = [fetch_one_url(client, url) for url in json_urls]
        results_from_all_urls = await asyncio.gather(*tasks)

    for paper_list in results_from_all_urls:
        if paper_list:
            combined_papers.extend(paper_list)

    return combined_papers


def _apply_filters_by_queries(
    papers: list[dict[str, Any]], queries: list[str]
) -> list[dict[str, Any]]:
    active_queries = [q.lower() for q in queries if q and not q.isspace()]
    if not active_queries:
        return papers

    filtered_list = []
    for paper in papers:
        # authors_fullnames = [author.get('fullname', '') for author in paper.get('authors', [])]

        searchable_text = " ".join(
            [
                paper.get("name", ""),
                # paper.get('abstract', ''),
                # " ".join(authors_fullnames),
                # " ".join(paper.get('keywords', []))
            ]
        ).lower()

        if all(query in searchable_text for query in active_queries):
            filtered_list.append(paper)

    return filtered_list


async def get_paper_titles_from_url(
    json_urls: list[str], queries: list[str]
) -> list[str]:
    all_papers = await _load_papers_from_urls(json_urls)
    if not all_papers:
        return []

    poster_papers = [
        paper for paper in all_papers if paper.get("eventtype") == "Poster"
    ]

    filtered_papers = _apply_filters_by_queries(poster_papers, queries)
    filtered_titles = [paper.get("name", "No Title Found") for paper in filtered_papers]

    return filtered_titles


if __name__ == "__main__":
    JSON_URLS = [
        "https://icml.cc/static/virtual/data/icml-2024-orals-posters.json",
        "https://iclr.cc/static/virtual/data/iclr-2024-orals-posters.json",
        "https://nips.cc/static/virtual/data/neurips-2024-orals-posters.json",
        "https://cvpr.thecvf.com/static/virtual/data/cvpr-2024-orals-posters.json",
    ]

    queries = ["diffusion model"]
    start_time = time.perf_counter()

    results = asyncio.run(get_paper_titles_from_url(JSON_URLS, queries))

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(f"results: {results}")
    print(f"count: {len(results)}")
    print(f"Execution time: {elapsed_time:.4f} seconds")
