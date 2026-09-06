"""phase_3_issues_and_findings

Revision ID: b4c3d2e1f0a9
Revises: a3f2b1c4e5d6
Create Date: 2026-09-06 23:15:00.000000+00:00

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b4c3d2e1f0a9"
down_revision: Union[str, Sequence[str], None] = "a3f2b1c4e5d6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "issues",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("business_id", sa.String(length=64), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("subtopic", sa.String(length=128), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("mention_count", sa.Integer(), nullable=False),
        sa.Column("platforms_breakdown", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("sentiment_breakdown", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_issues_business_id"), "issues", ["business_id"], unique=False)
    op.create_index(op.f("ix_issues_category"), "issues", ["category"], unique=False)
    op.create_index(op.f("ix_issues_severity"), "issues", ["severity"], unique=False)
    op.create_index(op.f("ix_issues_status"), "issues", ["status"], unique=False)

    op.create_table(
        "issue_mentions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("issue_id", sa.String(length=64), nullable=False),
        sa.Column("mention_id", sa.String(length=64), nullable=False),
        sa.Column("relevance_score", sa.Float(), nullable=False),
        sa.Column("excerpt", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["issue_id"], ["issues.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["mention_id"], ["mentions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_issue_mentions_issue_id"), "issue_mentions", ["issue_id"], unique=False)
    op.create_index(op.f("ix_issue_mentions_mention_id"), "issue_mentions", ["mention_id"], unique=False)

    op.create_table(
        "findings",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("business_id", sa.String(length=64), nullable=False),
        sa.Column("finding_type", sa.String(length=32), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_findings_business_id"), "findings", ["business_id"], unique=False)
    op.create_index(op.f("ix_findings_finding_type"), "findings", ["finding_type"], unique=False)
    op.create_index(op.f("ix_findings_severity"), "findings", ["severity"], unique=False)

    op.create_table(
        "finding_evidence",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("finding_id", sa.String(length=64), nullable=False),
        sa.Column("mention_id", sa.String(length=64), nullable=False),
        sa.Column("evidence_type", sa.String(length=32), nullable=False),
        sa.Column("snippet", sa.Text(), nullable=True),
        sa.Column("relevance_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["finding_id"], ["findings.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["mention_id"], ["mentions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_finding_evidence_finding_id"), "finding_evidence", ["finding_id"], unique=False)
    op.create_index(op.f("ix_finding_evidence_mention_id"), "finding_evidence", ["mention_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_finding_evidence_mention_id"), table_name="finding_evidence")
    op.drop_index(op.f("ix_finding_evidence_finding_id"), table_name="finding_evidence")
    op.drop_table("finding_evidence")

    op.drop_index(op.f("ix_findings_severity"), table_name="findings")
    op.drop_index(op.f("ix_findings_finding_type"), table_name="findings")
    op.drop_index(op.f("ix_findings_business_id"), table_name="findings")
    op.drop_table("findings")

    op.drop_index(op.f("ix_issue_mentions_mention_id"), table_name="issue_mentions")
    op.drop_index(op.f("ix_issue_mentions_issue_id"), table_name="issue_mentions")
    op.drop_table("issue_mentions")

    op.drop_index(op.f("ix_issues_status"), table_name="issues")
    op.drop_index(op.f("ix_issues_severity"), table_name="issues")
    op.drop_index(op.f("ix_issues_category"), table_name="issues")
    op.drop_index(op.f("ix_issues_business_id"), table_name="issues")
    op.drop_table("issues")
