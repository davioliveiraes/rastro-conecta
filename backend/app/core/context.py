from dataclasses import dataclass
from uuid import UUID

from app.models.organization_user import OrganizationRole


@dataclass(frozen=True, slots=True)
class RequestContext:
    user_id: UUID
    organization_id: UUID
    role: OrganizationRole
