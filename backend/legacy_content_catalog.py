"""Legacy AI-generated content catalog.

Stores metadata for previously generated images, videos, audio, and text without
checking large binary assets into Git. The catalog is provider-agnostic so old
generated content can be restored into the current JAN AI flow and selected as
training material for the built-in model pipeline.

The SQLite database path can be overridden with LEGACY_CONTENT_DB. For shared
production use, keep the database in durable storage and point this module at it.
"""

from __future__ import annotations

import os
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

DB_PATH = Path(os.getenv("LEGACY_CONTENT_DB", "data/legacy_content.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS content_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    external_id TEXT UNIQUE,
    asset_type TEXT NOT NULL CHECK(asset_type IN ('image', 'video', 'audio', 'text', 'other')),
    title TEXT,
    description TEXT,
    prompt TEXT,
    provider TEXT,
    model TEXT,
    source_url TEXT,
    local_path TEXT,
    thumbnail_path TEXT,
    mime_type TEXT,
    metadata_json TEXT,
    created_at TEXT NOT NULL,
    imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    training_eligible INTEGER NOT NULL DEFAULT 0 CHECK(training_eligible IN (0, 1)),
    training_status TEXT NOT NULL DEFAULT 'pending',
    training_notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_content_assets_type
    ON content_assets(asset_type);
CREATE INDEX IF NOT EXISTS idx_content_assets_provider_model
    ON content_assets(provider, model);
CREATE INDEX IF NOT EXISTS idx_content_assets_created_at
    ON content_assets(created_at);
CREATE INDEX IF NOT EXISTS idx_content_assets_source_url
    ON content_assets(source_url);
CREATE INDEX IF NOT EXISTS idx_content_assets_training
    ON content_assets(training_eligible, training_status);
"""


@dataclass(slots=True)
class ContentAsset:
    id: Optional[int]
    external_id: Optional[str]
    asset_type: str
    title: Optional[str]
    description: Optional[str]
    prompt: Optional[str]
    provider: Optional[str]
    model: Optional[str]
    source_url: Optional[str]
    local_path: Optional[str]
    thumbnail_path: Optional[str]
    mime_type: Optional[str]
    metadata_json: Optional[str]
    created_at: str
    training_eligible: bool = False
    training_status: str = "pending"
    training_notes: Optional[str] = None


def connect(db_path: Path | str = DB_PATH) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def initialize(db_path: Path | str = DB_PATH) -> None:
    """Create the shared legacy-content schema when it does not exist."""
    with closing(connect(db_path)) as conn:
        conn.executescript(SCHEMA)
        # Make the module safe for databases created by the first PR revision.
        columns = {row[1] for row in conn.execute("PRAGMA table_info(content_assets)")}
        migrations = {
            "training_eligible": "ALTER TABLE content_assets ADD COLUMN training_eligible INTEGER NOT NULL DEFAULT 0 CHECK(training_eligible IN (0, 1))",
            "training_status": "ALTER TABLE content_assets ADD COLUMN training_status TEXT NOT NULL DEFAULT 'pending'",
            "training_notes": "ALTER TABLE content_assets ADD COLUMN training_notes TEXT",
        }
        for name, statement in migrations.items():
            if name not in columns:
                conn.execute(statement)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_content_assets_training ON content_assets(training_eligible, training_status)")
        conn.commit()


def upsert_asset(asset: ContentAsset, db_path: Path | str = DB_PATH) -> int:
    """Insert or update an asset using external_id as the stable import key."""
    initialize(db_path)
    if not asset.external_id:
        raise ValueError("external_id is required for shared catalog upserts")

    sql = """
    INSERT INTO content_assets (
        external_id, asset_type, title, description, prompt, provider, model,
        source_url, local_path, thumbnail_path, mime_type, metadata_json, created_at,
        training_eligible, training_status, training_notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(external_id) DO UPDATE SET
        asset_type=excluded.asset_type,
        title=excluded.title,
        description=excluded.description,
        prompt=excluded.prompt,
        provider=excluded.provider,
        model=excluded.model,
        source_url=excluded.source_url,
        local_path=excluded.local_path,
        thumbnail_path=excluded.thumbnail_path,
        mime_type=excluded.mime_type,
        metadata_json=excluded.metadata_json,
        created_at=excluded.created_at,
        training_eligible=excluded.training_eligible,
        training_status=excluded.training_status,
        training_notes=excluded.training_notes,
        updated_at=CURRENT_TIMESTAMP
    RETURNING id
    """

    values = (
        asset.external_id,
        asset.asset_type,
        asset.title,
        asset.description,
        asset.prompt,
        asset.provider,
        asset.model,
        asset.source_url,
        asset.local_path,
        asset.thumbnail_path,
        asset.mime_type,
        asset.metadata_json,
        asset.created_at,
        int(asset.training_eligible),
        asset.training_status,
        asset.training_notes,
    )

    with closing(connect(db_path)) as conn:
        row = conn.execute(sql, values).fetchone()
        conn.commit()
        return int(row["id"])


def retrieve_assets(
    asset_type: Optional[str] = None,
    provider: Optional[str] = None,
    query: Optional[str] = None,
    training_eligible: Optional[bool] = None,
    training_status: Optional[str] = None,
    limit: int = 100,
    db_path: Path | str = DB_PATH,
) -> list[dict]:
    """Retrieve legacy assets for reuse or model-training preparation."""
    initialize(db_path)
    if limit < 1 or limit > 1000:
        raise ValueError("limit must be between 1 and 1000")

    clauses: list[str] = []
    values: list[object] = []

    if asset_type:
        clauses.append("asset_type = ?")
        values.append(asset_type)
    if provider:
        clauses.append("provider = ?")
        values.append(provider)
    if query:
        clauses.append("(title LIKE ? OR description LIKE ? OR prompt LIKE ?)")
        needle = f"%{query}%"
        values.extend([needle, needle, needle])
    if training_eligible is not None:
        clauses.append("training_eligible = ?")
        values.append(int(training_eligible))
    if training_status:
        clauses.append("training_status = ?")
        values.append(training_status)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    sql = f"""
        SELECT id, external_id, asset_type, title, description, prompt,
               provider, model, source_url, local_path, thumbnail_path,
               mime_type, metadata_json, created_at, imported_at, updated_at,
               training_eligible, training_status, training_notes
        FROM content_assets
        {where}
        ORDER BY created_at DESC, id DESC
        LIMIT ?
    """
    values.append(limit)

    with closing(connect(db_path)) as conn:
        return [dict(row) for row in conn.execute(sql, values).fetchall()]


def mark_training_status(
    external_id: str,
    status: str,
    notes: Optional[str] = None,
    db_path: Path | str = DB_PATH,
) -> None:
    """Update the training lifecycle for an imported asset."""
    initialize(db_path)
    with closing(connect(db_path)) as conn:
        result = conn.execute(
            """UPDATE content_assets
               SET training_status = ?, training_notes = ?, updated_at = CURRENT_TIMESTAMP
               WHERE external_id = ?""",
            (status, notes, external_id),
        )
        if result.rowcount == 0:
            raise KeyError(f"Unknown external_id: {external_id}")
        conn.commit()


def import_assets(
    assets: Iterable[ContentAsset],
    db_path: Path | str = DB_PATH,
) -> int:
    """Bulk-import old generated assets and return the number processed."""
    count = 0
    for asset in assets:
        upsert_asset(asset, db_path)
        count += 1
    return count


if __name__ == "__main__":
    initialize()
    print(f"Legacy content catalog ready: {DB_PATH}")
