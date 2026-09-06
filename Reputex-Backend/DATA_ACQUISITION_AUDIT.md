# RepuTex Data Acquisition Audit & Pipeline Gap Analysis

This document provides an exhaustive audit of the RepuTex backend specifically regarding **external data acquisition**, covering our primary data sources:
- **Google** (Google Business Profile, Google Maps Reviews, Places API)
- **Reddit** (Subreddits, discussions, post comments)
- **Twitter / X** (Recent search, brand mentions)
- **Google AI Summaries** (Google Search AI Overviews / SERP synthesis)

*(JustDial is intentionally omitted for now as requested).*

---

## 1. End-to-End Pipeline Trace

Below is the complete trace of the data path as designed versus as currently implemented:

```
[Stage 1: Business Keywords]
  ├── Designed: Active brand, product, location, personnel keywords are pulled per business.
  ├── Current: Stored in DB ('brand_keywords'), but completely ignored by acquisition tasks.
  └── Gap: Ingestion passes an empty list `[]` to connectors. No keyword-to-query translation.

[Stage 2: Scheduled Collection]
  ├── Designed: Celery Beat periodically triggers platform polling (every 15–60 mins) per business.
  ├── Current: Celery Beat is NOT configured. Tasks are only invoked on-demand or during tests.
  └── Gap: No scheduler, no interval definitions, no 'last_polled_at' incremental tracking.

[Stage 3: Source Scrapers / Connectors]
  ├── Google:
  │     ├── Current: Skeleton in 'app/integrations/google.py' checks API key, queries Places API findplacefromtext, ignores output, and returns `[]`.
  │     └── Gap: Places API only returns 5 reviews maximum. Missing Google Business Profile OAuth2 API for verified locations and missing Maps review paginator.
  ├── Reddit:
  │     ├── Current: Skeleton in 'app/integrations/reddit.py' checks credentials and returns `[]`.
  │     └── Gap: No OAuth2 client credentials negotiation, no search against /oauth.reddit.com/search, no comment crawler.
  ├── Twitter / X:
  │     ├── Current: Skeleton in 'app/integrations/twitter.py' checks Bearer token and returns `[]`.
  │     └── Gap: No X API v2 Recent Search client, no author expansions, no rate-limit backoff.
  └── Google AI Summaries:
        ├── Current: 0% — Completely missing.
        └── Gap: No connector, no SERP scraper, no parser for Google AI Overviews, no model or metadata representation.

[Stage 4: Normalization Layer]
  ├── Designed: Raw platform JSON converted into standardized Pydantic domain schemas.
  ├── Current: Only 'MockPlatformConnector' creates pre-baked dictionaries matching Mention fields.
  └── Gap: No typed raw-to-domain transformation schemas. No uniform handling of avatars, URLs, or engagement metrics.

[Stage 5: Deduplication & Idempotent Upsert]
  ├── Designed: Idempotent upsert prevents repeated runs from creating duplicate reviews.
  ├── Current: 'MentionRepository.bulk_create()' runs direct 'db.add_all(mentions)'.
  └── Gap: No unique constraint on '(business_id, platform, external_id)'. Repeated runs duplicate records and skew scoring.

[Stage 6: PostgreSQL Storage]
  ├── Designed: Clean, normalized mentions with raw JSON metadata archived.
  ├── Current: 'mentions' table exists and functions.
  └── Gap: Missing deduplication unique constraint/indexes. Missing first-class AI Overview entity.

[Stage 7: Sentiment / Fraud / Crisis Processing]
  ├── Designed: Inserting new mentions triggers an automated Celery canvas chain.
  ├── Current: Services exist, but are only invoked on-demand via REST endpoints.
  └── Gap: Ingested mentions bypass sentiment NLP, fraud heuristic analysis, and crisis checks.

[Stage 8: Reputation Score Recalculation & Alert Dispatch]
  ├── Designed: New mentions trigger incremental score recalculation and anomaly alerts.
  ├── Current: Scoring formula is isolated in 'reputation_service.py', but only runs on-demand.
  └── Gap: No automatic recalculation hook upon new review ingestion.

[Stage 9: Flutter Mobile Application]
  ├── Designed: RealApiService reads live PostgreSQL data via REST endpoints.
  ├── Current: Tested and working.
  └── Ready: Seamlessly renders live data as soon as the upstream pipeline updates PostgreSQL.
```

---

## 2. Component Status Matrix

| Component | Status | Classification | Key Missing Capabilities |
| :--- | :--- | :--- | :--- |
| `BrandKeyword` query engine | Disconnected | **Simulated** | Does not generate platform-specific search syntax from keywords. |
| Celery Beat Scheduler | Not configured | **Missing** | No periodic cron/interval worker defined in `celery_app.py` or `docker-compose.yml`. |
| Incremental Polling Tracker | Not configured | **Missing** | No `PlatformConnection` table tracking `last_polled_at`, rate limits, or credentials. |
| Google Connector | Skeletonized | **Skeleton** | Returns `[]`. Places API limited to 5 reviews; lacks Google Business Profile OAuth2 and Maps review paginator. |
| Reddit Connector | Skeletonized | **Skeleton** | Returns `[]`. Lacks OAuth2 client credentials flow, search API, and comment extraction. |
| Twitter / X Connector | Skeletonized | **Skeleton** | Returns `[]`. Lacks X API v2 Recent Search client, query builder, and author expansions. |
| Google AI Overview Scraper | Non-existent | **Missing (0%)** | Zero code. Lacks SERP search execution, AI Overview container extraction, and cited source tracking. |
| Ingestion Normalizer | Ad-hoc | **Mocked** | No typed raw-to-domain validation pipeline. Relies on mock dictionary structures. |
| Deduplication Engine | Non-existent | **Missing** | No `UniqueConstraint(business_id, platform, external_id)`. `bulk_create` blindly inserts duplicates. |
| Intelligence Pipeline Hook | Disconnected | **Missing** | Ingestion does not trigger Celery canvas chain for sentiment, fraud, crisis, and score updates. |

---

## 3. Implementation Blueprint Summary

To transition from the current mock/skeleton state to the production acquisition pipeline, the following 4 phases are planned:

1. **Phase 1: Ingestion Infrastructure & Deduplication Engine**
   - Add database unique constraint on `(business_id, platform, external_id)`.
   - Implement `upsert_mentions()` in `MentionRepository` with `ON CONFLICT DO UPDATE`.
   - Create `PlatformConnection` model to persist per-platform credentials and `last_polled_at`.
   - Configure Celery Beat periodic scheduler in `celery_app.py` and `docker-compose.yml`.

2. **Phase 2: Core Connectors (Google & Reddit)**
   - Build keyword-to-query translation utility (`query_builder.py`).
   - Implement Google Business Profile API & Google Maps reviews paginator in `app/integrations/google.py`.
   - Implement Reddit OAuth2 Search client and comment ingestion in `app/integrations/reddit.py`.

3. **Phase 3: Twitter/X & Google AI Summaries Scraper**
   - Implement X API v2 Recent Search client with author expansions in `app/integrations/twitter.py`.
   - Implement `GoogleAIOverviewConnector` in `app/integrations/google_ai_overview.py` to extract SERP AI Overviews, synthesized claims, and cited web URLs.

4. **Phase 4: Automated Intelligence Event Chain & E2E Validation**
   - Build Celery canvas workflow: `fetch -> upsert -> sentiment -> fraud -> crisis -> reputation -> alerts`.
   - Add pipeline monitoring and health status API endpoint (`GET /api/v1/integrations/status`).
   - Verify live data ingestion displaying seamlessly in the Flutter mobile application.
