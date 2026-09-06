# RepuTex Data Acquisition & Ingestion Architecture

This document specifies the technical architecture, data contracts, normalization pipelines, deduplication engine, and asynchronous scheduling infrastructure implemented in **Phase 1 — Ingestion Infrastructure & Deduplication Engine**.

---

## 1. End-to-End Ingestion Lifecycle

The acquisition pipeline coordinates how external brand sentiment and customer feedback are discovered, ingested, normalized, stored, and handed off for machine learning intelligence processing:

```
+------------------------+
| Active Brand Keywords  |
| (PostgreSQL Database)  |
+-----------+------------+
            |
            v
+------------------------+      +--------------------------+
|  PlatformQueryBuilder  | ---> | Tailored Platform Search |
| (Deterministic Syntax) |      | Queries (Google, Reddit) |
+-----------+------------+      +--------------------------+
            |
            v
+------------------------+      +--------------------------+
|   PlatformConnector    | ---> |   RawMentionRecord[]     |
| (Scrapers / Permitted) |      | (Unmodified Source Feeds)|
+-----------+------------+      +--------------------------+
            |
            v
+------------------------+      +--------------------------+
|   MentionNormalizer    | ---> |   NormalizedMention[]    |
| (Whitespace/UTC/URLs)  |      | (Deterministic Ext-IDs)  |
+-----------+------------+      +--------------------------+
            |
            v
+----------------------------------------------------------+
|                   Deduplication Engine                   |
| 1. In-Batch Filter (Unique Key & Content SHA-256 Hash)   |
| 2. PostgreSQL Atomic Upsert (ON CONFLICT DO UPDATE)     |
|    Constraint: (business_id, platform, external_id)      |
+---------------------------+------------------------------+
                            |
            +---------------+---------------+
            |                               |
            v                               v
+-----------------------+       +--------------------------+
|  PlatformConnection   |       |       IngestionJob       |
| (Incremental Polling) |       | (Audit Trail & Telemetry)|
+-----------------------+       +--------------------------+
            |
            v (if new records inserted)
+----------------------------------------------------------+
|             Downstream Intelligence Pipeline             |
| tasks.pipeline_process_mentions(business_id, mention_ids)|
| -> Sentiment Analysis -> Fraud Detection -> Crisis Event  |
| -> Reputation Score Recalculation                        |
+----------------------------------------------------------+
```

---

## 2. Ingestion Domain Contracts

