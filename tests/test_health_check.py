import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio
async def test_liveness(test_client: AsyncClient) -> None:
    # when
    response = await test_client.get("/api/v1/liveness")

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "alive"}
