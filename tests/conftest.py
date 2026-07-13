import json
from pathlib import Path
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict[str, Any]:
    with (FIXTURES / name).open(encoding="utf-8") as fixture_file:
        return json.load(fixture_file)


@pytest.fixture
async def api_client() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
