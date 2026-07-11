"""
Live job listing search via the JSearch API (RapidAPI).

JSearch aggregates real-time postings from Google for Jobs and the public
web, which in practice covers LinkedIn, Naukri, Glassdoor, Indeed,
ZipRecruiter and most other major job boards through a single endpoint.

Sign up for a free key (200 requests/month, no card required) at:
https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch

Set RAPIDAPI_KEY in backend/.env once you have it.
"""
import os
import requests

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
# JSearch retired the old /search endpoint in favor of cursor-based /search-v2.
SEARCH_URL = f"https://{RAPIDAPI_HOST}/search-v2"

# ISO country code JSearch uses for region-scoped results (India by default,
# since Naukri postings are indexed primarily under "in").
DEFAULT_COUNTRY = "in"


class JobSearchError(Exception):
    """Raised when the live job search cannot be completed."""


def search_jobs(query: str, location: str = "India", num_results: int = 8) -> list[dict]:
    """
    Search live job listings matching `query` near `location`.

    Returns a list of normalized dicts:
      external_id, title, company, location, description,
      apply_link, source, posted_at
    """
    if not RAPIDAPI_KEY:
        raise JobSearchError(
            "RAPIDAPI_KEY is not set. Get a free key at "
            "https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch and add it to backend/.env"
        )

    full_query = f"{query} in {location}" if location else query
    # /search-v2 is cursor-based (no page/num_pages) — omitting cursor gets page 1
    params = {
        "query": full_query,
        "country": DEFAULT_COUNTRY,
        "date_posted": "month",
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST,
    }

    try:
        resp = requests.get(SEARCH_URL, headers=headers, params=params, timeout=30)
    except requests.RequestException as e:
        raise JobSearchError(f"Job search request failed: {e}") from e

    if resp.status_code == 403:
        raise JobSearchError(
            "RapidAPI rejected the request (403). You likely haven't subscribed to the "
            "free plan yet — go to https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch/pricing "
            "and click Subscribe on the free BASIC plan, then retry."
        )
    if resp.status_code == 404:
        raise JobSearchError(
            f"RapidAPI returned 404 for {resp.url} — the endpoint/host may be wrong, or you're "
            "not subscribed to JSearch specifically (RapidAPI keys are account-wide but each API "
        