"""Initial migration

Revision ID: 700b98982143
Revises: 
Create Date: 2025-02-21 01:18:10.497376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '700b98982143'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create items table
    op.create_table('items',
        sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('description', sa.TEXT(), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id', name='items_pkey')
    )

    # Create trigger for updating timestamp
    op.execute("""
        CREATE TRIGGER update_items_updated_at
        BEFORE UPDATE ON items
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column()
    """)


def downgrade() -> None:
    # Drop trigger
    op.execute("DROP TRIGGER IF EXISTS update_items_updated_at ON items")
    # Drop table
    op.drop_table('items')
