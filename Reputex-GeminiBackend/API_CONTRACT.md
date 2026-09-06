# RepuTex API Contract Specification

This document defines the REST API contract implemented by the backend and consumed by the Flutter mobile application (`c:\Users\adira\Projects\major\Reputex-App`).

All endpoints are accessible with prefix `/api` (Flutter default) and `/api/v1` (REST standard).

---

## 1. Authentication

### POST `/api/auth/register`
Creates a new owner account and initial business.
- **Request Body**:
  ```json
  {
    "email": "user@business.com",
    "password": "Password123!",
    "full_name": "Jane Doe",
    "business_name": "Spice Symphony",
    "business_category": "Restaurant"
  }
  ```
- **Response** `201 Created`:
  ```json
  {
    "user": {
      "id": "uuid",
      "email": "user@business.com",
      "full_name": "Jane Doe",
      "role": "owner",
      "business_id": "uuid",
      "is_active": true
    },
    "tokens": {
      "access_token": "jwt...",
      "refresh_token": "jwt...",
      "token_type": "bearer"
    }
  }
  ```

### POST `/api/auth/login`
- **Request Body**:
  ```json
  {
    "email": "user@business.com",
    "password": "Password123!"
  }
  ```
- **Response** `200 OK`: Same as register.

### GET `/api/auth/me`
- **Header**: `Authorization: Bearer <access_token>`
- **Response** `200 OK`: `User` object.

---

## 2. Business & Scans

### GET `/api/business`
Returns current business details and keywords.

### POST `/api/business/scan`
Triggers asynchronous scan workflow.
- **Response** `200 OK`:
  ```json
  {
    "scan_id": "uuid",
    "status": "PENDING",
    "message": "Scan initiated successfully",
    "business_id": "uuid"
  }
  ```

### GET `/api/business/scan/status`
Returns real-time scan progress and state machine status.
- **Response** `200 OK`:
  ```json
  {
    "scan_id": "uuid",
    "business_id": "uuid",
    "status": "COMPLETED",
    "current_step": "Scan completed successfully with evidence findings",
    "google_status": "COMPLETED",
    "reddit_status": "COMPLETED",
    "x_status": "COMPLETED",
    "mentions_found": 75,
    "mentions_added": 75,
    "progress_pct": 100
  }
  ```

---

## 3. Dashboard & Analytics

### GET `/api/dashboard`
Returns high-level summary for the mobile dashboard.
- **Response** `200 OK`:
  ```json
  {
    "reputation_score": {
      "current_score": 72.4,
      "previous_score": 78.0,
      "change": -5.6,
      "trend": "declining"
    },
    "sentiment_distribution": {
      "positive": 18,
      "neutral": 22,
      "negative": 35,
      "total": 75,
      "positive_percentage": 24.0,
      "neutral_percentage": 29.3,
      "negative_percentage": 46.7
    },
    "total_mentions": 75,
    "crisis_active": true,
    "crisis_risk_level": "High",
    "suspicious_reviews_count": 6,
    "active_clusters_count": 1,
    "top_issues": [...],
    "recent_mentions": [...]
  }
  ```

---

## 4. Customer Issues

### GET `/api/issues`
- **Response** `200 OK`:
  ```json
  {
    "items": [
      {
        "id": "uuid",
        "business_id": "uuid",
        "category": "Customer Service",
        "subtopic": "Staff Behavior",
        "severity": "high",
        "status": "active",
        "mention_count": 18,
        "platforms_breakdown": {"google": 10, "reddit": 6, "twitter": 2},
        "sentiment_breakdown": {"negative": 18},
        "evidence": [
          {
            "id": "uuid",
            "mention_id": "uuid",
            "excerpt": "The waiter had a major attitude and rolled his eyes.",
            "relevance_score": 1.0
          }
        ]
      }
    ],
    "total": 1
  }
  ```

---

## 5. Findings & Authenticity

### GET `/api/findings`
Returns traceable findings explaining what occurred and citing evidence.

### GET `/api/suspicious-reviews`
Returns findings of type `SUSPICIOUS_REVIEW`.

### GET `/api/manipulation-clusters`
Returns findings of type `MANIPULATION_CLUSTER`.

### GET `/api/fraud`
Returns structured review authenticity scores (0-100), risk levels, and identified patterns.

---

## 6. Crisis Monitoring

### GET `/api/crisis` & `/api/crisis/active`
Returns active crisis alert with trigger reason, velocity, affected platforms, and suggested mitigation actions.