### Connector Interface (`PlatformConnector`)
Located in [`app/integrations/base.py`](file:///c:/Users/adira/Projects/Reputex/backend/app/integrations/base.py). All external adapters (Google, Reddit, X, Mock) implement this interface:

```python
class PlatformConnector(ABC):
    platform_name: str

    @abstractmethod
    async def fetch_mentions(
        self,
        business_name: str,
        keywords: list[str],
        since: datetime | None = None,
        cursor: str | None = None,
        location: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch brand mentions and social discussions."""
        pass

    @abstractmethod
    async def fetch_reviews(
        self,
        business_identifier: str,
        since: datetime | None = None,
        cursor: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch customer ratings and reviews."""
        pass

    @abstractmethod
    async def publish_response(
        self,
        external_mention_id: str,
        response_text: str,
    ) -> bool:
        """Publish an approved business response back to external source."""
        pass
```

---

## 3. Platform Query Builder

Located in [`app/integrations/query_builder.py`](file:///c:/Users/adira/Projects/Reputex/backend/app/integrations/query_builder.py).

The query builder accepts a `Business`, its aliases, and active `BrandKeyword` tokens, producing deterministic, platform-syntax compliant search queries:

| Platform | Query Syntax Example | Characteristics |
| :--- | :--- | :--- |
| **Google** | `"Spice Symphony" Indiranagar, Bangalore biryani "fine dining"` | Brand in quotes + location + product keywords |
| **Reddit** | `("Spice Symphony" OR "mutton biryani" OR SpiceSymphonyBlr)` | Boolean OR grouping, subreddit suggestion filters |
| **X / Twitter** | `("Spice Symphony" OR "best food") -is:retweet lang:en` | API v2 syntax: exclusion of retweets and language filtering |
| **Google AI Overview** | `"Spice Symphony" in Indiranagar customer reviews and reputation` | Natural query phrase triggering generative review summaries |

---

## 4. Raw Ingestion Models

Located in [`app/schemas/ingestion.py`](file:///c:/Users/adira/Projects/Reputex/backend/app/schemas/ingestion.py):

* **`RawMentionRecord`**: Immutable Pydantic model representing external payloads before database ingestion. Contains `platform`, `external_id`, `source_url`, `title`, `content`, `author`, `author_id`, `author_avatar`, `published_at`, `collected_at`, `rating`, `engagement`, `metadata`, and `raw_payload`.
* Scrapers **never** instantiate SQLAlchemy `Mention` ORM models directly.

---

## 5. Normalization Pipeline

Located in [`app/services/normalizer.py`](file:///c:/Users/adira/Projects/Reputex/backend/app/services/normalizer.py):

1. **Whitespace & Control Chars**: Strips null bytes (`\x00`), non-printable ASCII control characters, collapses excess line breaks (`\n{3,}` -> `\n\n`), and trims each line.
2. **Content Hash**: Generates deterministic SHA-256 hash of cleaned text for cross-platform content duplicate detection.
3. **Deterministic Fallback External IDs**: If the external source lacks a permanent ID, generates `{platform}_{content_hash[:16]}` ensuring reproducibility.
4. **Timezone Awareness**: Normalizes all timestamps into UTC-aware datetimes.
5. **Rating Clamping**: Standardizes customer review ratings to float range `1.0 <= rating <= 5.0` rounded to 1 decimal place.
6. **Engagement Metrics**: Casts likes, retweets/shares, and comments to non-negative integers.
7. **Platform Name Standardization**: Normalizes aliases (`"google_places"`, `"twitter"`) to standard platform names (`"Google"`, `"X"`, `"Reddit"`).
8. **Batch Fault Tolerance**: `normalize_batch()` isolates individual malformed records into an `errors` list so one bad record never aborts the ingestion of valid records.

---

## 6. Deduplication Engine & Database Constraints

Deduplication occurs at both application and database tiers:

### A. Application-Level Deduplication
Before issuing database operations, `MentionRepository.upsert_mentions()` scans the batch:
* Discards duplicate records within the batch that share the same `(platform, external_id)` or `content_hash`.
* Counts internal batch duplicates as `skipped`.

### B. Database-Level Uniqueness & Native Upsert
* **Constraint**: `uq_business_platform_external` on table `mentions (business_id, platform, external_id)`.
* **Atomic Native Upsert**: Uses PostgreSQL `ON CONFLICT (business_id, platform, external_id) DO UPDATE` (and SQLite `on_conflict_do_update` during local testing).
* When a record is re-fetched:
  * Updates `engagement` metrics with latest counts.
  * Updates `collected_at` timestamp.
  * Coalesces `url` and `author_avatar`.
  * Preserves existing `id`, `business_id`, `sentiment`, `sentiment_score`, `is_fake`, `fraud_confidence`, and user replies.
* **Idempotency Guarantee**: Fetching the same batch 10 times results in **exactly 1 row** in PostgreSQL, with 0 errors and 10 skipped on subsequent runs.

---

## 7. Incremental Polling State

Tracked per tenant and per platform in table `platform_connections` via model `PlatformConnection`:
* `business_id` (ForeignKey)
* `platform`
* `is_active`
* `last_polled_at` & `last_success_at` & `last_attempt_at`
* `records_fetched`, `records_inserted`, `records_skipped`
* `error_count` & `last_error`
* `cursor` (supports pagination / continuation tokens for future cursor-based APIs)
* `rate_limit_reset_at` (enforces exponential backoff when upstream rate limits are encountered)
* `status` (`healthy`, `warning`, `error`)

---

## 8. Celery Beat Periodic Scheduling

* **Configurable Interval**: Configured via `INGESTION_SCHEDULE_INTERVAL_MINUTES` in [`app/core/config.py`](file:///c:/Users/adira/Projects/Reputex/backend/app/core/config.py) (default: 30 minutes).
* **Beat Scheduler Task**: `tasks.schedule_periodic_ingestion` in [`app/workers/tasks.py`](file:///c:/Users/adira/Projects/Reputex/backend/app/workers/tasks.py).
* **Worker Execution Task**: `tasks.ingest_platform_for_business` processes individual (business, platform) pairs concurrently with retry backoff (`max_retries=3`).
* **Containerized Beat**: Container `reputex_beat` declared in [`docker-compose.yml`](file:///c:/Users/adira/Projects/Reputex/backend/docker-compose.yml).

---

## 9. Ingestion Job Tracking & Telemetry

Stored in table `ingestion_jobs` via model `IngestionJob`:
* `id` (`job_{uuid}`)
* `business_id`
* `platform`
* `status` (`PENDING`, `RUNNING`, `SUCCESS`, `PARTIAL`, `FAILED`)
* `started_at` & `completed_at`
* `records_fetched`, `records_normalized`, `records_inserted`, `records_skipped`
* `error_message`
* `retry_count`

---

## 10. Downstream Intelligence Processing Handoff

Upon successful mention insertion (`inserted_count > 0`), the ingestion pipeline asynchronously dispatches:
```python
tasks.pipeline_process_mentions.delay(business_id, new_mention_ids)
```
This task:
1. Executes `SentimentService.analyze_mention()` for sentiment and aspect extraction.
2. Executes `FraudService.get_fraud_analysis()` for fake review probability detection.
3. Executes `ReputationService.recalculate()` to refresh the aggregate business reputation score.
4. Executes `CrisisService.analyze_and_detect()` to check for emerging anomaly volume.

---

## 11. Mock Platform Connector

[`app/integrations/mock_connector.py`](file:///c:/Users/adira/Projects/Reputex/backend/app/integrations/mock_connector.py) exercises the entire pipeline end-to-end without requiring live third-party credentials:
* Invokes `PlatformQueryBuilder.build_query()` to verify query construction.
* Emits high-fidelity `RawMentionRecord` instances across Google, Reddit, X, and JustDial.
* Feeds into `MentionNormalizer` and `MentionRepository.upsert_mentions()` to prove end-to-end deduplication and persistence.

---

## 12. Future Platform Collector Integration Roadmap

### Phase 2 — Google Places & Business Profile
* Target: Permitted Google Places API (`/findplacefromtext`, `/details`) and official Business Profile APIs.
* Connector: `GoogleConnector` in [`app/integrations/google.py`](file:///c:/Users/adira/Projects/Reputex/backend/app/integrations/google.py).
* Returns `RawMentionRecord` with review text, author name, star rating (1.0–5.0), and place ID metadata.

### Phase 3 — Reddit Discussions
* Target: Reddit OAuth2 API (`/search`, `/r/{subreddit}/comments`).
* Connector: `RedditConnector` in [`app/integrations/reddit.py`](file:///c:/Users/adira/Projects/Reputex/backend/app/integrations/reddit.py).
* Returns `RawMentionRecord` with post title, body text, upvotes, comment count, and subreddit metadata.

### Phase 4 — X / Twitter Discussions
* Target: Twitter API v2 Recent Search endpoint (`/2/tweets/search/recent`).
* Connector: `TwitterConnector` in [`app/integrations/twitter.py`](file:///c:/Users/adira/Projects/Reputex/backend/app/integrations/twitter.py).
* Returns `RawMentionRecord` with tweet text, author handle, like/retweet metrics, and conversation ID.

### Phase 5 — Google AI Overview Snapshots
* Dedicated model `GoogleAISnapshot` (separate from `Mention`):
  * `business_id`
  * `query_phrase`
  * `captured_at`
  * `summary_text`
  * `cited_sources` (list of domains and URLs)
  * `content_hash`
  * `metadata`
* Ingestion engine will query AI Overviews on a scheduled cadence to monitor the brand's AI search reputation.
