"""Add cascade messages deletion

Revision ID: 4ab8fe1cd3e2
Revises: 47df7be8c795
Create Date: 2025-04-16 12:34:04.250131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ab8fe1cd3e2'
down_revision: Union[str, None] = '47df7be8c795'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('messages_chat_id_fkey', 'messages', type_='foreignkey')

    op.create_foreign_key(
        'messages_chat_id_fkey',
        source_table='messages',
        referent_table='chats',
        local_cols=['chat_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('messages_chat_id_fkey', 'messages', type_='foreignkey')

    op.create_foreign_key(
        'messages_chat_id_fkey',
        source_table='messages',
        referent_table='chats',
        local_cols=['chat_id'],
        remote_cols=['id']
    )
