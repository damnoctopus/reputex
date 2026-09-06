"""High-fidelity deterministic MockPlatformConnector for local development and offline testing.

Exercises the real query builder and emits raw platform records matching the domain contract.
"""

from datetime import UTC, datetime, timedelta
from typing import Any

from app.integrations.base import PlatformConnector
from app.integrations.query_builder import PlatformQueryBuilder
from app.schemas.ingestion import RawMentionRecord


class MockPlatformConnector(PlatformConnector):
    platform_name: str = "MockPlatform"

    def __init__(self, platform: str = "MockPlatform"):
        self.platform_name = platform

    async def fetch_mentions(
        self,
        business_name: str,
        keywords: list[str],
        since: datetime | None = None,
        cursor: str | None = None,
        location: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch raw external records using the platform query builder."""
        query = PlatformQueryBuilder.build_query(
            platform=self.platform_name,
            business_name=business_name,
            keywords=keywords,
            location=location,
        )

        now = datetime.now(UTC)
        meta_base = {
            "query_used": query.query_string,
            "keywords_used": query.keywords_used,
            "filters": query.filters,
            "connector": "MockPlatformConnector",
        }

        # Deterministic raw records pool
        raw_pool: list[RawMentionRecord] = [
            RawMentionRecord(
                platform="Reddit",
                external_id="red_post_101",
                source_url="https://reddit.com/r/bangalore/comments/spice_symphony_review",
                title=f"Disappointing dinner at {business_name}",
                content=f"Had dinner at {business_name} yesterday. The mutton biryani was cold and smelled off. When we informed staff, they were dismissive. Never going back! Beware guys.",
                author="u/bangalore_foodie",
                author_id="user_red_101",
                author_avatar=None,
                published_at=now - timedelta(hours=3),
                collected_at=now,
                rating=1.0,
                engagement={"likes": 42, "shares": 8, "comments": 15},
                metadata={**meta_base, "subreddit": "r/bangalore"},
                raw_payload={"id": "red_post_101", "ups": 42, "num_comments": 15},
            ),
            RawMentionRecord(
                platform="X",
                external_id="tw_post_202",
                source_url="https://x.com/foodie_bangalore/status/987654321",
                title=None,
                content=f"{business_name} in Indiranagar has the crispiest butter garlic naan in the city! Service was top notch too. Highly recommended for family dinners. ⭐⭐⭐⭐⭐",
                author="@foodie_bangalore",
                author_id="user_tw_202",
                author_avatar="https://pbs.twimg.com/profile_images/sample.jpg",
                published_at=now - timedelta(hours=6),
                collected_at=now,
                rating=5.0,
                engagement={"likes": 128, "shares": 34, "comments": 12},
                metadata={**meta_base, "tweet_type": "original"},
                raw_payload={"id": "tw_post_202", "retweet_count": 34, "like_count": 128},
            ),
            RawMentionRecord(
                platform="Google",
                external_id="goog_rev_303",
                source_url="https://maps.google.com/?cid=123456",
                title="Decent Ambience",
                content=f"Decent ambience and prompt seating. Paneer tikka was great, but mocktails took almost 25 minutes to arrive. Average experience overall at {business_name}.",
                author="Priya Sharma",
                author_id="goog_user_303",
                author_avatar=None,
                published_at=now - timedelta(days=1),
                collected_at=now,
                rating=3.0,
                engagement={"likes": 3, "shares": 0, "comments": 1},
                metadata={**meta_base, "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4"},
                raw_payload={"review_id": "goog_rev_303", "stars": 3},
            ),
            RawMentionRecord(
                platform="Google",
                external_id="goog_rev_304",
                source_url="https://maps.google.com/?cid=123456&rev=304",
                title="Exquisite Dining",
                content=f"Exceptional culinary journey at {business_name}! The chef personally checked on our table. Best dining spot in town hands down.",
                author="Ananya Roy",
                author_id="goog_user_304",
                author_avatar="https://lh3.googleusercontent.com/a/sample_avatar.jpg",
                published_at=now - timedelta(days=2),
                collected_at=now,
                rating=5.0,
                engagement={"likes": 8, "shares": 1, "comments": 2},
                metadata={**meta_base, "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4"},
                raw_payload={"review_id": "goog_rev_304", "stars": 5},
            ),
            RawMentionRecord(
                platform="JustDial",
                external_id="jd_rev_404",
                source_url="https://justdial.com/Bengaluru/Spice-Symphony",
                title="Horrible Fraud",
                content="Worst experience ever, complete scam! Do not visit this place at all!",
                author="Rajesh Kumar",
                author_id="jd_user_404",
                author_avatar=None,
                published_at=now - timedelta(hours=2),
                collected_at=now,
                rating=1.0,
                engagement={"likes": 1, "shares": 0, "comments": 0},
                metadata={**meta_base, "verified_buyer": False},
                raw_payload={"jd_id": "jd_rev_404", "rating_stars": 1},
            ),
            RawMentionRecord(
                platform="X",
                external_id="tw_post_205",
                source_url="https://x.com/tech_diner/status/1122334455",
                title=None,
                content=f"Thinking about trying {business_name} tonight with colleagues. Has anyone checked out their weekend buffet recently? Any keyword recommendations?",
                author="@tech_diner",
                author_id="user_tw_205",
                author_avatar=None,
                published_at=now - timedelta(hours=12),
                collected_at=now,
                rating=None,
                engagement={"likes": 15, "shares": 2, "comments": 7},
                metadata={**meta_base, "tweet_type": "query"},
                raw_payload={"id": "tw_post_205", "retweet_count": 2, "like_count": 15},
            ),
            RawMentionRecord(
                platform="Reddit",
                external_id="red_post_106",
                source_url="https://reddit.com/r/bangalore/comments/best_restaurants_thread",
                title="Weekly Bangalore Food Thread",
                content=f"Shoutout to {business_name} for catering our team lunch! Fresh naan, tender butter chicken and on-time delivery.",
                author="u/dev_guru_blr",
                author_id="user_red_106",
                author_avatar=None,
                published_at=now - timedelta(days=3),
                collected_at=now,
                rating=4.5,
                engagement={"likes": 67, "shares": 5, "comments": 22},
                metadata={**meta_base, "subreddit": "r/bangalore"},
                raw_payload={"id": "red_post_106", "ups": 67},
            ),
            RawMentionRecord(
                platform="Google",
                external_id="goog_rev_307",
                source_url="https://maps.google.com/?cid=123456&rev=307",
                title="Clean and hygienic",
                content=f"Clean tables, fast billing, and courteous valets at {business_name}. Will surely visit again with family.",
                author="Siddharth Jain",
                author_id="goog_user_307",
                author_avatar=None,
                published_at=now - timedelta(days=4),
                collected_at=now,
                rating=4.0,
                engagement={"likes": 5, "shares": 0, "comments": 0},
                metadata={**meta_base, "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4"},
                raw_payload={"review_id": "goog_rev_307", "stars": 4},
            ),
            RawMentionRecord(
                platform="X",
                external_id="tw_post_208",
                source_url="https://x.com/chef_insights/status/998877665",
                title=None,
                content=f"Great hospitality seen at {business_name}. Staff was well trained in allergen management.",
                author="@chef_insights",
                author_id="user_tw_208",
                author_avatar=None,
                published_at=now - timedelta(days=5),
                collected_at=now,
                rating=5.0,
                engagement={"likes": 88, "shares": 19, "comments": 4},
                metadata={**meta_base, "tweet_type": "review"},
                raw_payload={"id": "tw_post_208", "like_count": 88},
            ),
            RawMentionRecord(
                platform="Google",
                external_id="goog_rev_309",
                source_url="https://maps.google.com/?cid=123456&rev=309",
                title="Slow kitchen",
                content=f"Food tastes authentic but preparation takes a long time at {business_name}. Be prepared to wait at least 30 minutes during peak rush hours.",
                author="Vikram Sethi",
                author_id="goog_user_309",
                author_avatar=None,
                published_at=now - timedelta(days=6),
                collected_at=now,
                rating=2.0,
                engagement={"likes": 12, "shares": 1, "comments": 3},
                metadata={**meta_base, "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4"},
                raw_payload={"review_id": "goog_rev_309", "stars": 2},
            ),
        ]

        # Filter by platform if connector is configured for a specific one
        if self.platform_name.lower() not in ["mockplatform", "all", "base"]:
            matched = [r for r in raw_pool if r.platform.lower() == self.platform_name.lower()]
            if matched:
                return matched
            # If no direct match in pool, construct a tailored record
            return [
                RawMentionRecord(
                    platform=self.platform_name,
                    external_id=f"{self.platform_name.lower()}_mock_001",
                    source_url=f"https://{self.platform_name.lower()}.com/mock_review",
                    title=f"{self.platform_name} Review for {business_name}",
                    content=f"Sample feedback from {self.platform_name} regarding {business_name}. Service was pleasant.",
                    author="Mock Reviewer",
                    published_at=now - timedelta(hours=1),
                    collected_at=now,
                    rating=4.0,
                    engagement={"likes": 5, "shares": 1, "comments": 0},
                    metadata=meta_base,
                    raw_payload={"mock": True},
                )
            ]

        # Return full 10 records for MockPlatform/All
        return raw_pool

    async def fetch_reviews(
        self,
        business_identifier: str,
        since: datetime | None = None,
        cursor: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        mentions = await self.fetch_mentions(
            business_identifier, [], since=since, cursor=cursor, credentials=credentials
        )
        return [m for m in mentions if m.rating is not None]

    async def publish_response(
        self,
        external_mention_id: str,
        response_text: str,
    ) -> bool:
        return True
