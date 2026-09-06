"""Unit tests for PlatformQueryBuilder."""

from app.integrations.query_builder import PlatformQueryBuilder
from app.models.business import BrandKeyword


def test_query_builder_google_syntax():
    """Verify Google Places / search query structure."""
    keywords = [
        BrandKeyword(keyword="biryani"),
        BrandKeyword(keyword="fine dining"),
    ]
    query = PlatformQueryBuilder.build_query(
        platform="Google",
        business_name="Spice Symphony",
        keywords=keywords,
        location="Indiranagar, Bangalore",
    )
    assert query.platform == "Google"
    assert '"Spice Symphony"' in query.query_string
    assert "Indiranagar, Bangalore" in query.query_string
    assert "biryani" in query.query_string
    assert query.filters.get("location") == "Indiranagar, Bangalore"


def test_query_builder_reddit_syntax():
    """Verify Reddit boolean OR search query structure."""
    keywords = ["mutton biryani", "catering service"]
    query = PlatformQueryBuilder.build_query(
        platform="Reddit",
        business_name="Spice Symphony",
        keywords=keywords,
        location="Bangalore, Karnataka",
        aliases=["SpiceSymphonyBlr"],
    )
    assert query.platform == "Reddit"
    # Expected boolean OR grouping
    assert " OR " in query.query_string
    assert '"Spice Symphony"' in query.query_string
    assert '"mutton biryani"' in query.query_string
    assert "SpiceSymphonyBlr" in query.query_string
    assert query.filters.get("suggested_subreddit") == "r/bangalore"


def test_query_builder_x_twitter_syntax():
    """Verify X/Twitter search query with retweet exclusion and language filter."""
    keywords = ["best food", "weekend brunch"]
    query = PlatformQueryBuilder.build_query(
        platform="X",
        business_name="Spice Symphony",
        keywords=keywords,
        aliases=["@spicesymphony"],
    )
    assert query.platform == "X"
    assert "-is:retweet" in query.query_string
    assert "lang:en" in query.query_string
    assert " OR " in query.query_string
    assert query.filters.get("exclude_retweets") is True
    assert query.filters.get("lang") == "en"


def test_query_builder_google_ai_overview_syntax():
    """Verify Google AI Overview structured query."""
    query = PlatformQueryBuilder.build_query(
        platform="Google AI Overview",
        business_name="Spice Symphony",
        keywords=["reputation", "hygiene"],
        location="Indiranagar",
    )
    assert query.platform == "Google AI Overview"
    assert '"Spice Symphony"' in query.query_string
    assert "Indiranagar" in query.query_string
    assert "customer reviews and reputation" in query.query_string


def test_query_builder_empty_keywords():
    """Verify query builder safely generates default query when no keywords are passed."""
    query = PlatformQueryBuilder.build_query(
        platform="Reddit",
        business_name="Solo Business",
        keywords=[],
    )
    assert query.platform == "Reddit"
    assert "Solo Business" in query.query_string


def test_query_builder_whitespace_and_deduplication():
    """Verify whitespace stripping and case-insensitive keyword deduplication."""
    tokens = [
        "  Spice Symphony  ",
        "spice symphony",
        "SPICE SYMPHONY",
        "  Biryani   Delight  ",
    ]
    query = PlatformQueryBuilder.build_query(
        platform="Google",
        business_name="Spice Symphony",
        keywords=tokens,
    )
    # Ensure 'Spice Symphony' is not duplicated in keywords_used
    assert len([k for k in query.keywords_used if k.lower() == "spice symphony"]) == 1
    assert "Biryani Delight" in query.keywords_used
