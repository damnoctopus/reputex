"""Deterministic 75-mention cross-platform mock dataset for offline development and testing."""
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from app.acquisition.base import AcquisitionProvider, RawMentionRecord


class MockAcquisitionProvider(AcquisitionProvider):
    """Produces a rich, realistic 75-mention dataset across Google, Reddit, and X."""

    def acquire(
        self,
        business_name: str,
        location: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        last_scan_time: Optional[datetime] = None,
    ) -> List[RawMentionRecord]:
        name = business_name or "Spice Symphony"
        records: List[RawMentionRecord] = []
        now = datetime.now(timezone.utc)

        # ── 1. Google Reviews (35 mentions) ──
        # 15 Genuine Positive Reviews
        positive_snippets = [
            f"We had a great dinner at {name}! The staff was courteous and the atmosphere was welcoming.",
            f"Delicious food and excellent presentation at {name}. Will definitely be returning with family.",
            f"Consistent high quality at {name}. Their signature dishes are always cooked to perfection.",
            f"Wonderful experience celebrating our anniversary at {name}. Highly recommended!",
            f"Five stars for {name}. Prompt service and clean dining area.",
            f"Loved the spices and rich flavors at {name}. One of the top spots in the area.",
            f"The desserts at {name} are unmatched. Great culinary creativity.",
            f"Friendly greeting from the host, quick seating, and top tier hospitality at {name}.",
            f"Great value lunch specials at {name}. Very fresh ingredients.",
            f"Comfortable seating, attentive servers, and wonderful music at {name}.",
            f"Outstanding flavors! {name} never fails to impress our out-of-town guests.",
            f"Crisp, clean, and delicious. {name} has become our weekly dinner tradition.",
            f"Very accommodating with dietary restrictions at {name}. Knowledgeable staff.",
            f"Super fast delivery and food arrived hot from {name}!",
            f"Authentic flavors and generous portions at {name}. 10/10 experience.",
        ]
        for i, text in enumerate(positive_snippets):
            records.append(RawMentionRecord(
                platform="google",
                external_id=f"goog_pos_{i+1}",
                content=text,
                author=f"Customer_G{i+1}",
                rating=5.0 if i % 3 != 0 else 4.0,
                source_url=f"https://maps.google.com/?cid=mock_goog_pos_{i+1}",
                published_at=now - timedelta(days=14 - i),
                engagement={"likes": i + 1},
            ))

        # 14 Customer Service & Wait Times Complaints
        complaint_snippets = [
            f"Waited over 45 minutes for our table at {name} despite having a reservation. Slow service.",
            f"The staff ignored us for 20 minutes before even taking our drink orders at {name}. Rude staff!",
            f"Terrible service at {name}. Our waiter had a major attitude and rolled his eyes.",
            f"Slow service and cold food. Nobody helped us when we complained to the manager at {name}.",
            f"The host at {name} was completely dismissive. Very unprofessional behavior.",
            f"Employees were rude when we asked to split the bill at {name}. Awful experience.",
            f"Service was terrible! The waiter forgot half our order at {name}.",
            f"Staff behavior at {name} was so disrespectful. We will not be returning.",
            f"Waited an hour for entrees at {name}. Nobody apologized for the delay.",
            f"The waitress at {name} was visibly irritated whenever we asked for water refills.",
            f"Unfriendly staff, slow service, and high prices at {name}. Skip this place.",
            f"Disorganized front desk at {name}. Lost our reservation and made us wait in the rain.",
            f"Nobody helped us for 15 minutes after we sat down at {name}. Disappointing.",
            f"Manager at {name} argued with us over a clearly wrong order. Awful customer service.",
        ]
        for i, text in enumerate(complaint_snippets):
            records.append(RawMentionRecord(
                platform="google",
                external_id=f"goog_neg_{i+1}",
                content=text,
                author=f"Reviewer_G{i+1}",
                rating=1.0 if i % 2 == 0 else 2.0,
                source_url=f"https://maps.google.com/?cid=mock_goog_neg_{i+1}",
                published_at=now - timedelta(days=10 - (i // 2)),
                engagement={"likes": (i + 1) * 2},
            ))

        # 6 Coordinated Suspicious 5-Star Reviews (Manipulation Cluster)
        # Posted within a 35-minute burst with nearly identical templated superlatives
        cluster_time = now - timedelta(days=2, hours=3)
        for i in range(6):
            records.append(RawMentionRecord(
                platform="google",
                external_id=f"goog_cluster_{i+1}",
                content=f"Best place in town! Highly recommended to all. Incredible phenomenal food at {name}! 5 stars! Simply the best.",
                author=f"User_{1000 + i}",
                rating=5.0,
                source_url=f"https://maps.google.com/?cid=mock_goog_cluster_{i+1}",
                published_at=cluster_time + timedelta(minutes=i * 6),
                engagement={"likes": 0},
                metadata={"cluster_candidate": True},
            ))

        # ── 2. Reddit Mentions (22 mentions) ──
        # Discussions about hidden fees, billing surcharges, and customer service
        reddit_posts = [
            f"Beware of hidden fees on your bill at {name}. They added an unexpected 18% service charge plus extra fees!",
            f"Anyone else notice {name} adds mandatory gratuity without mentioning it on the menu? Hidden surcharge!",
            f"Check your receipt at {name}! They charged me for two cocktails I never ordered and refused to refund.",
            f"Disputed an incorrect charge from {name}. Their billing department was completely unhelpful.",
            f"Hidden charge of  on our bill at {name} for 'kitchen wellness fee'. Deceptive billing practice.",
            f"The pricing at {name} is getting out of hand with all these hidden surcharge add-ons.",
            f"Had an awful experience with rude staff at {name} last weekend. Thread here to share your thoughts.",
            f"Can confirm, {name} service has deteriorated significantly this year. Staff ignored us completely.",
            f"Avoid {name} on Friday nights. Massive wait times and disorganized servers.",
            f"Why is the manager at {name} always so aggressive with customers who question the bill?",
            f"PSA: {name} charged a credit card fee on top of sales tax and auto-grat. Watch out.",
            f"Left a bad review about rude staff at {name} and the owner sent a hostile reply.",
            f"Is {name} still good? Last time we visited, the food quality was mediocre and cold.",
            f"Discussion: Alternatives to {name} in the neighborhood with honest billing?",
            f"Ordered takeout from {name} and items were missing. No refund offered.",
            f"The service at {name} used to be stellar, now it is slow service and uninterested waitstaff.",
            f"Another complaint about {name}: waited 50 minutes past reservation time.",
            f"Unfriendly staff behavior seems to be a common trend at {name} based on recent posts.",
            f"Check your credit card statements after dining at {name}. Duplicate charge reported!",
            f"Surprised by the negative changes at {name}. It used to be our favorite spot.",
            f"Billing issues at {name} are getting ridiculous. How is this legal?",
            f"Honestly had a neutral experience at {name}, food was fine but wait times were long.",
        ]
        for i, text in enumerate(reddit_posts):
            records.append(RawMentionRecord(
                platform="reddit",
                external_id=f"red_{i+1}",
                content=text,
                author=f"redditor_{i+1}",
                source_url=f"https://reddit.com/r/local/comments/mock_red_{i+1}",
                published_at=now - timedelta(days=7 - (i // 4)),
                engagement={"upvotes": (i + 1) * 8, "comments": (i + 1) * 3},
            ))

        # ── 3. X / Twitter Mentions (18 mentions) ──
        # Recent viral spike of negative mentions alleging severe food poisoning / contamination
        # Clustered in the last 48 hours to trigger Crisis Early Warning
        crisis_time = now - timedelta(hours=36)
        x_posts = [
            f"Avoid {name} right now! Three people in our group got severe food poisoning after dinner last night. Sick all night!",
            f"Reporting {name} to the health department today. Multiple people hospitalized with food poisoning symptoms!",
            f"Has anyone else gotten violently sick after eating at {name} this week? Severe food safety contamination!",
            f"Do NOT eat at {name}! Undercooked chicken resulted in severe bacterial infection and vomit.",
            f"Health department needs to inspect {name} immediately. Food poisoning outbreak reported by multiple tables.",
            f"Wife and I are both in urgent care after eating the seafood at {name}. Unacceptable food safety issue!",
            f"Seeing multiple tweets about food poisoning from {name} over the last 24 hours. Stay away!",
            f"Called {name} about getting sick and management hung up on me. Complete lack of accountability!",
            f"Health hazard at {name}. Food was visibly undercooked and smelled off.",
            f"Food safety crisis brewing at {name}. Half our party is down with severe nausea and fever.",
            f"Terrible news about {name}. Hopefully the local authorities investigate this food contamination.",
            f"Can confirm the food poisoning rumors about {name}. Worst night of my life.",
            f"Staff behavior at {name} when confronted about the spoiled food was disgraceful.",
            f"{name} customer service refuses to acknowledge the food poisoning reports.",
            f"Local foodies beware: contamination risk reported at {name}. Multiple victims posting.",
            f"How is {name} still open after so many people got sick this weekend?",
            f"Trending locally: food poisoning reports tied to {name}. Avoid!",
            f"Devastated to hear about the sickness from {name}. Hope everyone recovers quickly.",
        ]
        for i, text in enumerate(x_posts):
            records.append(RawMentionRecord(
                platform="twitter",
                external_id=f"tw_{i+1}",
                content=text,
                author=f"user_tw_{i+1}",
                source_url=f"https://x.com/user_tw_{i+1}/status/mock_{i+1}",
                published_at=crisis_time + timedelta(hours=i * 2),
                engagement={"retweets": (i + 1) * 15, "likes": (i + 1) * 45},
            ))

        return records
