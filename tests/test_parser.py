import pytest

from app.parser import NoJourneysFoundError, parse_quick_commute
from tests.conftest import load_fixture


def test_parse_quick_commute_success() -> None:
    response = parse_quick_commute(load_fixture("journey_success.json"))

    assert response.model_dump() == {
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


def test_parse_quick_commute_no_journeys() -> None:
    with pytest.raises(NoJourneysFoundError):
        parse_quick_commute(load_fixture("journey_no_results.json"))


def test_parse_quick_commute_instruction_fallback() -> None:
    payload = load_fixture("journey_success.json")
    payload["journeys"][0]["legs"][0].pop("instruction")

    response = parse_quick_commute(payload)

    assert response.instructions[0] == (
        "Travel from London Waterloo to Camden Town Underground Station."
    )
