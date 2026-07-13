from datetime import datetime
from typing import Any

from app.models import CommuteSummary, CommuteTimes, QuickCommuteResponse


class NoJourneysFoundError(Exception):
    pass


def parse_quick_commute(payload: dict[str, Any]) -> QuickCommuteResponse:
    journeys = payload.get("journeys")
    if not isinstance(journeys, list) or not journeys:
        raise NoJourneysFoundError("No journeys found for the requested commute.")

    journey = journeys[0]
    if not isinstance(journey, dict):
        raise ValueError("TfL journey payload is malformed.")

    legs = journey.get("legs") or []
    if not isinstance(legs, list):
        raise ValueError("TfL journey legs payload is malformed.")

    start = _point_name(_first_leg(legs), "departurePoint", "Unknown start")
    destination = _point_name(_last_leg(legs), "arrivalPoint", "Unknown destination")

    return QuickCommuteResponse(
        summary=CommuteSummary(
            start=start,
            destination=destination,
            total_duration_minutes=_required_int(journey, "duration"),
        ),
        times=CommuteTimes(
            departing_at=_format_time(_required_str(journey, "startDateTime")),
            arriving_at=_format_time(_required_str(journey, "arrivalDateTime")),
        ),
        instructions=_build_instructions(legs),
    )


def _first_leg(legs: list[Any]) -> dict[str, Any]:
    return legs[0] if legs and isinstance(legs[0], dict) else {}


def _last_leg(legs: list[Any]) -> dict[str, Any]:
    return legs[-1] if legs and isinstance(legs[-1], dict) else {}


def _point_name(leg: dict[str, Any], field: str, fallback: str) -> str:
    point = leg.get(field)
    if isinstance(point, dict):
        common_name = point.get("commonName")
        if isinstance(common_name, str) and common_name.strip():
            return common_name.strip()
    return fallback


def _required_int(data: dict[str, Any], field: str) -> int:
    value = data.get(field)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"TfL journey field {field!r} is missing or invalid.")
    return value


def _required_str(data: dict[str, Any], field: str) -> str:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"TfL journey field {field!r} is missing or invalid.")
    return value


def _format_time(value: str) -> str:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    return parsed.strftime("%H:%M")


def _build_instructions(legs: list[Any]) -> list[str]:
    instructions: list[str] = []

    for leg in legs:
        if not isinstance(leg, dict):
            continue

        instruction = leg.get("instruction")
        if isinstance(instruction, dict):
            text = instruction.get("summary") or instruction.get("detailed")
            if isinstance(text, str) and text.strip():
                instructions.append(_with_period(text.strip()))
                continue

        departure = _point_name(leg, "departurePoint", "the start")
        arrival = _point_name(leg, "arrivalPoint", "the destination")
        instructions.append(f"Travel from {departure} to {arrival}.")

    return instructions


def _with_period(value: str) -> str:
    return value if value.endswith((".", "!", "?")) else f"{value}."
