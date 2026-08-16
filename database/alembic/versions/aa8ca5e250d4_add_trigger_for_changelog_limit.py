"""add trigger for changelog limit

Revision ID: aa8ca5e250d4
Revises: 700a92e2a264
Create Date: 2026-08-14 18:50:21.466964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa8ca5e250d4'
down_revision: Union[str, Sequence[str], None] = '700a92e2a264'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE OR REPLACE FUNCTION enforce_changelog_limit()
        RETURNS TRIGGER AS $$
        BEGIN
            DELETE FROM changelog
            WHERE id IN (
                SELECT id FROM changelog
                ORDER BY created_at DESC
                OFFSET 100
            );
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER trigger_enforce_changelog_limit
        AFTER INSERT ON changelog
        FOR EACH STATEMENT
        EXECUTE FUNCTION enforce_changelog_limit();
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trigger_enforce_changelog_limit ON changelog;")
    op.execute("DROP FUNCTION IF EXISTS enforce_changelog_limit();")
