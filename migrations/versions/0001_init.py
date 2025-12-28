"""initial schema

Revision ID: 0001
Revises: 
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'files',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('sha256', sa.String(length=64), unique=True, nullable=False),
        sa.Column('size_bytes', sa.Integer(), nullable=False),
        sa.Column('mime_type', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        'model_versions',
        sa.Column('version', sa.String(length=50), primary_key=True),
        sa.Column('algo', sa.String(length=50), nullable=False),
        sa.Column('metrics', postgresql.JSONB(), nullable=True),
        sa.Column('path', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('false')),
    )
    op.create_table(
        'datasets',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('source_url', sa.Text(), nullable=False),
        sa.Column('license_note', sa.Text(), nullable=True),
        sa.Column('samples_count', sa.Integer(), nullable=True),
        sa.Column('meta', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        'scans',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('file_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('files.id')),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('predicted_class', sa.String(length=50), nullable=True),
        sa.Column('probabilities', postgresql.JSONB(), nullable=True),
        sa.Column('explain', postgresql.JSONB(), nullable=True),
        sa.Column('model_version', sa.String(length=50), nullable=True),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('scans')
    op.drop_table('datasets')
    op.drop_table('model_versions')
    op.drop_table('files')
