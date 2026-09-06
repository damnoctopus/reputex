# RepuTex Architecture Documentation

## 1. System Architecture Diagram

```text
                    Flutter Mobile App (Unchanged)
                                 │
                                 ▼
                         FastAPI API Layer
                     (/api/... & /api/v1/...)
                                 │
             ┌───────────────────┴───────────────────┐
             │                                       │
       API Services                            Scan Service
  (Dashboard, Mentions,                   (State Machine: PENDING →
  Issues, Findings, etc.)                ACQUIRING → ANALYZING →
             │                           AGGREGATING → COMPLETED)
             │                                       │
             │                         ┌─────────────┴─────────────┐
             │                         ▼                           ▼
             │                  Acquisition Layer             Gemini AI
             │               (Google Search Grounding      (Batched Semantic
             │                  or Offline Mock)              Intelligence)
             │                         │                           │
             │                         └─────────────┬─────────────┘
             │                                       ▼
             │                         Normalization & Deduplication
             │                           (SHA-256 Content Hash &
             │                            Unique External IDs)
             │                                       │
             └───────────────────────►           PostgreSQL
                                                     │
                       ┌─────────────────────────────┼────────────────────────────┐
                       ▼                             ▼                            ▼
                 Customer Issues               Authenticity                  Crisis Risk
             (Semantic Clustering &          (Multi-Signal              (Deterministic Time-Series:
             Cross-Platform Breakdown)      Suspicion Scoring)           N_t, ΔS_t, Velocity, G_t)
                       │                             │                            │
                       └─────────────────────────────┼────────────────────────────┘
                                                     ▼
                                          Traceable Findings
                                          & Evidence Quotes
                                                     │
                                                     ▼
                                             Flutter Dashboard
```

---

## 2. Key Architectural Decisions

### A. Acquisition Strategy & Cost Control
- **Gemini Google Search Grounding**: Uses Gemini's native `google_search` tool for web discovery rather than operating complex custom scrapers.
- **Bounded Queries**: Runs 3–4 targeted searches per scan (`"{business}" reviews`, `"{business}" complaints`, `"{business}" site:reddit.com`, `"{business}" (site:x.com OR site:twitter.com)`).
- **Search-Level Caching**: Caches search query results by `(business_id, query, date_window)` to prevent repeated requests on frequent rescans.
- **Incremental Discovery**: Discards known external IDs and content hashes, saving only new observations to steadily grow the business timeline.

### B. Gemini Semantic Understanding Layer
- **Batched Analysis**: Mentions are processed in chunks of 5–10, issuing a single structured prompt returning a `GeminiBatchMentionAnalysis` payload.
- **Structured Pydantic Validation**: Guarantees typed fields for sentiment label, sentiment score (-1.0 to 1.0), intent, categorized issues with verbatim excerpts, aspects, and linguistic signals.

### C. Deterministic Time-Series Analytics
To ensure reproducibility and reliability, mathematical calculations are performed strictly in Python/SQL:
1. **Negative Ratio**: $N_t = \frac{\text{negative mentions}}{\text{total mentions}}$
2. **Sentiment Deterioration**: $\Delta S_t = S_t - S_{t-k}$
3. **Complaint Velocity**: Negative mentions per day.
4. **Engagement Growth**: $G_t = \frac{E_t - E_{t-k}}{\max(E_{t-k}, 1)}$

### D. Evidence-Based Review Authenticity
- Uses legally defensible, non-defamatory classifications: `Potentially Suspicious`, `Likely Suspicious`, `High Suspicion`, `Review Manipulation Risk`.
- Combines Gemini linguistic markers (`templated_language`, `excessive_superlatives`) with deterministic temporal bursts, duplicate text, and polarized rating inversions.

### E. Isolated Research Module
- The `research/` directory (`feature_engineering.py`, `baselines.py`, `crisis_model.py`, `evaluation.py`, `explainability.py`) remains completely decoupled from production runtime services.
