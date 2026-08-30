from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.dependencies import get_request_context
from app.core.context import RequestContext
from app.models import OrganizationRole

router = APIRouter(prefix="/me", tags=["context"])


class ContextResponse(BaseModel):
    user_id: UUID
    organization_id: UUID
    role: OrganizationRole


@router.get("/context", response_model=ContextResponse)
def read_request_context(
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> ContextResponse:
    return ContextResponse(
        user_id=context.user_id,
        organization_id=context.organization_id,
        role=context.role,
    )
