# Legacy AI Content Catalog

This module provides a shared metadata catalog for previously generated AI content that should remain retrievable by the current JAN AI system and optionally prepared for the built-in model training pipeline.

## What is stored

- Images
- Videos
- Audio
- Text
- Other generated assets
- Original prompt/model/provider metadata
- Training eligibility and training lifecycle status

The catalog stores metadata and references such as source URLs and local paths. Large binary files should stay in durable object/file storage rather than in Git.

## Database

The module creates a SQLite database at `data/legacy_content.db` by default. Set `LEGACY_CONTENT_DB` to use another path.

## Usage

```python
from backend.legacy_content_catalog import ContentAsset, initialize, retrieve_assets, upsert_asset

initialize()

upsert_asset(ContentAsset(
    id=None,
    external_id="old-provider-asset-001",
    asset_type="image",
    title="Legacy campaign image",
    description="Imported from the previous generation database",
    prompt="Original generation prompt",
    provider="old-provider",
    model="legacy-model",
    source_url="https://example.com/asset.png",
    local_path="/mnt/assets/asset.png",
    thumbnail_path=None,
    mime_type="image/png",
    metadata_json='{"source":"legacy-db"}',
    created_at="2026-01-15T10:30:00Z",
    training_eligible=True,
    training_status="pending",
))

assets = retrieve_assets(
    asset_type="image",
    query="campaign",
    training_eligible=True,
    training_status="pending",
)
```

## Migration principle

The old database can be imported into this catalog using `external_id` as the stable idempotent key. Re-running the migration updates existing rows instead of creating duplicate records.

## Training workflow

1. Import historical generated content.
2. Review metadata, prompts, and source references.
3. Mark suitable assets as `training_eligible`.
4. Export/prepare only eligible records for the model-training pipeline.
5. Update `training_status` as records move through preparation, training, evaluation, or exclusion.

This keeps the historical content store and the model-training process loosely coupled: the database is the source of truth for provenance and eligibility, while the actual model artifacts remain outside Git.
