# RepuTex API Contract Specification

This document defines the formal, bidirectional REST API contract between the **FastAPI Backend** and the **RepuTex Flutter Mobile Application**.

---

## 1. Overview & Protocol Conventions

- **Base URL**:
  - Flutter default emulator host: `http://10.0.2.2:8000/api`
  - Real device / Web / Production: `http://<host>:8000/api`
  - API versioned routes: `/api/v1` (with direct route aliasing under `/api` for 100% zero-friction Flutter client compatibility)
- **Protocol**: HTTP/1.1 and HTTP/2 over TLS (HTTPS in production)
- **Content-Type**: `application/json`
- **Accept**: `application/json`
- **Date/Time Format**: ISO 8601 UTC (e.g. `2026-09-05T14:30:00Z`)

---

## 2. Authentication & Authorization Standard

### 2.1 Header Format
Every authenticated request requires the Bearer token in the `Authorization` header:
```http
Authorization: Bearer <access_token>
```

### 2.2 Token Lifecycle
- **Access Token**: Short-lived JWT (default: 60 minutes) containing `sub` (User ID), `business_id`, `role`, and `exp`.
- **Refresh Token**: Long-lived secure token (default: 30 days) stored in Postgres and validated upon rotation.
- **Auto-Refresh**: Flutter's `_AuthInterceptor` in `dio_client.dart` catches `401 Unauthorized`, issues `POST /api/auth/refresh`, updates secure storage, and retries the original request seamlessly.

### 2.3 Roles (RBAC)
- `OWNER`: Full business privileges, member management, billing.
- `ADMIN`: Operational management, keyword editing, AI response dispatching.
- `ANALYST`: View analytics, fraud, crisis, and draft responses.
- `VIEWER`: Read-only access to dashboard and mentions.

---

## 3. Global Error Response Standard

All errors returned by the API adhere to the following schema, ensuring full compatibility with Flutter's `ErrorHandler._extractMessage(data)` which inspects `data['message'] ?? data['detail']`:

```json
{
  "success": false,
  "detail": "Descriptive human-readable error explanation",
  "message": "Descriptive human-readable error explanation",
  "error": {
    "code": "SPECIFIC_ERROR_CODE",
    "message": "Descriptive human-readable error explanation",
    "details": {}
  }
}
```

### Standard HTTP Status Codes:
- `400 Bad Request`: `VALIDATION_ERROR` or malformed request syntax.
- `401 Unauthorized`: `INVALID_CREDENTIALS`, `TOKEN_EXPIRED`, `INVALID_TOKEN`.
- `403 Forbidden`: `ACCESS_DENIED`, `BUSINESS_ACCESS_DENIED` (Tenant isolation breach).
- `404 Not Found`: `RESOURCE_NOT_FOUND`, `BUSINESS_NOT_FOUND`, `MENTION_NOT_FOUND`.
- `409 Conflict`: `EMAIL_ALREADY_EXISTS`, `DUPLICATE_KEYWORD`.
- `422 Unprocessable Entity`: Pydantic schema validation failures.
- `429 Too Many Requests`: Rate limiting threshold reached.
- `500 Internal Server Error`: Centralized exception handler concealing stack traces.

---

## 4. Endpoints Matrix & Detailed Contracts

### 4.1 Authentication Service

#### 4.1.1 Register Account & Business
- **Endpoint**: `POST /api/v1/auth/register` (alias: `POST /api/auth/register`)
- **Authentication**: None
- **Request Body**:
```json
{
  "email": "adira@spicesymphony.com",
  "password": "password123",
  "full_name": "Adithya",
  "business_name": "Spice Symphony",
  "business_category": "Restaurant",
  "phone": "+91 98765 43210"
}
```
- **Response JSON (201 Created)**:
```json
{
  "user": {
    "id": "usr_01J6X7B9C1...",
    "email": "adira@spicesymphony.com",
    "full_name": "Adithya",
    "role": "owner",
    "business_id": "biz_01J6X7B9C2...",
    "is_active": true,
    "created_at": "2026-09-05T14:30:00Z"
  },
  "tokens": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 3600
  }
}
```
- **Flutter Model Consumed**: `AuthResponse` (`lib/features/auth/domain/models/auth_response.dart`)
- **Errors**: `400 Bad Request`, `409 Conflict (EMAIL_ALREADY_EXISTS)`, `422 Validation Error`.

