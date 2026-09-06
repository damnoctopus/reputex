"""Deterministic database seed script to populate realistic demo intelligence for RepuTex."""

import asyncio
import os
import sys
from datetime import UTC, datetime, timedelta

# Ensure project root in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal, Base, engine
from app.core.security import hash_password
from app.models.ai_response import AIResponse
from app.models.alert import Alert
from app.models.business import BrandKeyword, Business, BusinessMember
from app.models.crisis import CrisisEvent
from app.models.fraud import FraudAnalysis
from app.models.mention import Mention
from app.models.reputation import ReputationScoreHistory
from app.models.sentiment import MentionAspect
from app.models.user import User


async def seed_database():
    print("[Seed] Initializing database schema...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        print("[Seed] Creating demo user and business...")

        # 1. Demo User
        user_id = "usr_demo_adira"
        biz_id = "biz_demo_spicesymphony"

        # Check if already seeded
        from sqlalchemy import select

        existing_user = (
            (await session.execute(select(User).where(User.email == "adira@spicesymphony.com"))).scalars().first()
        )
        if existing_user:
            print("[Seed] Database already contains seed user 'adira@spicesymphony.com'. Skipping.")
            return

        demo_user = User(
            id=user_id,
            email="adira@spicesymphony.com",
            password_hash=hash_password("Password123!"),
            full_name="Adithya Raman",
            phone="+91 98765 43210",
            role="owner",
            business_id=biz_id,
            is_active=True,
        )
        session.add(demo_user)

        # 2. Demo Business
        demo_business = Business(
            id=biz_id,
            owner_id=user_id,
            name="Spice Symphony",
            category="Fine Dining Restaurant",
            description="Authentic royal Indian fine dining, dum biryanis, and artisan desserts in Bangalore.",
            website="https://spicesymphony.in",
            location="Indiranagar, Bangalore",
            phone="+91 80 4123 5678",
            monitored_platforms=["google", "instagram", "reddit", "twitter"],
        )

        session.add(demo_business)

        # 3. Business Member
        member = BusinessMember(
            business_id=biz_id,
            user_id=user_id,
            role="owner",
        )
        session.add(member)

        # 4. Brand Keywords
        keywords = [
            BrandKeyword(business_id=biz_id, keyword="Spice Symphony", category="brand"),
            BrandKeyword(business_id=biz_id, keyword="dum biryani", category="product"),
            BrandKeyword(business_id=biz_id, keyword="paneer tikka", category="product"),
            BrandKeyword(business_id=biz_id, keyword="gulab jamun", category="product"),
            BrandKeyword(business_id=biz_id, keyword="Indiranagar", category="location"),
            BrandKeyword(business_id=biz_id, keyword="Chef Sanjeev", category="personnel"),
        ]
        session.add_all(keywords)

        # 5. Mentions & Reviews
        now = datetime.now(UTC)
        raw_mentions = [
            {
                "platform": "Google",
                "author": "Pooja Sharma",
                "content": "The Dum Biryani here is hands down the best in Indiranagar! Fragrant, perfectly spiced, and the gulab jamun melted in our mouths. Staff was remarkably courteous!",
                "rating": 5.0,
                "sentiment": "positive",
                "sentiment_score": 0.92,
                "is_fake": False,
                "published_at": now - timedelta(hours=3),
                "engagement": {"likes": 18, "helpful": 14},
            },
            {
                "platform": "Google",
                "author": "Anand Varma",
                "content": "Paneer tikka was wonderfully smoky and fresh. However, the wait time on a Saturday evening was almost 45 minutes despite reservations. Service was slow.",
                "rating": 3.0,
                "sentiment": "neutral",
                "sentiment_score": 0.15,
                "is_fake": False,
                "published_at": now - timedelta(hours=9),
                "engagement": {"likes": 7, "helpful": 5},
            },
            {
                "platform": "Google",
                "author": "Karthik R.",
                "content": "Horrible experience! Food smelled off, chicken was cold and staff was completely dismissive when we complained. Complete scam, avoid at all costs!",
                "rating": 1.0,
                "sentiment": "negative",
                "sentiment_score": -0.88,
                "is_fake": True,
                "fraud_confidence": 0.82,
                "published_at": now - timedelta(hours=14),
                "engagement": {"likes": 2, "helpful": 0},
            },
            {
                "platform": "Google",
                "author": "Ramesh Unknown",
                "content": "Worst experience ever! Food smelled off, staff rude, total scam! Do not visit this place!",
                "rating": 1.0,
                "sentiment": "negative",
                "sentiment_score": -0.90,
                "is_fake": True,
                "fraud_confidence": 0.89,
                "published_at": now - timedelta(hours=14, minutes=10),
                "engagement": {"likes": 0, "helpful": 0},
            },
            {
                "platform": "Instagram",
                "author": "@bangalore_food_diaries",
                "content": "Obsessed with the presentation at @spicesymphony! Look at this saffron-infused biryani pot! The ambience is pure luxury. Rating: 10/10 ✨🍛",
                "rating": 5.0,
                "sentiment": "positive",
                "sentiment_score": 0.96,
                "is_fake": False,
                "published_at": now - timedelta(days=1, hours=2),
                "engagement": {"likes": 642, "comments": 38},
            },
            {
                "platform": "Instagram",
                "author": "@kavita_eats",
                "content": "Cozy dinner at Spice Symphony. Great mocktails and warm staff. Perfectly executed kebabs.",
                "rating": 4.5,
                "sentiment": "positive",
                "sentiment_score": 0.85,
                "is_fake": False,
                "published_at": now - timedelta(days=2),
                "engagement": {"likes": 189, "comments": 12},
            },
            {
                "platform": "Reddit",
                "author": "u/masala_dev",
                "content": "Has anyone visited Spice Symphony on 100ft road recently? Heard their weekend rush is causing massive delays and cold starters.",
                "rating": 2.5,
                "sentiment": "negative",
                "sentiment_score": -0.45,
                "is_fake": False,
                "published_at": now - timedelta(days=2, hours=6),
                "engagement": {"upvotes": 34, "comments": 21},
            },
            {
                "platform": "Twitter",
                "author": "@techie_foodie",
                "content": "Quick team dinner @spicesymphony Indiranagar. Prompt billing, top notch naan and dal makhani. Recommended for corporate dinners!",
                "rating": 4.0,
                "sentiment": "positive",
                "sentiment_score": 0.78,
                "is_fake": False,
                "published_at": now - timedelta(days=3),
                "engagement": {"retweets": 4, "likes": 27},
            },
        ]

        seeded_mentions = []
        for i, m_data in enumerate(raw_mentions):
            m = Mention(
                id=f"men_seed_{i + 1}",
                business_id=biz_id,
                platform=m_data["platform"],
                external_id=f"ext_{i + 1}",
                author=m_data["author"],
                content=m_data["content"],
                url=f"https://{m_data['platform'].lower()}.com/review/{i + 1}",
                rating=m_data["rating"],
                sentiment=m_data["sentiment"],
                sentiment_score=m_data["sentiment_score"],
                is_fake=m_data["is_fake"],
                fraud_confidence=m_data.get("fraud_confidence", 0.05),
                engagement=m_data["engagement"],
                published_at=m_data["published_at"],
            )
            session.add(m)
            seeded_mentions.append(m)

        await session.flush()

        # 6. Aspects
        aspects_data = [
            ("men_seed_1", "Food Quality", "POSITIVE", 0.95),
            ("men_seed_1", "Service & Hospitality", "POSITIVE", 0.90),
            ("men_seed_2", "Food Quality", "POSITIVE", 0.85),
            ("men_seed_2", "Service & Hospitality", "NEGATIVE", 0.75),
            ("men_seed_3", "Food Quality", "NEGATIVE", 0.90),
            ("men_seed_3", "Service & Hospitality", "NEGATIVE", 0.92),
            ("men_seed_5", "Ambience & Cleanliness", "POSITIVE", 0.98),
            ("men_seed_8", "Price & Value", "POSITIVE", 0.85),
        ]
        for mid, asp, sent, conf in aspects_data:
            session.add(
                MentionAspect(
                    mention_id=mid,
                    business_id=biz_id,
                    aspect=asp,
                    sentiment=sent,
                    confidence=conf,
                )
            )

        # 7. Fraud Analysis for fake mentions
        fake_m = seeded_mentions[2]
        session.add(
            FraudAnalysis(
                mention_id=fake_m.id,
                business_id=biz_id,
                is_fraudulent=True,
                confidence=0.89,
                risk_level="critical",
                reasons=[
                    "Contains high-frequency negative spam triggers: complete scam, avoid at all costs",
                    "Near-identical text wave detected across 2 reviews posted within 10 minutes",
                ],
                patterns=[
                    {
                        "pattern_name": "Duplicate Text Wave",
                        "description": "Identical review text posted across different accounts",
                        "severity": "critical",
                    }
                ],
            )
        )

        # 8. Reputation Score History (past 7 days)
        scores = [81.5, 82.0, 83.2, 84.0, 85.1, 87.0, 88.5]
        for days_ago, sc in enumerate(reversed(scores)):
            session.add(
                ReputationScoreHistory(
                    business_id=biz_id,
                    current_score=sc,
                    previous_score=sc - 1.2 if days_ago > 0 else 80.0,
                    change=1.2,
                    trend="improving",
                    components={
                        "rating_component": 88.0,
                        "sentiment_component": 85.0,
                        "volume_component": 82.0,
                        "response_component": 90.0,
                        "fraud_penalty": 2.5,
                    },
                    calculated_at=now - timedelta(days=days_ago),
                )
            )

        # 9. Crisis Event
        session.add(
            CrisisEvent(
                id="crs_seed_1",
                business_id=biz_id,
                title="Service Quality Complaint Wave",
                severity="high",
                status="active",
                trigger_reason="Unusual concentration of 1-star reviews on Google citing dinner rush wait times.",
                velocity=3.4,
                negative_mentions_count=4,
                affected_platforms=["Google", "Reddit"],
                suggested_actions=[
                    "Deploy proactive empathetic apologies on negative Google reviews",
                    "Offer direct manager contact and complimentary dessert voucher",
                    "Brief floor staff on peak-hour table communication protocols",
                ],
                estimated_reach=1450,
                peak_volume_per_hour=4,
                started_at=now - timedelta(hours=6),
            )
        )

        # 10. Alerts
        alerts = [
            Alert(
                id="alt_seed_1",
                business_id=biz_id,
                type="CRISIS",
                title="Service Quality Complaint Wave",
                message="Multiple 1-star reviews detected on Google within the last 4 hours.",
                severity="critical",
                is_read=False,
                reference_id="crs_seed_1",
                reference_type="crisis",
                created_at=now - timedelta(minutes=45),
            ),
            Alert(
                id="alt_seed_2",
                business_id=biz_id,
                type="FRAUD_DETECTED",
                title="Potential Astroturfing Detected",
                message="Cluster of 2 near-identical 1-star reviews posted from suspicious accounts.",
                severity="high",
                is_read=False,
                reference_id="men_seed_3",
                reference_type="fraud",
                created_at=now - timedelta(hours=2),
            ),
            Alert(
                id="alt_seed_3",
                business_id=biz_id,
                type="AI_RESPONSE_READY",
                title="AI Response Draft Generated",
                message="Empathetic response draft ready for review on Google Maps review by Anand Varma.",
                severity="low",
                is_read=False,
                reference_id="resp_seed_1",
                reference_type="response_draft",
                created_at=now - timedelta(hours=5),
            ),
        ]
        session.add_all(alerts)

        # 11. AI Response Draft
        session.add(
            AIResponse(
                id="resp_seed_1",
                business_id=biz_id,
                mention_id="men_seed_2",
                original_review="Paneer tikka was wonderfully smoky and fresh. However, the wait time on a Saturday evening was almost 45 minutes despite reservations. Service was slow.",
                generated_response=(
                    "Dear Anand, thank you for your candid feedback and for appreciating our smoky paneer tikka. "
                    "We sincerely regret that the wait time during Saturday evening disrupted your dining experience. "
                    "We have reviewed our table management protocols to avoid future delays. Please reach out to "
                    "concierge@spicesymphony.in so we can extend a personal VIP table reservation on your next visit."
                ),
                tone="empathetic",
                status="drafted",
                created_at=now - timedelta(hours=5),
            )
        )

        await session.commit()
        print("[Seed] Successfully populated demo data for 'Spice Symphony'!")
        print("[Seed] Login Credentials: adira@spicesymphony.com / Password123!")


if __name__ == "__main__":
    asyncio.run(seed_database())
