"""Legacy schema baseline.

For an existing pre-Alembic database, back it up and verify it matches this
revision before running `alembic stamp 0001` then `alembic upgrade head`.
Fresh databases should run `alembic upgrade head` directly; never stamp them.
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(50)), sa.Column('email', sa.String(100)),
        sa.Column('hashed_password', sa.String(255)), sa.Column('is_active', sa.Integer()),
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_table('submissions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(50), nullable=False),
        sa.Column('code_snippet', sa.Text(), nullable=False),
        sa.Column('language', sa.String(20), nullable=False),
        sa.Column('summary', sa.String(2000)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_submissions_id', 'submissions', ['id'])
    op.create_index('ix_submissions_user_id', 'submissions', ['user_id'])
    op.create_table('weaknesses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('submission_id', sa.Integer(), sa.ForeignKey('submissions.id')),
        sa.Column('user_id', sa.String(50), nullable=False),
        sa.Column('type', sa.String(100)), sa.Column('line', sa.Integer()),
        sa.Column('explanation', sa.Text()),
    )
    op.create_index('ix_weaknesses_id', 'weaknesses', ['id'])
    op.create_index('ix_weaknesses_user_id', 'weaknesses', ['user_id'])
    op.create_index('ix_weaknesses_type', 'weaknesses', ['type'])


def downgrade():
    op.drop_table('weaknesses')
    op.drop_table('submissions')
    op.drop_table('users')
