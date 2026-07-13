\# AGENTS.md



\## Project rules



\- Use uv for Python package and task management.

\- Use FastAPI for the API.

\- Use httpx for async HTTP requests.

\- Use Pydantic models for request/response structure.

\- Keep FastAPI route code separate from TfL client logic and parsing logic.

\- Add tests for new behavior.

\- Use mocked TfL responses in tests instead of depending only on live TfL availability.

\- Ask for a plan before making non-trivial edits.

\- Keep changes small and reviewable.

\- Do not change unrelated files.

\- Explain risky commands before running them.



\## Expected endpoint



Create one GET endpoint:



`/api/v1/quick-commute`



Query parameters:



\- `from\_location`

\- `to\_location`



Example:



`/api/v1/quick-commute?from\_location=Waterloo\&to\_location=Camden%20Town`



\## Expected workflow



1\. Inspect the workspace.

2\. Read `INSTRUCTIONS.md`.

3\. Propose a project plan first.

4\. Do not implement until the plan is approved.

5\. After approval, build the project step by step.

6\. Run tests after implementation.

