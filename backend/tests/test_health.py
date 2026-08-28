import asyncio

from httpx import ASGITransport, AsyncClient, Response

from app.main import app


async def request_health() -> Response:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        return await client.get("/api/v1/health")


def test_health_check() -> None:
    response = asyncio.run(request_health())

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "rastro-api",
    }
