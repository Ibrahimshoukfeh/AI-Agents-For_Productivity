import httpx
import pytest
import respx

from app.tfl_client import BASE_URL
from tests.conftest import load_fixture


@pytest.mark.respx(base_url=BASE_URL)
async def test_quick_commute_success(api_client: httpx.AsyncClient, respx_mock: respx.Router) -> None:
    respx_mock.get("/Waterloo/to/Camden%20Town").mock(
        return_value=httpx.Response(200, json=load_fixture("journey_success.json"))
    )

    response = await api_client.get(
        "/api/v1/quick-commute",
        params={"from_location": "Waterloo", "to_location": "Camden Town"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "summary": {
            "start": "London Waterloo",
            "destination": "Camden Town",
            "total_duration_minutes": 18,
        },
        "times": {
            "departing_at": "08:15",
            "arriving_at": "08:33",
        },
        "instructions": [
            "Take the Northern line northbound towards Edgware.",
            "Get off at Camden Town Underground Station.",
        ],
    }


async def test_quick_commute_blank_query_param(api_client: httpx.AsyncClient) -> None:
    response = await api_client.get(
        "/api/v1/quick-commute",
        params={"from_location": " ", "to_location": "Camden Town"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "from_location and to_location are required."}


@pytest.mark.respx(base_url=BASE_URL)
async def test_quick_commute_no_journeys(api_client: httpx.AsyncClient, respx_mock: respx.Router) -> None:
    respx_mock.get("/Waterloo/to/Camden%20Town").mock(
        return_value=httpx.Response(200, json=load_fixture("journey_no_results.json"))
    )

    response = await api_client.get(
        "/api/v1/quick-commute",
        params={"from_location": "Waterloo", "to_location": "Camden Town"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "No journeys found for the requested commute."}


@pytest.mark.respx(base_url=BASE_URL)
async def test_quick_commute_tfl_4xx(api_client: httpx.AsyncClient, respx_mock: respx.Router) -> None:
    respx_mock.get("/Unknown/to/Camden%20Town").mock(
        return_value=httpx.Response(404, json=load_fixture("journey_invalid_location.json"))
    )

    response = await api_client.get(
        "/api/v1/quick-commute",
        params={"from_location": "Unknown", "to_location": "Camden Town"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "No journeys found for the requested commute."}


@pytest.mark.respx(base_url=BASE_URL)
async def test_quick_commute_tfl_5xx(api_client: httpx.AsyncClient, respx_mock: respx.Router) -> None:
    respx_mock.get("/Waterloo/to/Camden%20Town").mock(return_value=httpx.Response(500))

    response = await api_client.get(
        "/api/v1/quick-commute",
        params={"from_location": "Waterloo", "to_location": "Camden Town"},
    )

    assert response.status_code == 502
    assert response.json() == {"detail": "TfL Journey Planner returned an error."}


@pytest.mark.respx(base_url=BASE_URL)
async def test_quick_commute_timeout(api_client: httpx.AsyncClient, respx_mock: respx.Router) -> None:
    respx_mock.get("/Waterloo/to/Camden%20Town").mock(
        side_effect=httpx.ConnectTimeout("connection timed out")
    )

    response = await api_client.get(
        "/api/v1/quick-commute",
        params={"from_location": "Waterloo", "to_location": "Camden Town"},
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "TfL Journey Planner is unavailable."}
