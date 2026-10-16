"""Bind submissions to users, remove redundant weakness ownership, enforce categories.

Preflight rejects orphaned/inconsistent legacy data before DDL. Resolve such
rows explicitly after a backup, then retry. MySQL DDL is not transactional;
backups are required and a failed DDL step needs inspection before retrying.
"""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

# Frozen migration contract; do not import mutable application enums.
CATEGORIES = (
    'SyntaxError', 'IndentationError', 'TypeError', 'ImportError', 'NameError',
    'LogicError', 'InfiniteLoop', 'BoundaryError', 'NullSafety', 'DataStructureMisuse',
    'Efficiency', 'RedundantCode', 'NamingConvention', 'Security', 'Documentation', 'Other',
)
NAMING = {'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s'}


def upgrade():
    conn = op.get_bind()
    checks = [
        'SELECT COUNT(*) FROM users WHERE username IS NULL OR email IS NULL OR hashed_password IS NULL OR is_active IS NULL',
        'SELECT COUNT(*) FROM submissions s LEFT JOIN users u ON s.user_id = u.username WHERE u.id IS NULL',
        'SELECT COUNT(*) FROM weaknesses w LEFT JOIN submissions s ON w.submission_id = s.id WHERE s.id IS NULL OR w.user_id <> s.user_id OR w.explanation IS NULL',
    ]
    if any(conn.scalar(sa.text(query)) for query in checks):
        raise RuntimeError('Legacy data contains null, orphaned, or inconsistent ownership; resolve before migration.')
    invalid = conn.scalar(sa.text(
        'SELECT COUNT(*) FROM weaknesses WHERE type IS NULL OR type NOT IN :categories'
    ).bindparams(sa.bindparam('categories', expanding=True)), {'categories': CATEGORIES})
    if invalid:
        raise RuntimeError('Legacy data contains unknown error categories; resolve before migration.')

    with op.batch_alter_table('users') as batch:
        for name, type_ in [('username', sa.String(50)), ('email', sa.String(100)), ('hashed_password', sa.String(255)), ('is_active', sa.Integer)]:
            batch.alter_column(name, existing_type=type_, nullable=False)
    op.add_column('submissions', sa.Column('owner_id', sa.Integer(), nullable=True))
    conn.execute(sa.text('UPDATE submissions SET owner_id = (SELECT users.id FROM users WHERE users.username = submissions.user_id)'))
    with op.batch_alter_table('submissions') as batch:
        batch.drop_index('ix_submissions_user_id')
        batch.drop_column('user_id')
        batch.alter_column('owner_id', existing_type=sa.Integer(), nullable=False)
        batch.create_index('ix_submissions_owner_id', ['owner_id'])
        batch.create_foreign_key('fk_submissions_owner_id_users', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    foreign_keys = sa.inspect(conn).get_foreign_keys('weaknesses')
    with op.batch_alter_table('weaknesses', naming_convention=NAMING) as batch:
        for fk in foreign_keys:
            batch.drop_constraint(fk['name'] or 'fk_weaknesses_submission_id_submissions', type_='foreignkey')
        batch.drop_index('ix_weaknesses_user_id')
        batch.drop_column('user_id')
        batch.alter_column('submission_id', existing_type=sa.Integer(), nullable=False)
        batch.alter_column('type', existing_type=sa.String(100), nullable=False)
        batch.alter_column('explanation', existing_type=sa.Text(), nullable=False)
        batch.create_foreign_key('fk_weaknesses_submission_id_submissions', 'submissions', ['submission_id'], ['id'], ondelete='CASCADE')
        batch.create_check_constraint('error_type', 'type IN (' + ', '.join(repr(c) for c in CATEGORIES) + ')')


def downgrade():
    conn = op.get_bind()
    op.add_column('submissions', sa.Column('user_id', sa.String(50), nullable=True))
    conn.execute(sa.text('UPDATE submissions SET user_id = (SELECT username FROM users WHERE users.id = submissions.owner_id)'))
    op.add_column('weaknesses', sa.Column('user_id', sa.String(50), nullable=True))
    conn.execute(sa.text('UPDATE weaknesses SET user_id = (SELECT user_id FROM submissions WHERE submissions.id = weaknesses.submission_id)'))
    with op.batch_alter_table('weaknesses') as batch:
        batch.drop_constraint('error_type', type_='check')
        batch.drop_constraint('fk_weaknesses_submission_id_submissions', type_='foreignkey')
        batch.create_foreign_key('fk_weaknesses_submission_id_submissions', 'submissions', ['submission_id'], ['id'])
        batch.alter_column('user_id', existing_type=sa.String(50), nullable=False)
        batch.create_index('ix_weaknesses_user_id', ['user_id'])
        for name, type_ in [('submission_id', sa.Integer), ('type', sa.String(100)), ('explanation', sa.Text)]:
            batch.alter_column(name, existing_type=type_, nullable=True)
    with op.batch_alter_table('submissions') as batch:
        batch.drop_constraint('fk_submissions_owner_id_users', type_='foreignkey')
        batch.drop_index('ix_submissions_owner_id')
        batch.drop_column('owner_id')
        batch.alter_column('user_id', existing_type=sa.String(50), nullable=False)
        batch.create_index('ix_submissions_user_id', ['user_id'])
    with op.batch_alter_table('users') as batch:
        for name, type_ in [('username', sa.String(50)), ('email', sa.String(100)), ('hashed_password', sa.String(255)), ('is_active', sa.Integer)]:
            batch.alter_column(name, existing_type=type_, nullable=True)