---

#### 4.1.2 Login
- **Endpoint**: `POST /api/v1/auth/login` (alias: `POST /api/auth/login`)
- **Authentication**: None
- **Request Body**:
```json
{
  "email": "adira@spicesymphony.com",
  "password": "password123"
}
```
- **Response JSON (200 OK)**: Same as 4.1.1 `AuthResponse`
- **Flutter Model Consumed**: `AuthResponse`
- **Errors**: `401 Unauthorized (INVALID_CREDENTIALS)`.

---

#### 4.1.3 Refresh Token
- **Endpoint**: `POST /api/v1/auth/refresh` (alias: `POST /api/auth/refresh`)
- **Authentication**: None (Refresh token in body)
- **Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```
- **Response JSON (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```
- **Flutter Model Consumed**: `AuthTokens` (`lib/features/auth/domain/models/auth_tokens.dart`)
- **Errors**: `401 Unauthorized (INVALID_OR_EXPIRED_REFRESH_TOKEN)`.

---

#### 4.1.4 Logout
- **Endpoint**: `POST /api/v1/auth/logout` (alias: `POST /api/auth/logout`)
- **Authentication**: Required (`Bearer <token>`)
- **Request Body**: None
- **Response JSON (200 OK)**:
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```
- **Flutter Model Consumed**: `void`

---

#### 4.1.5 Get Current User Profile
- **Endpoint**: `GET /api/v1/auth/me` (alias: `GET /api/auth/me`)
- **Authentication**: Required (`Bearer <token>`)
- **Request Body**: None
- **Response JSON (200 OK)**:
```json
{
  "id": "usr_01J6X7B9C1...",
  "email": "adira@spicesymphony.com",
  "full_name": "Adithya",
  "role": "owner",
  "business_id": "biz_01J6X7B9C2...",
  "is_active": true,
  "created_at": "2026-09-05T14:30:00Z"
}
```
- **Flutter Model Consumed**: `User` (`lib/features/auth/domain/models/user.dart`)
- **Errors**: `401 Unauthorized`.

---

### 4.2 Business Management & Keywords

#### 4.2.1 Get Active Business
- **Endpoint**: `GET /api/v1/business` (alias: `GET /api/business`, `GET /api/v1/businesses/me`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
{
  "id": "biz_01J6X7B9C2...",
  "name": "Spice Symphony",
  "category": "Restaurant & Hospitality",
  "website": "https://spicesymphony.in",
  "location": "Indiranagar, Bengaluru",
  "phone": "+91 98765 43210",
  "monitored_platforms": ["Google", "JustDial", "Reddit", "X", "Sulekha"],
  "keywords": [
    {
      "id": "kw_1",
      "keyword": "Spice Symphony",
      "category": "brand",
      "is_active": true,
      "business_id": "biz_01J6X7B9C2..."
    },
    {
      "id": "kw_2",
      "keyword": "Spice Symphony Indiranagar",
      "category": "brand",
      "is_active": true,
      "business_id": "biz_01J6X7B9C2..."
    }
  ],
  "owner_id": "usr_01J6X7B9C1...",
  "created_at": "2026-08-01T10:00:00Z"
}
```
- **Flutter Model Consumed**: `Business?` (`lib/features/onboarding/domain/models/business.dart`)
- **Errors**: `404 Not Found` (if user has not onboarded a business yet, returns `null` or 404 handled gracefully).

---

#### 4.2.2 Setup / Create Business (Onboarding Wizard)
- **Endpoint**: `POST /api/v1/business` (alias: `POST /api/business`, `POST /api/v1/businesses`)
- **Authentication**: Required (`Bearer <token>`)
- **Request Body**:
```json
{
  "name": "Spice Symphony",
  "category": "Restaurant",
  "website": "https://spicesymphony.in",
  "location": "Indiranagar, Bengaluru",
  "phone": "+91 98765 43210",
  "keywords": [
    "Spice Symphony",
    "Spice Symphony Indiranagar",
    "best biryani Indiranagar"
  ],
  "platforms": [
    "Google",
    "JustDial",
    "Reddit",
    "X"
  ]
}
```
- **Response JSON (201 Created)**: Same as 4.2.1 `Business`
- **Flutter Model Consumed**: `Business`
- **Errors**: `400 Bad Request`, `422 Validation Error`.

