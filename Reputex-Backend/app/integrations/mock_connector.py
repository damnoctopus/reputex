"""High-fidelity deterministic MockPlatformConnector for local development and offline testing.

Exercises the real query builder and emits raw platform records matching the domain contract.
Provides a comprehensive 75-mention dataset:
- Google (40 mentions): positive, customer service issues, billing issues, 5-star manipulation cluster, food poisoning surge
- Reddit (15 mentions): recommendations, wait time discussions, billing transparency, viral crisis threads
- X / Twitter (20 mentions): foodie praise, queue complaints, bill surcharges, viral retweet storm
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

    def _build_dataset(self, business_name: str, now: datetime, meta_base: dict[str, Any]) -> list[RawMentionRecord]:
        records: list[RawMentionRecord] = []

        # ═════════════════════════════════════════════════════════════════════
        # 1. GOOGLE REVIEWS (40 mentions)
        # ═════════════════════════════════════════════════════════════════════

        # A. 20 Genuine Positive Reviews (4.0 - 5.0 stars)
        positive_google_reviews = [
            ("Ananya Roy", "Exceptional culinary journey at {biz}! The chef personally checked on our table. Best dining spot in town hands down.", 5.0, 25),
            ("Siddharth Jain", "Clean tables, fast billing, and courteous valets at {biz}. Will surely visit again with family.", 5.0, 24),
            ("Pooja Hegde", "The dal makhani and garlic naan are to die for! Wonderful family dining ambience.", 5.0, 23),
            ("Kavita Nair", "Celebrated our 10th wedding anniversary here. The staff made it truly memorable with complimentary dessert.", 5.0, 22),
            ("Aditya Verma", "Top notch North Indian cuisine. Tandoori chicken was cooked to perfection and juicy.", 4.5, 21),
            ("Meera Joshi", "Great lunch buffet with wide variety of vegetarian and non-veg curries. Courteous staff.", 4.0, 20),
            ("Rohan Desai", "Superb cocktail menu and lovely outdoor seating. Chicken tikka was delightfully smoky.", 5.0, 19),
            ("Suresh Reddy", "Consistent quality every single time we visit. Service is prompt and welcoming.", 4.5, 18),
            ("Divya Menon", "A real gem for authentic flavors. Loved the paneer butter masala and biryani aroma.", 5.0, 17),
            ("Kiran Patel", "Brought our corporate clients here for dinner. Everyone left thoroughly impressed by the hospitality.", 5.0, 16),
            ("Sunita Rao", "Very flavorful food and lovely presentation. Kids enjoyed the mocktails.", 4.0, 15),
            ("Deepak Sharma", "Crispy butter naan and tender lamb shank curry. Worth every rupee.", 5.0, 14),
            ("Arjun Singhal", "Warm atmosphere, quick table turnaround and very polite servers.", 4.5, 13),
            ("Neha Kapoor", "Our favorite weekend spot in the city. The gulab jamun with rabdi is unbeatable.", 5.0, 12),
            ("Manish Agarwal", "Great acoustic design and ambient music that allows comfortable table conversation.", 4.0, 11),
            ("Priyanka Das", "Fresh ingredients and generous portion sizes. High standards of dining.", 4.5, 10),
            ("Naveen Kumar", "The head server was very attentive to our nut allergy instructions.", 5.0, 9),
            ("Bhavna Shah", "Exceeded expectations! Beautiful decor and stellar tandoori platters.", 5.0, 8),
            ("Vivek Pillai", "Smooth reservation experience and flavorful mocktails.", 4.5, 7),
            ("Tanvi Sen", "Hearty meal with friends. The biryani pot was fragrant and perfectly spiced.", 5.0, 6),
        ]
        for idx, (author, text_tmpl, rating, days_ago) in enumerate(positive_google_reviews):
            records.append(
                RawMentionRecord(
                    platform="Google",
                    external_id=f"goog_pos_{idx+1:02d}",
                    source_url=f"https://maps.google.com/?cid=123456&rev=pos_{idx+1:02d}",
                    title="Great Experience",
                    content=text_tmpl.format(biz=business_name),
                    author=author,
                    author_id=f"user_goog_pos_{idx+1:02d}",
                    author_avatar="https://lh3.googleusercontent.com/a/sample_avatar.jpg",
                    published_at=now - timedelta(days=days_ago, hours=idx),
                    collected_at=now,
                    rating=rating,
                    engagement={"likes": 4 + idx % 6, "shares": 0, "comments": 1},
                    metadata={**meta_base, "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4"},
                    raw_payload={"review_id": f"goog_pos_{idx+1:02d}", "stars": rating},
                )
            )

        # B. 6 Customer Service Issues (Wait times, slow service, 1.0 - 2.0 stars)
        service_google_reviews = [
            ("Priya Sharma", "Decent ambience, but mocktails took almost 45 minutes to arrive. Slow service and we waited forever for our table.", 2.0, 5),
            ("Vikram Sethi", "Food tastes authentic but preparation takes a long time at {biz}. Waited 50 minutes during dinner rush.", 1.5, 4),
            ("Amit Trivedi", "Extremely slow service. The waiters ignored us completely for 30 minutes after taking our order.", 1.0, 3),
            ("Nisha Gupta", "Table reservation was completely lost by the receptionist. Had to wait in line for 40 minutes with elderly parents.", 1.0, 3),
            ("Rahul Bakshi", "Terrible delay in serving main course. Cold food arrived after an hour of waiting.", 2.0, 2),
            ("Simran Kaur", "Staff was dismissive and rude when we pointed out the 45-minute delay on our drinks.", 1.0, 2),
        ]
        for idx, (author, text_tmpl, rating, days_ago) in enumerate(service_google_reviews):
            records.append(
                RawMentionRecord(
                    platform="Google",
                    external_id=f"goog_serv_{idx+1:02d}",
                    source_url=f"https://maps.google.com/?cid=123456&rev=serv_{idx+1:02d}",
                    title="Service Delay",
                    content=text_tmpl.format(biz=business_name),
                    author=author,
                    author_id=f"user_goog_serv_{idx+1:02d}",
                    author_avatar=None,
                    published_at=now - timedelta(days=days_ago, hours=idx * 2),
                    collected_at=now,
                    rating=rating,
                    engagement={"likes": 7 + idx * 2, "shares": 1, "comments": 2},
                    metadata={**meta_base, "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4"},
                    raw_payload={"review_id": f"goog_serv_{idx+1:02d}", "stars": rating},
                )
            )

        # C. 4 Billing Issues (Hidden fees, price gouging, 1.0 - 2.0 stars)
        billing_google_reviews = [
            ("Harish Bhat", "Watch out your bill! Unexpected surcharge and hidden fee added without consent at {biz}.", 1.0, 8),
            ("Gaurav Chopra", "Refused to refund an overcharged item that was never served. Total rip off and billing issue.", 1.5, 7),
            ("Sneha Kulkarni", "Extra charge of 12% mandatory service fee added and manager refused to remove it when asked.", 1.0, 6),
            ("Ramesh Iyer", "Overcharging customers on bottled water and mocktails. Too expensive and deceptive pricing.", 2.0, 5),
        ]
        for idx, (author, text_tmpl, rating, days_ago) in enumerate(billing_google_reviews):
            records.append(
                RawMentionRecord(
                    platform="Google",
                    external_id=f"goog_bill_{idx+1:02d}",
                    source_url=f"https://maps.google.com/?cid=123456&rev=bill_{idx+1:02d}",
                    title="Billing Dispute",
                    content=text_tmpl.format(biz=business_name),
                    author=author,
                    author_id=f"user_goog_bill_{idx+1:02d}",
                    author_avatar=None,
                    published_at=now - timedelta(days=days_ago, hours=idx * 3),
                    collected_at=now,
                    rating=rating,
                    engagement={"likes": 11 + idx, "shares": 2, "comments": 3},
                    metadata={**meta_base, "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4"},
                    raw_payload={"review_id": f"goog_bill_{idx+1:02d}", "stars": rating},
                )
            )

        # D. 5-Star Coordinated Review Manipulation Cluster (5 reviews, identical template text within 15 minutes)
        cluster_template = "Best place in the world! Ten stars if i could, absolute perfection must visit for everyone!"
        for idx in range(5):
            records.append(
                RawMentionRecord(
                    platform="Google",
                    external_id=f"goog_clust_{idx+1:02d}",
                    source_url=f"https://maps.google.com/?cid=123456&rev=clust_{idx+1:02d}",
                    title="Perfection",
                    content=cluster_template,
                    author=f"ReviewBot_{idx+1:02d}",
                    author_id=f"user_bot_{idx+1:02d}",
                    author_avatar=None,
                    published_at=now - timedelta(days=2, minutes=idx * 4),  # all within 16 mins
                    collected_at=now,
                    rating=5.0,
                    engagement={"likes": 0, "shares": 0, "comments": 0},
                    metadata={**meta_base, "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4", "synthetic": True},
                    raw_payload={"review_id": f"goog_clust_{idx+1:02d}", "stars": 5},
                )
            )

        # E. 5 Food Poisoning & Health Crisis Reviews (recent 6-18 hours ago, 1.0 star)
        crisis_google_reviews = [
            ("Aakash Mittal", "Severe food poisoning after dinner at {biz}! Spent the whole night vomiting. Unclean kitchen!", 1.0, 6),
            ("Radhika Merchant", "Got terrible stomach infection and fever after eating seafood curry here yesterday. Dangerous hygiene!", 1.0, 9),
            ("Rohit Saxena", "My entire family fell sick with vomiting and food poisoning after visiting {biz}. Filthy restrooms too.", 1.0, 12),
            ("Smita Paul", "Food tasted spoiled and caused violent stomach cramps for both of us. Do not eat here!", 1.0, 15),
            ("Zoya Akhtar", "Unsanitary and contaminated food. The chicken smelled foul and we woke up sick.", 1.0, 18),
        ]
        for idx, (author, text_tmpl, rating, hours_ago) in enumerate(crisis_google_reviews):
            records.append(
                RawMentionRecord(
                    platform="Google",
                    external_id=f"goog_cris_{idx+1:02d}",
                    source_url=f"https://maps.google.com/?cid=123456&rev=cris_{idx+1:02d}",
                    title="Health Hazard",
                    content=text_tmpl.format(biz=business_name),
                    author=author,
                    author_id=f"user_goog_cris_{idx+1:02d}",
                    author_avatar=None,
                    published_at=now - timedelta(hours=hours_ago),
                    collected_at=now,
                    rating=rating,
                    engagement={"likes": 28 + idx * 5, "shares": 6, "comments": 9},
                    metadata={**meta_base, "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4"},
                    raw_payload={"review_id": f"goog_cris_{idx+1:02d}", "stars": rating},
                )
            )

        # ═════════════════════════════════════════════════════════════════════
        # 2. REDDIT DISCUSSIONS (15 mentions)
        # ═════════════════════════════════════════════════════════════════════

        # A. 5 Positive Recommendations
        reddit_pos = [
            ("u/bangalore_foodie", "Weekly Bangalore Food Thread", "Shoutout to {biz} for catering our team lunch! Fresh naan, tender butter chicken and on-time delivery.", 4.5, 14),
            ("u/spice_connoisseur", "Best Biryani in Indiranagar?", "Definitely check out {biz}. Their dum biryani is authentic and consistent.", 5.0, 12),
            ("u/techie_gourmet", "Hidden gems around town", "{biz} has great seating and reliable North Indian curries. Worth visiting with colleagues.", 4.0, 10),
            ("u/dosa_and_curry", "Friday Dinner Suggestions", "Went to {biz} last night. Ambiance was 10/10 and staff was very polite.", 4.5, 8),
            ("u/hungry_coder", "North Indian Food thread", "Butter chicken at {biz} is legit one of the best in Bangalore.", 5.0, 6),
        ]
        for idx, (author, title, text_tmpl, rating, days_ago) in enumerate(reddit_pos):
            records.append(
                RawMentionRecord(
                    platform="Reddit",
                    external_id=f"red_pos_{idx+1:02d}",
                    source_url=f"https://reddit.com/r/bangalore/comments/pos_{idx+1:02d}",
                    title=title,
                    content=text_tmpl.format(biz=business_name),
                    author=author,
                    author_id=f"user_red_pos_{idx+1:02d}",
                    author_avatar=None,
                    published_at=now - timedelta(days=days_ago),
                    collected_at=now,
                    rating=rating,
                    engagement={"likes": 45 + idx * 8, "shares": 5, "comments": 14},
                    metadata={**meta_base, "subreddit": "r/bangalore"},
                    raw_payload={"id": f"red_pos_{idx+1:02d}", "ups": 45 + idx * 8},
                )
            )

        # B. 4 Customer Service Complaints (Wait times, queue delays)
        reddit_serv = [
            ("u/blr_commuter", "Never going back to {biz}", "Waited 50 minutes for a table even with prior booking. Manager was arrogant and rude. Slow service!", 1.5, 5),
            ("u/weekend_diner", "Peak hour nightmare at {biz}", "Terrible line and queue delay. Waited forever for drinks and food arrived cold.", 1.0, 4),
            ("u/indiranagar_local", "Overcrowded and chaotic", "{biz} took 40 minutes for our main course. The floor manager completely ignored us.", 2.0, 3),
            ("u/food_critic_99", "Declining service at {biz}", "Service quality has seriously declined. Took so long to get our bill and water.", 2.0, 2),
        ]
        for idx, (author, title, text_tmpl, rating, days_ago) in enumerate(reddit_serv):
            records.append(
                RawMentionRecord(
                    platform="Reddit",
                    external_id=f"red_serv_{idx+1:02d}",
                    source_url=f"https://reddit.com/r/bangalore/comments/serv_{idx+1:02d}",
                    title=title,
                    content=text_tmpl.format(biz=business_name),
                    author=author,
                    author_id=f"user_red_serv_{idx+1:02d}",
                    author_avatar=None,
                    published_at=now - timedelta(days=days_ago),
                    collected_at=now,
                    rating=rating,
                    engagement={"likes": 65 + idx * 12, "shares": 8, "comments": 28},
                    metadata={**meta_base, "subreddit": "r/bangalore"},
                    raw_payload={"id": f"red_serv_{idx+1:02d}", "ups": 65 + idx * 12},
                )
            )

        # C. 3 Billing Complaints (Hidden fees, surcharges)
        reddit_bill = [
            ("u/consumer_rights_blr", "Deceptive billing at {biz}", "They add an extra charge and service fee. When questioned, they refused to refund or remove it. Price gouging.", 1.0, 7),
            ("u/frugal_eats", "Hidden surcharge alert", "Beware guys, {biz} adds sneaky charges on food and drinks. Total ripoff.", 1.0, 6),
            ("u/bangalore_lawyer", "Illegal mandatory service charge", "{biz} is forcing customers to pay extra fees. Disputed the bill with management.", 1.5, 5),
        ]
        for idx, (author, title, text_tmpl, rating, days_ago) in enumerate(reddit_bill):
            records.append(
                RawMentionRecord(
                    platform="Reddit",
                    external_id=f"red_bill_{idx+1:02d}",
                    source_url=f"https://reddit.com/r/bangalore/comments/bill_{idx+1:02d}",
                    title=title,
                    content=text_tmpl.format(biz=business_name),
                    author=author,
                    author_id=f"user_red_bill_{idx+1:02d}",
                    author_avatar=None,
                    published_at=now - timedelta(days=days_ago),
                    collected_at=now,
                    rating=rating,
                    engagement={"likes": 88 + idx * 15, "shares": 14, "comments": 42},
                    metadata={**meta_base, "subreddit": "r/bangalore"},
                    raw_payload={"id": f"red_bill_{idx+1:02d}", "ups": 88 + idx * 15},
                )
            )

        # D. 3 Viral Crisis Posts (Food poisoning surge in last 24h)
        reddit_crisis = [
            ("u/sick_in_bangalore", "Food Poisoning Outbreak at {biz}??", "Ate at {biz} yesterday night and down with violent vomiting and fever. Has anyone else gotten sick from their food?", 1.0, 8),
            ("u/doctor_foodie", "PSA: Contaminated food at {biz}", "Admitted two patients this morning with severe food poisoning after dinner at {biz}. Kitchen hygiene looks deeply compromised.", 1.0, 14),
            ("u/blr_food_patrol", "Avoid {biz} this weekend", "Multiple reports on reddit and twitter of acute gastroenteritis after dining at {biz}. Major health alert!", 1.0, 20),
        ]
        for idx, (author, title, text_tmpl, rating, hours_ago) in enumerate(reddit_crisis):
            records.append(
                RawMentionRecord(
                    platform="Reddit",
                    external_id=f"red_cris_{idx+1:02d}",
                    source_url=f"https://reddit.com/r/bangalore/comments/cris_{idx+1:02d}",
                    title=title,
                    content=text_tmpl.format(biz=business_name),
                    author=author,
                    author_id=f"user_red_cris_{idx+1:02d}",
                    author_avatar=None,
                    published_at=now - timedelta(hours=hours_ago),
                    collected_at=now,
                    rating=rating,
                    engagement={"likes": 195 + idx * 45, "shares": 38, "comments": 85},
                    metadata={**meta_base, "subreddit": "r/bangalore", "viral": True},
                    raw_payload={"id": f"red_cris_{idx+1:02d}", "ups": 195 + idx * 45},
                )
            )

        # ═════════════════════════════════════════════════════════════════════
        # 3. X / TWITTER POSTS (20 mentions)
        # ═════════════════════════════════════════════════════════════════════

        # A. 8 Positive Tweets
        x_pos = [
            ("@foodie_bangalore", "{biz} in Indiranagar has the crispiest butter garlic naan in the city! Service was top notch. Highly recommended. ⭐⭐⭐⭐⭐", 5.0, 20),
            ("@bangalore_bites", "Delicious lunch at {biz}. Dal makhani was velvety and full of flavor. 10/10 dining.", 5.0, 18),
            ("@chef_insights", "Great hospitality seen at {biz}. Staff was well trained in allergen management.", 5.0, 16),
            ("@travel_diner", "Wonderful ambience at {biz}. Perfect spot for late evening cocktails with friends.", 4.5, 14),
            ("@curry_lover", "The paneer tikka platter at {biz} is truly unmatched. Always our go-to spot.", 5.0, 12),
            ("@silicon_foodie", "Team lunch at {biz} was fantastic. Smooth table setup and prompt refills.", 4.5, 10),
            ("@taste_buds_in", "Exceptional flavors at {biz}. Chef definitely knows his spices!", 5.0, 8),
            ("@blrcafe_hopper", "Lovely weekend meal at {biz}. Great desserts and relaxing decor.", 4.0, 6),
        ]
        for idx, (author, text_tmpl, rating, days_ago) in enumerate(x_pos):
            records.append(
                RawMentionRecord(
                    platform="X",
                    external_id=f"tw_pos_{idx+1:02d}",
                    source_url=f"https://x.com/{author.lstrip('@')}/status/pos_{idx+1:02d}",
                    title=None,
                    content=text_tmpl.format(biz=business_name),
                    author=author,
                    author_id=f"user_tw_pos_{idx+1:02d}",
                    author_avatar="https://pbs.twimg.com/profile_images/sample.jpg",
                    published_at=now - timedelta(days=days_ago),
                    collected_at=now,
                    rating=rating,
                    engagement={"likes": 32 + idx * 10, "shares": 6, "comments": 3},
                    metadata={**meta_base, "tweet_type": "review"},
                    raw_payload={"id": f"tw_pos_{idx+1:02d}", "like_count": 32 + idx * 10},
                )
            )

        # B. 4 Customer Service / Wait Time Tweets
        x_serv = [
            ("@angry_diner_blr", "Been standing in line for 45 minutes at {biz}. Manager refused to give a realistic wait time. Slow service and bad attitude!", 1.0, 5),
            ("@busy_exec", "@{biz} Waited forever for our order to arrive during dinner rush. Took 50 minutes for starters. Disappointing delay.", 1.5, 4),
            ("@weekend_out", "Table reservation was completely ignored at {biz}. Staff was unapologetic and rude.", 1.0, 3),
            ("@city_explorer_in", "Why does service take so long at {biz}? Over an hour to get our food on a weekday night.", 1.5, 2),
        ]
        for idx, (author, text_tmpl, rating, days_ago) in enumerate(x_serv):
            records.append(
                RawMentionRecord(
                    platform="X",
                    external_id=f"tw_serv_{idx+1:02d}",
                    source_url=f"https://x.com/{author.lstrip('@')}/status/serv_{idx+1:02d}",
                    title=None,
                    content=text_tmpl.format(biz=business_name),
                    author=author,
                    author_id=f"user_tw_serv_{idx+1:02d}",
                    author_avatar=None,
                    published_at=now - timedelta(days=days_ago),
                    collected_at=now,
                    rating=rating,
                    engagement={"likes": 48 + idx * 15, "shares": 12, "comments": 8},
                    metadata={**meta_base, "tweet_type": "complaint"},
                    raw_payload={"id": f"tw_serv_{idx+1:02d}", "like_count": 48 + idx * 15},
                )
            )

        # C. 3 Billing Surcharge Tweets
        x_bill = [
            ("@consumer_voice", "@{biz} What is this hidden fee and extra charge on the bill? Price gouging at its finest.", 1.0, 6),
            ("@tech_investor", "Disputed an overcharged bill at {biz} tonight. Beware guys, check every item before paying.", 1.0, 4),
            ("@frugal_traveller", "{biz} charging mandatory service surcharges on card payments. Totally illegal and rip off.", 1.0, 3),
        ]
        for idx, (author, text_tmpl, rating, days_ago) in enumerate(x_bill):
            records.append(
                RawMentionRecord(
                    platform="X",
                    external_id=f"tw_bill_{idx+1:02d}",
                    source_url=f"https://x.com/{author.lstrip('@')}/status/bill_{idx+1:02d}",
                    title=None,
                    content=text_tmpl.format(biz=business_name),
                    author=author,
                    author_id=f"user_tw_bill_{idx+1:02d}",
                    author_avatar=None,
                    published_at=now - timedelta(days=days_ago),
                    collected_at=now,
                    rating=rating,
                    engagement={"likes": 74 + idx * 20, "shares": 22, "comments": 15},
                    metadata={**meta_base, "tweet_type": "complaint"},
                    raw_payload={"id": f"tw_bill_{idx+1:02d}", "like_count": 74 + idx * 20},
                )
            )

        # D. 5 Viral Crisis Tweets & Retweets (Food poisoning crisis in past 24 hours)
        x_crisis = [
            ("@health_alert_in", "URGENT: Multiple diners hospitalised with severe food poisoning after dinner at {biz}. Kitchen contamination suspected! #BangaloreEats", 1.0, 5),
            ("@bangalore_times", "Outbreak alert: Over 15 patrons report violent sickness and food poisoning from {biz} Indiranagar branch. Health inspectors notified.", 1.0, 8),
            ("@viral_foodie_blr", "Do NOT eat at {biz}! My brother and I are on IV drips with bacterial infection after eating their chicken curry last night.", 1.0, 11),
            ("@food_safety_org", "Food safety advisory issued following severe gastrointestinal illnesses traced back to {biz}. Contaminated batch under investigation.", 1.0, 14),
            ("@city_journalist", "Breaking: Health authorities inspecting {biz} following public outcry over food poisoning cluster. Avoid this place!", 1.0, 17),
        ]
        for idx, (author, text_tmpl, rating, hours_ago) in enumerate(x_crisis):
            records.append(
                RawMentionRecord(
                    platform="X",
                    external_id=f"tw_cris_{idx+1:02d}",
                    source_url=f"https://x.com/{author.lstrip('@')}/status/cris_{idx+1:02d}",
                    title=None,
                    content=text_tmpl.format(biz=business_name),
                    author=author,
                    author_id=f"user_tw_cris_{idx+1:02d}",
                    author_avatar=None,
                    published_at=now - timedelta(hours=hours_ago),
                    collected_at=now,
                    rating=rating,
                    engagement={"likes": 280 + idx * 60, "shares": 110 + idx * 25, "comments": 65 + idx * 15},
                    metadata={**meta_base, "tweet_type": "crisis", "viral": True},
                    raw_payload={"id": f"tw_cris_{idx+1:02d}", "retweet_count": 110 + idx * 25, "like_count": 280 + idx * 60},
                )
            )

        return records

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

        all_records = self._build_dataset(business_name, now, meta_base)

        # Filter by platform if connector is configured for a specific one
        plat = self.platform_name.lower()
        if plat in ["google", "googleplaces", "google_reviews"]:
            return [r for r in all_records if r.platform.lower() == "google"]
        elif plat in ["reddit"]:
            return [r for r in all_records if r.platform.lower() == "reddit"]
        elif plat in ["twitter", "x"]:
            return [r for r in all_records if r.platform.lower() == "x"]
        elif plat in ["mockplatform", "mock"]:
            # Dedicated 10 distinct records for Phase 1 idempotency & deduplication contract
            return all_records[:10]

        # Return all 75 records for default / multi-platform scan
        return all_records

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
