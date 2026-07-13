from typing import Any
from urllib.parse import quote

import httpx


BASE_URL = "https://api.tfl.gov.uk/Journey/JourneyResults"


class TflClientError(Exception):
    pass


class TflResponseError(Exception):
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code
        super().__init__(f"TfL returned HTTP {status_code}")


async def fetch_journey(from_location: str, to_location: str) -> dict[str, Any]:
    from_path = quote(from_location, safe="")
    to_path = quote(to_location, safe="")
    url = f"{BASE_URL}/{from_path}/to/{to_path}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
    except httpx.HTTPError as exc:
        raise TflClientError("Could not reach TfL Journey Planner.") from exc

    if response.status_code >= 400:
        raise TflResponseError(response.status_code)

    try:
        payload = response.json()
    except ValueError as exc:
        raise TflClientError("TfL returned invalid JSON.") from exc

    if not isinstance(payload, dict):
        raise TflClientError("TfL returned an unexpected payload.")

    return payload
