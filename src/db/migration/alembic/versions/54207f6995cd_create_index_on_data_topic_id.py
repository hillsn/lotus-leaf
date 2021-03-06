"""Create index on data.topic_id.

Revision ID: 54207f6995cd
Revises: 2534585a9391
Create Date: 2017-12-30 14:19:32.156907

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '54207f6995cd'
down_revision = '2534585a9391'
branch_labels = None
depends_on = None


def upgrade():
  """Creates an index on data.topic."""
  op.create_index('topic_id_idx', 'data', ['topic_id'])


def downgrade():
  """Drops the index on data.topic_id."""
  op.drop_index('topic_id_idx', 'data')
