# TfL Quick Commute

Small FastAPI service that wraps the TfL Journey Planner API and returns a compact commute response.

## Run

```powershell
uv run uvicorn app.main:app --reload
```

## Test

```powershell
uv run pytest
```

## Endpoint

```text
GET /api/v1/quick-commute?from_location=Waterloo&to_location=Camden%20Town
```