---

#### 4.2.3 Business List & Detail by ID
- `GET /api/v1/businesses` -> returns `List<Business>` for user.
- `GET /api/v1/businesses/{id}` -> returns `Business` (validating tenant ownership).
- `PUT /api/v1/businesses/{id}` -> updates business metadata.
- `DELETE /api/v1/businesses/{id}` -> deletes business (Owner role only).

---

#### 4.2.4 List Brand Keywords
- **Endpoint**: `GET /api/v1/keywords` (alias: `GET /api/keywords`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
[
  {
    "id": "kw_1",
    "keyword": "Spice Symphony",
    "category": "brand",
    "is_active": true,
    "business_id": "biz_01J6X7B9C2..."
  },
  {
    "id": "kw_2",
    "keyword": "best biryani Indiranagar",
    "category": "competitor",
    "is_active": true,
    "business_id": "biz_01J6X7B9C2..."
  }
]
```
- **Flutter Model Consumed**: `List<BrandKeyword>` (`lib/features/onboarding/domain/models/brand_keyword.dart`)

---

#### 4.2.5 Add Brand Keyword
- **Endpoint**: `POST /api/v1/keywords` (alias: `POST /api/keywords`)
- **Authentication**: Required (`Bearer <token>`)
- **Request Body**:
```json
{
  "keyword": "butter garlic naan Bengaluru",
  "category": "brand"
}
```
- **Response JSON (201 Created)**: `BrandKeyword`
- **Flutter Model Consumed**: `BrandKeyword`

---

#### 4.2.6 Delete Brand Keyword
- **Endpoint**: `DELETE /api/v1/keywords/{id}` (alias: `DELETE /api/keywords/{id}`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
{
  "success": true,
  "message": "Keyword deleted"
}
```
- **Flutter Model Consumed**: `void`

---

### 4.3 Dashboard & Aggregated Analytics

#### 4.3.1 Dashboard Summary
- **Endpoint**: `GET /api/v1/dashboard` (alias: `GET /api/dashboard`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
{
  "reputation_score": {
    "current_score": 78.4,
    "previous_score": 74.2,
    "change": 4.2,
    "trend": "up",
    "calculated_at": "2026-09-05T12:00:00Z"
  },
  "sentiment_distribution": {
    "positive": 142,
    "neutral": 58,
    "negative": 30,
    "total": 230,
    "positive_percentage": 61.7,
    "neutral_percentage": 25.2,
    "negative_percentage": 13.1
  },
  "total_mentions": 230,
  "crisis_active": true,
  "crisis_count": 1,
  "pending_responses_count": 3,
  "fraud_alerts_count": 1,
  "recent_mentions": [
    {
      "id": "men_1",
      "platform": "Reddit",
      "author": "u/bangalore_foodie",
      "content": "Had dinner at Spice Symphony yesterday. The mutton biryani was cold and smelled off...",
      "sentiment": "negative",
      "sentiment_score": -0.84,
      "is_fake": false,
      "fraud_confidence": 0.12,
      "url": "https://reddit.com/r/bangalore/comments/...",
      "timestamp": "2026-09-05T14:30:00Z",
      "engagement": {
        "likes": 42,
        "shares": 8,
        "comments": 15
      },
      "rating": 1.0,
      "response_status": "drafted",
      "response_text": "Dear u/bangalore_foodie, we are genuinely sorry...",
      "author_avatar": null
    }
  ]
}
```
- **Flutter Model Consumed**: `DashboardSummary` (`lib/features/dashboard/domain/models/dashboard_summary.dart`)

---

#### 4.3.2 Reputation Score
- **Endpoint**: `GET /api/v1/dashboard/score` (alias: `GET /api/dashboard/score`, `GET /api/v1/reputation`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
{
  "current_score": 78.4,
  "previous_score": 74.2,
  "change": 4.2,
  "trend": "up",
  "calculated_at": "2026-09-05T12:00:00Z"
}
```
- **Flutter Model Consumed**: `ReputationScore` (`lib/features/dashboard/domain/models/reputation_score.dart`)

---

#### 4.3.3 Sentiment Distribution
- **Endpoint**: `GET /api/v1/dashboard/sentiment` (alias: `GET /api/dashboard/sentiment`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
{
  "positive": 142,
  "neutral": 58,
  "negative": 30,
  "total": 230,
  "positive_percentage": 61.7,
  "neutral_percentage": 25.2,
  "negative_percentage": 13.1
}
```
- **Flutter Model Consumed**: `SentimentDistribution` (`lib/features/dashboard/domain/models/sentiment_distribution.dart`)

---

#### 4.3.4 Sentiment Trends
- **Endpoint**: `GET /api/v1/dashboard/trends` (alias: `GET /api/dashboard/trends`, `GET /api/v1/analytics/trends`)
- **Authentication**: Required (`Bearer <token>`)
- **Query Parameters**:
  - `days`: Integer (default: 7, supports 7, 30, 90)
- **Response JSON (200 OK)**:
```json
[
  {
    "date": "Mon",
    "positive": 18,
    "neutral": 6,
    "negative": 3,
    "score": 78.0
  },
  {
    "date": "Tue",
    "positive": 22,
    "neutral": 8,
    "negative": 2,
    "score": 82.5
  }
]
```
- **Flutter Model Consumed**: `List<SentimentTrend>` (`lib/features/dashboard/domain/models/sentiment_trend.dart`)

---

#### 4.3.5 Platform Statistics
- **Endpoint**: `GET /api/v1/dashboard/platforms` (alias: `GET /api/dashboard/platforms`, `GET /api/v1/analytics/platforms`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
[
  {
    "platform": "Google",
    "count": 110,
    "positive_percentage": 68.0,
    "negative_percentage": 12.0,
    "neutral_percentage": 20.0,
    "average_rating": 4.2
  },
  {
    "platform": "JustDial",
    "count": 45,
    "positive_percentage": 55.0,
    "negative_percentage": 22.0,
    "neutral_percentage": 23.0,
    "average_rating": 3.8
  },
  {
    "platform": "Reddit",
    "count": 25,
    "positive_percentage": 40.0,
    "negative_percentage": 36.0,
    "neutral_percentage": 24.0,
    "average_rating": 3.1
  }
]
```
- **Flutter Model Consumed**: `List<PlatformStatistics>` (`lib/features/dashboard/domain/models/platform_statistics.dart`)

---

#### 4.3.6 Full Sentiment Analytics Overview
- **Endpoint**: `GET /api/v1/analytics/sentiment` (alias: `GET /api/analytics/sentiment`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
{
  "distribution": {
    "positive": 142,
    "neutral": 58,
    "negative": 30,
    "total": 230,
    "positive_percentage": 61.7,
    "neutral_percentage": 25.2,
    "negative_percentage": 13.1
  },
  "trends": [
    {
      "date": "Mon",
      "positive": 18,
      "neutral": 6,
      "negative": 3,
      "score": 78.0
    }
  ],
  "platform_breakdown": [
    {
      "platform": "Google",
      "count": 110,
      "positive_percentage": 68.0,
      "negative_percentage": 12.0,
      "neutral_percentage": 20.0,
      "average_rating": 4.2
    }
  ],
  "overall_score": 78.4,
  "total_reviews_analyzed": 230
}
```
- **Flutter Model Consumed**: `SentimentAnalytics` (`lib/features/sentiment/domain/models/sentiment_analytics.dart`)

---

#### 4.3.7 Aspect Sentiment Analytics
- **Endpoint**: `GET /api/v1/analytics/aspects`
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
[
  {
    "aspect": "Food Quality",
    "sentiment": "POSITIVE",
    "positive_percentage": 78.5,
    "negative_percentage": 14.2,
    "neutral_percentage": 7.3,
    "sample_count": 95
  },
  {
    "aspect": "Service & Hospitality",
    "sentiment": "NEGATIVE",
    "positive_percentage": 35.0,
    "negative_percentage": 52.0,
    "neutral_percentage": 13.0,
    "sample_count": 60
  }
]
```

---

### 4.4 Mentions & Reviews

#### 4.4.1 Paginated Mentions Feed
- **Endpoint**: `GET /api/v1/mentions` (alias: `GET /api/mentions`)
- **Authentication**: Required (`Bearer <token>`)
- **Query Parameters**:
  - `page`: Integer (default: 1)
  - `limit`: Integer (default: 20)
  - `platform`: String (optional: "Google", "Reddit", "X", "JustDial", "Sulekha")
  - `sentiment`: String (optional: "positive", "neutral", "negative")
  - `is_fake`: Boolean (optional: true, false)
  - `q`: String (search keyword in content or author)
  - `sort_by`: String (default: "newest", supports "oldest", "highest_rating", "lowest_rating")
- **Response JSON (200 OK)**:
```json
{
  "items": [
    {
      "id": "men_1",
      "platform": "Reddit",
      "author": "u/bangalore_foodie",
      "content": "Had dinner at Spice Symphony yesterday. The mutton biryani was cold and smelled off. When we informed staff, they were dismissive. Never going back! Beware guys.",
      "sentiment": "negative",
      "sentiment_score": -0.84,
      "is_fake": false,
      "fraud_confidence": 0.12,
      "url": "https://reddit.com/r/bangalore/comments/...",
      "timestamp": "2026-09-05T14:30:00Z",
      "engagement": {
        "likes": 42,
        "shares": 8,
        "comments": 15
      },
      "rating": 1.0,
      "response_status": "drafted",
      "response_text": "Dear u/bangalore_foodie, we are genuinely sorry...",
      "author_avatar": null
    }
  ],
  "total_count": 230,
  "page": 1,
  "total_pages": 12,
  "has_more": true
}
```
- **Flutter Model Consumed**: `PaginatedMentions` (`lib/features/mentions/domain/models/paginated_mentions.dart`)

---

#### 4.4.2 Mention Detail
- **Endpoint**: `GET /api/v1/mentions/{id}` (alias: `GET /api/mentions/{id}`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**: `Mention`
- **Flutter Model Consumed**: `Mention` (`lib/features/mentions/domain/models/mention.dart`)
- **Errors**: `404 Not Found (MENTION_NOT_FOUND)`.

---

#### 4.4.3 Reviews (Mentions with Ratings)
- **Endpoint**: `GET /api/v1/reviews` & `GET /api/v1/reviews/{id}`
- Filtered subset of mentions with explicit rating values (`1.0` - `5.0`).

---

### 4.5 Fraud Detection

#### 4.5.1 List Flagged Fraudulent Reviews
- **Endpoint**: `GET /api/v1/fraud` (alias: `GET /api/fraud`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
[
  {
    "mention_id": "men_fraud_1",
    "is_fraudulent": true,
    "confidence": 0.94,
    "risk_level": "critical",
    "reasons": [
      "4 reviews posted within 8 minutes from fresh accounts",
      "Identical syntactic structures detected across competitor accounts"
    ],
    "patterns": [
      {
        "pattern_name": "Review Burst",
        "description": "Coordinated burst of 4 reviews in 8 minutes",
        "severity": "critical"
      },
      {
        "pattern_name": "Account Freshness",
        "description": "Accounts created < 24h prior to review",
        "severity": "high"
      }
    ],
    "review_content": "Worst experience ever, complete scam! Do not visit!",
    "author": "Rajesh Kumar",
    "platform": "JustDial",
    "timestamp": "2026-09-05T12:00:00Z"
  }
]
```
- **Flutter Model Consumed**: `List<FraudResult>` (`lib/features/fraud/domain/models/fraud_result.dart`)

---

#### 4.5.2 Fraud Analysis by Mention ID
- **Endpoint**: `GET /api/v1/fraud/{mention_id}` (alias: `GET /api/fraud/{mention_id}`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**: `FraudResult`
- **Flutter Model Consumed**: `FraudResult`

---

#### 4.5.3 Trigger On-Demand Fraud Analysis
- **Endpoint**: `POST /api/v1/fraud/analyze/{mention_id}`
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**: `FraudResult`

---

### 4.6 Crisis Detection & Management

#### 4.6.1 List Crisis Events
- **Endpoint**: `GET /api/v1/crisis` (alias: `GET /api/crisis`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
[
  {
    "id": "crs_1",
    "title": "Severe Food Quality & Hygiene Complaints",
    "severity": "high",
    "status": "active",
    "trigger_reason": "Negative mention velocity surged on Reddit (+14.5 mentions/hr) regarding food quality.",
    "velocity": 14.5,
    "negative_mentions_count": 18,
    "affected_platforms": ["Reddit", "X", "Google"],
    "started_at": "2026-09-05T13:00:00Z",
    "resolved_at": null,
    "suggested_actions": [
      "Issue prompt public clarification addressing kitchen inspection",
      "Reach out directly to affected diners with direct contact info",
      "Pause ongoing promotional campaigns"
    ],
    "estimated_reach": 15400,
    "peak_volume_per_hour": 16
  }
]
```
- **Flutter Model Consumed**: `List<CrisisEvent>` (`lib/features/crisis/domain/models/crisis_event.dart`)

---

#### 4.6.2 Get Active Crisis (if any)
- **Endpoint**: `GET /api/v1/crisis/active` (alias: `GET /api/crisis/active`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK or 204 No Content)**:
  - If active crisis exists: returns `CrisisEvent`
  - If no active crisis: returns `null` (HTTP 200 with `null` or 204)
- **Flutter Model Consumed**: `CrisisEvent?`

---

#### 4.6.3 Get Crisis by ID
- **Endpoint**: `GET /api/v1/crisis/{id}` (alias: `GET /api/crisis/{id}`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**: `CrisisEvent`
- **Flutter Model Consumed**: `CrisisEvent`

---

#### 4.6.4 Update Crisis Status (Resolve / Mitigate)
- **Endpoint**: `PATCH /api/v1/crisis/{id}`
- **Authentication**: Required (`Bearer <token>`)
- **Request Body**:
```json
{
  "status": "resolved"
}
```
- **Response JSON (200 OK)**: `CrisisEvent`

---

### 4.7 Alerts System

#### 4.7.1 List Alerts
- **Endpoint**: `GET /api/v1/alerts` (alias: `GET /api/alerts`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
[
  {
    "id": "alt_1",
    "type": "crisis",
    "title": "Active Reputation Crisis Detected",
    "message": "Negative mention velocity surged on Reddit (+14.5 mentions/hr) regarding food quality.",
    "severity": "high",
    "timestamp": "2026-09-05T14:05:00Z",
    "is_read": false,
    "reference_id": "crs_1",
    "reference_type": "crisis"
  },
  {
    "id": "alt_2",
    "type": "fraud",
    "title": "Suspicious Review Wave Flagged",
    "message": "4 reviews posted within 8 minutes from fresh accounts on JustDial show coordinated behavior.",
    "severity": "critical",
    "timestamp": "2026-09-05T12:30:00Z",
    "is_read": false,
    "reference_id": "men_fraud_1",
    "reference_type": "mention"
  }
]
```
- **Flutter Model Consumed**: `List<AlertItem>` (`lib/features/alerts/domain/models/alert_item.dart`)

---

#### 4.7.2 Mark Alert as Read
- **Endpoint**: `PUT /api/v1/alerts/{id}/read` & `PATCH /api/v1/alerts/{id}/read` (alias: `PUT /api/alerts/{id}/read`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
{
  "success": true,
  "message": "Alert marked as read"
}
```
- **Flutter Model Consumed**: `void`

---

#### 4.7.3 Mark All Alerts as Read
- **Endpoint**: `PATCH /api/v1/alerts/read-all`
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**:
```json
{
  "success": true,
  "marked_count": 5
}
```

---

### 4.8 AI Response Studio

#### 4.8.1 Generate AI Response Draft
- **Endpoint**: `POST /api/v1/responses/generate` (alias: `POST /api/responses/generate`, `POST /api/v1/ai/responses/generate`)
- **Authentication**: Required (`Bearer <token>`)
- **Request Body**:
```json
{
  "mention_id": "men_1",
  "tone": "empathetic",
  "custom_instructions": "Offer personal phone contact with restaurant manager"
}
```
- **Supported Tones**:
  - `empathetic` (apologetic, sincere, customer-delight focused)
  - `professional` (formal, objective, management review)
  - `firm` (factual, policy and receipt verification)
  - `promotional` (cheerful, inviting, menu highlights)
- **Response JSON (201 Created / 200 OK)**:
```json
{
  "id": "res_1725547800000",
  "mention_id": "men_1",
  "original_review": "Had dinner at Spice Symphony yesterday. The mutton biryani was cold and smelled off...",
  "generated_response": "Dear u/bangalore_foodie, we are genuinely sorry to hear that your dining experience did not meet our high standards. Quality and customer delight are everything to us. Please reach out to our manager at +91 98765 43210 so we can personally make amends.",
  "tone": "empathetic",
  "status": "drafted",
  "created_at": "2026-09-05T15:00:00Z",
  "approved_at": null,
  "dispatched_at": null
}
```
- **Flutter Model Consumed**: `ResponseDraft` (`lib/features/responses/domain/models/response_draft.dart`)

---

#### 4.8.2 List Response Drafts
- **Endpoint**: `GET /api/v1/responses` (alias: `GET /api/responses`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**: `List<ResponseDraft>`
- **Flutter Model Consumed**: `List<ResponseDraft>`

---

#### 4.8.3 Get Response Draft by ID
- **Endpoint**: `GET /api/v1/responses/{id}` (alias: `GET /api/responses/{id}`)
- **Authentication**: Required (`Bearer <token>`)
- **Response JSON (200 OK)**: `ResponseDraft`
- **Flutter Model Consumed**: `ResponseDraft`

---

#### 4.8.4 Approve Response Draft
- **Endpoint**: `POST /api/v1/responses/{id}/approve` (alias: `POST /api/responses/{id}/approve`)
- **Authentication**: Required (`Bearer <token>`)
- **Request Body**:
```json
{
  "response_text": "Dear u/bangalore_foodie, our general manager would like to host your family for dinner..."
}
```
- **Response JSON (200 OK)**:
```json
{
  "id": "res_1725547800000",
  "mention_id": "men_1",
  "original_review": "Had dinner at Spice Symphony yesterday...",
  "generated_response": "Dear u/bangalore_foodie, our general manager would like to host your family for dinner...",
  "tone": "empathetic",
  "status": "approved",
  "created_at": "2026-09-05T15:00:00Z",
  "approved_at": "2026-09-05T15:10:00Z",
  "dispatched_at": null
}
```
- **Flutter Model Consumed**: `ResponseDraft`

---

#### 4.8.5 Dispatch / Publish Response Draft
- **Endpoint**: `POST /api/v1/responses/{id}/dispatch` (alias: `POST /api/responses/{id}/dispatch`, `POST /api/v1/ai/responses/{id}/publish`)
- **Authentication**: Required (`Bearer <token>`)
- **Request Body**: None
- **Response JSON (200 OK)**:
```json
{
  "id": "res_1725547800000",
  "mention_id": "men_1",
  "original_review": "Had dinner at Spice Symphony yesterday...",
  "generated_response": "Dear u/bangalore_foodie, our general manager would like to host your family for dinner...",
  "tone": "empathetic",
  "status": "dispatched",
  "created_at": "2026-09-05T15:00:00Z",
  "approved_at": "2026-09-05T15:10:00Z",
  "dispatched_at": "2026-09-05T15:12:00Z"
}
```
- **Flutter Model Consumed**: `ResponseDraft`

---

### 4.9 Devices & Push Notifications (FCM)

#### 4.9.1 Register FCM Device Token
- **Endpoint**: `POST /api/v1/devices/register` (alias: `POST /api/devices/register`)
- **Authentication**: Required (`Bearer <token>`)
- **Request Body**:
```json
{
  "fcm_token": "eXamPle_fcm_t0ken_string...",
  "device_type": "android"
}
```
- **Response JSON (200 OK)**:
```json
{
  "success": true,
  "message": "Device token registered"
}
```
