from sqlalchemy import Enum

from app.core.database import Base
from app.models import Organization, OrganizationRole, OrganizationUser, User


def test_metadata_contains_only_multi_tenant_foundation_tables() -> None:
    assert set(Base.metadata.tables) == {
        "organizations",
        "organization_users",
        "users",
    }
    assert "organization_id" not in User.__table__.columns


def test_membership_relationships_can_be_built() -> None:
    organization = Organization(name="Loja Exemplo", slug="loja-exemplo")
    user = User(email="user@example.com", name="Usuário Exemplo")
    membership = OrganizationUser(
        organization=organization,
        user=user,
        role=OrganizationRole.OWNER,
    )

    assert organization.memberships == [membership]
    assert user.memberships == [membership]
    assert membership.organization is organization
    assert membership.user is user


def test_model_defaults_and_database_constraints() -> None:
    membership_table = OrganizationUser.__table__
    role_column = membership_table.c.role
    foreign_keys = {
        foreign_key.parent.name: foreign_key
        for foreign_key in membership_table.foreign_keys
    }

    assert membership_table.primary_key.columns.keys() == [
        "organization_id",
        "user_id",
    ]
    assert foreign_keys["organization_id"].ondelete == "CASCADE"
    assert foreign_keys["user_id"].ondelete == "CASCADE"
    assert isinstance(role_column.type, Enum)
    assert role_column.type.native_enum is False
    assert role_column.type.create_constraint is False
    assert role_column.type.enums == ["owner", "member"]
    assert {
        constraint.name for constraint in membership_table.constraints
    } >= {"ck_organization_users_organization_role"}
    assert role_column.default.arg is OrganizationRole.MEMBER
    assert User.__table__.c.is_active.default.arg is True
    assert Organization.__table__.c.created_at.type.timezone is True
    assert Organization.__table__.c.updated_at.type.timezone is True
    assert User.__table__.c.created_at.type.timezone is True
    assert User.__table__.c.updated_at.type.timezone is True
