from typing import Annotated, NoReturn
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.context import RequestContext
from app.core.database import get_session
from app.models import OrganizationUser, User

USER_ID_HEADER = "X-Rastro-User-Id"
ORGANIZATION_ID_HEADER = "X-Rastro-Organization-Id"

_TEMPORARY_IDENTITY_ENVIRONMENTS = frozenset({"development", "test"})
_IDENTITY_ERROR_DETAIL = "User identity could not be validated."
_ORGANIZATION_ACCESS_ERROR_DETAIL = "Organization access denied."


def _raise_unauthorized() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=_IDENTITY_ERROR_DETAIL,
    )


def _raise_forbidden() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=_ORGANIZATION_ACCESS_ERROR_DETAIL,
    )


def _parse_user_id(value: str | None) -> UUID:
    if value is None:
        _raise_unauthorized()

    try:
        return UUID(value)
    except ValueError:
        _raise_unauthorized()


def _parse_organization_id(value: str | None) -> UUID:
    if value is None:
        _raise_forbidden()

    try:
        return UUID(value)
    except ValueError:
        _raise_forbidden()


def get_current_user(
    settings: Annotated[Settings, Depends(get_settings)],
    session: Annotated[Session, Depends(get_session)],
    user_id_header: Annotated[
        str | None,
        Header(alias=USER_ID_HEADER),
    ] = None,
) -> User:
    if (
        settings.app_env.strip().casefold()
        not in _TEMPORARY_IDENTITY_ENVIRONMENTS
    ):
        _raise_unauthorized()

    user_id = _parse_user_id(user_id_header)
    user = session.get(User, user_id)

    if user is None or not user.is_active:
        _raise_unauthorized()

    return user


def get_request_context(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    organization_id_header: Annotated[
        str | None,
        Header(alias=ORGANIZATION_ID_HEADER),
    ] = None,
) -> RequestContext:
    organization_id = _parse_organization_id(organization_id_header)
    membership = session.get(
        OrganizationUser,
        {
            "organization_id": organization_id,
            "user_id": current_user.id,
        },
    )

    if membership is None:
        _raise_forbidden()

    return RequestContext(
        user_id=current_user.id,
        organization_id=organization_id,
        role=membership.role,
    )
