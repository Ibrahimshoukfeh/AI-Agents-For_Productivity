from fastapi import APIRouter, HTTPException, Query

from app.models import QuickCommuteResponse
from app.parser import NoJourneysFoundError, parse_quick_commute
from app.tfl_client import TflClientError, TflResponseError, fetch_journey

router = APIRouter()


@router.get("/quick-commute", response_model=QuickCommuteResponse)
async def quick_commute(
    from_location: str = Query(...),
    to_location: str = Query(...),
) -> QuickCommuteResponse:
    from_location = from_location.strip()
    to_location = to_location.strip()

    if not from_location or not to_location:
        raise HTTPException(status_code=400, detail="from_location and to_location are required.")

    try:
        payload = await fetch_journey(from_location, to_location)
        return parse_quick_commute(payload)
    except TflResponseError as exc:
        if 400 <= exc.status_code < 500:
            raise HTTPException(
                status_code=404,
                detail="No journeys found for the requested commute.",
            ) from exc
        raise HTTPException(status_code=502, detail="TfL Journey Planner returned an error.") from exc
    except TflClientError as exc:
        raise HTTPException(status_code=503, detail="TfL Journey Planner is unavailable.") from exc
    except NoJourneysFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="No journeys found for the requested commute.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=502, detail="TfL Journey Planner returned malformed data.") from exc
