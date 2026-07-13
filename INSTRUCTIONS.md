# INSTRUCTIONS.md

## Project

Build a FastAPI application that acts as a simplified wrapper around the TfL Journey Planner API.

The purpose of the app is to accept a simple request, call TfL behind the scenes, discard most of the noisy upstream JSON, and return a compact, easy-to-consume response for a front-end application.

## Required endpoint

Create one `GET` endpoint:

- path: `/api/v1/quick-commute`
- query parameters:
  - `from_location`
  - `to_location`

Example request:

```text
/api/v1/quick-commute?from_location=Waterloo&to_location=Camden%20Town
```

## Upstream API

Build the upstream request URL using:

```text
https://api.tfl.gov.uk/Journey/JourneyResults/{from_location}/to/{to_location}
```

Use an `async` HTTP request.

## Required behavior

When the endpoint is called, the application should:

1. build the TfL Journey Planner URL using the query parameter values
2. make an asynchronous request to the TfL API
3. inspect the `journeys` array in the upstream response
4. take the first journey only
5. extract only:
   - total duration in minutes
   - departure time
   - arrival time
   - user-friendly instructions derived from the journey legs
6. return a clean, strictly typed JSON payload

## Target response shape

Return JSON in this structure:

```json
{
  "summary": {
    "start": "London Waterloo",
    "destination": "Camden Town",
    "total_duration_minutes": 18
  },
  "times": {
    "departing_at": "08:15",
    "arriving_at": "08:33"
  },
  "instructions": [
    "Take the Northern line northbound towards Edgware.",
    "Get off at Camden Town Underground Station."
  ]
}
```

The exact instruction wording can be normalized from the upstream leg data, but the output structure should stay stable.

## Technical expectations

- use FastAPI
- use `httpx` for async HTTP
- use Pydantic models for the response schema
- keep HTTP client logic separate from parsing/transformation logic where practical
- handle upstream failures and missing journeys gracefully

## Testing expectations

Add tests that cover:

- a successful response path
- invalid or unknown locations
- no journeys returned
- upstream HTTP failure behavior

Prefer mocked or fixture-based TfL responses rather than relying only on live API calls.

## Workflow expectations

Before implementation:

- inspect the project files
- read `AGENTS.md` if present
- propose a plan first
- list the files to create or modify
- explain the testing strategy

During implementation:

- keep the work bounded
- do not change unrelated files
- do not add unnecessary dependencies
- explain risky commands before running them

## Commit expectations

- make atomic commits
- keep commit scope logical and reviewable
- do not create one giant final commit for the entire project if smaller checkpoints make more sense

## Suggested implementation order

1. scaffold the FastAPI app structure
2. define response models
3. implement the TfL client
4. implement the parsing/transformation logic
5. implement the route
6. add tests
7. run tests and fix failures

## Bonus ideas

Optional stretch goals:

- add a `warning` field when the route is disrupted
- append a weather note for the destination
- improve diagnostics or logging without leaking sensitive information
