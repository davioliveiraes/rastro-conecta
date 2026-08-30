import asyncio
from collections.abc import Iterator
from typing import Any
from uuid import UUID, uuid4

import pytest
from httpx import ASGITransport, AsyncClient, Response

from app.api.dependencies import ORGANIZATION_ID_HEADER, USER_ID_HEADER
from app.core.config import Settings, get_settings
from app.core.database import get_session
from app.main import app
from app.models import OrganizationRole, OrganizationUser, User


class FakeSession:
    def __init__(
        self,
        *,
        users: dict[UUID, User] | None = None,
        memberships: dict[tuple[UUID, UUID], OrganizationUser] | None = None,
    ) -> None:
        self.users = users or {}
        self.memberships = memberships or {}
        self.user_lookups = 0

    def get(self, entity: type[Any], identity: Any) -> Any | None:
        if entity is User:
            self.user_lookups += 1
            return self.users.get(identity)

        if entity is OrganizationUser:
            key = (
                identity["organization_id"],
                identity["user_id"],
            )
            return self.memberships.get(key)

        raise AssertionError(f"Unexpected entity lookup: {entity}")


@pytest.fixture(autouse=True)
def reset_dependency_overrides() -> Iterator[None]:
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


def configure_dependencies(
    session: FakeSession,
    *,
    app_env: str = "test",
) -> None:
    def override_session() -> Iterator[FakeSession]:
        yield session

    app.dependency_overrides[get_session] = override_session
    app.dependency_overrides[get_settings] = lambda: Settings(app_env=app_env)


async def make_request(
    path: str,
    *,
    headers: dict[str, str] | None = None,
) -> Response:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        return await client.get(path, headers=headers)


def context_headers(user_id: UUID, organization_id: UUID) -> dict[str, str]:
    return {
        USER_ID_HEADER: str(user_id),
        ORGANIZATION_ID_HEADER: str(organization_id),
    }


def test_health_remains_public_without_context() -> None:
    response = asyncio.run(make_request("/api/v1/health"))

    assert response.status_code == 200


def test_context_rejects_missing_identity() -> None:
    configure_dependencies(FakeSession())

    response = asyncio.run(make_request("/api/v1/me/context"))

    assert response.status_code == 401


def test_context_rejects_invalid_user_uuid() -> None:
    configure_dependencies(FakeSession())

    response = asyncio.run(
        make_request(
            "/api/v1/me/context",
            headers={
                USER_ID_HEADER: "not-a-uuid",
                ORGANIZATION_ID_HEADER: str(uuid4()),
            },
        )
    )

    assert response.status_code == 401


def test_context_rejects_unknown_user() -> None:
    configure_dependencies(FakeSession())
    user_id = uuid4()

    response = asyncio.run(
        make_request(
            "/api/v1/me/context",
            headers=context_headers(user_id, uuid4()),
        )
    )

    assert response.status_code == 401


def test_context_rejects_inactive_user() -> None:
    user_id = uuid4()
    user = User(
        id=user_id,
        email="inactive@example.com",
        name="Inactive User",
        is_active=False,
    )
    configure_dependencies(FakeSession(users={user_id: user}))

    response = asyncio.run(
        make_request(
            "/api/v1/me/context",
            headers=context_headers(user_id, uuid4()),
        )
    )

    assert response.status_code == 401


def test_context_rejects_invalid_organization_uuid() -> None:
    user_id = uuid4()
    user = User(
        id=user_id,
        email="user@example.com",
        name="Example User",
        is_active=True,
    )
    configure_dependencies(FakeSession(users={user_id: user}))

    response = asyncio.run(
        make_request(
            "/api/v1/me/context",
            headers={
                USER_ID_HEADER: str(user_id),
                ORGANIZATION_ID_HEADER: "not-a-uuid",
            },
        )
    )

    assert response.status_code == 403


def test_context_rejects_user_without_membership() -> None:
    user_id = uuid4()
    user = User(
        id=user_id,
        email="user@example.com",
        name="Example User",
        is_active=True,
    )
    configure_dependencies(FakeSession(users={user_id: user}))

    response = asyncio.run(
        make_request(
            "/api/v1/me/context",
            headers=context_headers(user_id, uuid4()),
        )
    )

    assert response.status_code == 403


def test_context_returns_valid_membership_and_role() -> None:
    user_id = uuid4()
    organization_id = uuid4()
    user = User(
        id=user_id,
        email="owner@example.com",
        name="Organization Owner",
        is_active=True,
    )
    membership = OrganizationUser(
        organization_id=organization_id,
        user_id=user_id,
        role=OrganizationRole.OWNER,
    )
    configure_dependencies(
        FakeSession(
            users={user_id: user},
            memberships={(organization_id, user_id): membership},
        )
    )

    response = asyncio.run(
        make_request(
            "/api/v1/me/context",
            headers=context_headers(user_id, organization_id),
        )
    )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": str(user_id),
        "organization_id": str(organization_id),
        "role": "owner",
    }


def test_context_rejects_temporary_identity_in_production() -> None:
    user_id = uuid4()
    organization_id = uuid4()
    user = User(
        id=user_id,
        email="owner@example.com",
        name="Organization Owner",
        is_active=True,
    )
    membership = OrganizationUser(
        organization_id=organization_id,
        user_id=user_id,
        role=OrganizationRole.OWNER,
    )
    session = FakeSession(
        users={user_id: user},
        memberships={(organization_id, user_id): membership},
    )
    configure_dependencies(session, app_env="production")

    response = asyncio.run(
        make_request(
            "/api/v1/me/context",
            headers=context_headers(user_id, organization_id),
        )
    )

    assert response.status_code == 401
    assert session.user_lookups == 0
