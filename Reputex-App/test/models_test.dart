import 'package:flutter_test/flutter_test.dart';
import 'package:reputex_mobile/features/alerts/domain/models/alert_item.dart';
import 'package:reputex_mobile/features/auth/domain/models/user.dart';
import 'package:reputex_mobile/features/crisis/domain/models/crisis_event.dart';
import 'package:reputex_mobile/features/dashboard/domain/models/dashboard_summary.dart';
import 'package:reputex_mobile/features/fraud/domain/models/fraud_result.dart';
import 'package:reputex_mobile/features/mentions/domain/models/mention.dart';
import 'package:reputex_mobile/features/onboarding/domain/models/business.dart';
import 'package:reputex_mobile/features/responses/domain/models/response_draft.dart';
import 'package:reputex_mobile/features/sentiment/domain/models/sentiment_analytics.dart';

void main() {
  group('Freezed Domain Models Serialization', () {
    test('User model parses and serializes correctly', () {
      final json = {
        'id': 'usr_1',
        'email': 'adira@spicesymphony.com',
        'full_name': 'Adithya R',
        'created_at': '2026-01-01T00:00:00.000Z',
      };

      final user = User.fromJson(json);
      expect(user.id, 'usr_1');
      expect(user.email, 'adira@spicesymphony.com');
      expect(user.fullName, 'Adithya R');
      expect(user.toJson()['email'], 'adira@spicesymphony.com');
    });

    test('Business model parses correctly', () {
      final json = {
        'id': 'biz_1',
        'name': 'Spice Symphony',
        'category': 'Restaurant',
        'website': 'https://spicesymphony.com',
        'location': 'Indiranagar, Bengaluru',
        'keywords': [
          {'id': 'k1', 'keyword': 'Spice Symphony', 'is_primary': true},
        ],
        'monitored_platforms': ['reddit', 'google_news'],
      };

      final business = Business.fromJson(json);
      expect(business.id, 'biz_1');
      expect(business.name, 'Spice Symphony');
      expect(business.keywords.first.keyword, 'Spice Symphony');
      expect(business.monitoredPlatforms.length, 2);
    });

    test('Mention model parses correctly', () {
      final json = {
        'id': 'm1',
        'platform': 'reddit',
        'author': 'FoodieBlr',
        'content': 'Great biryani and ambiance!',
        'timestamp': '2026-03-01T12:00:00.000Z',
        'sentiment': 'positive',
        'sentiment_score': 0.85,
        'url': 'https://reddit.com/r/bangalore/123',
        'rating': 5.0,
      };

      final mention = Mention.fromJson(json);
      expect(mention.id, 'm1');
      expect(mention.sentiment, 'positive');
      expect(mention.sentimentScore, 0.85);
      expect(mention.author, 'FoodieBlr');
    });

    test('FraudResult model parses correctly', () {
      final json = {
        'mention_id': 'm1',
        'is_fraudulent': false,
        'confidence': 0.95,
        'risk_level': 'low',
        'reasons': ['Account age > 2 years'],
      };

      final fraud = FraudResult.fromJson(json);
      expect(fraud.mentionId, 'm1');
      expect(fraud.isFraudulent, false);
      expect(fraud.riskLevel, 'low');
      expect(fraud.reasons.length, 1);
    });

    test('CrisisEvent model parses correctly', () {
      final json = {
        'id': 'cr_1',
        'title': 'Viral negative thread',
        'summary': 'Sudden spike in food poisoning claims',
        'severity': 'high',
        'status': 'active',
        'trigger_reason': 'Food poisoning claims',
        'started_at': '2026-03-01T10:00:00.000Z',
        'affected_platforms': ['reddit', 'x'],
        'suggested_actions': ['Issue public clarification immediately'],
      };

      final crisis = CrisisEvent.fromJson(json);
      expect(crisis.id, 'cr_1');
      expect(crisis.severity, 'high');
      expect(crisis.status, 'active');
      expect(crisis.affectedPlatforms, contains('reddit'));
    });

    test('AlertItem model parses correctly', () {
      final json = {
        'id': 'alt_1',
        'type': 'crisis',
        'title': 'Crisis Alert',
        'message': 'Negative mention surge detected',
        'timestamp': '2026-03-01T10:30:00.000Z',
        'is_read': false,
      };

      final alert = AlertItem.fromJson(json);
      expect(alert.id, 'alt_1');
      expect(alert.type, 'crisis');
      expect(alert.isRead, false);
    });

    test('ResponseDraft model parses correctly', () {
      final json = {
        'id': 'resp_1',
        'mention_id': 'm1',
        'original_review': 'Great biryani and ambiance!',
        'generated_response': 'Thank you for your warm feedback!',
        'tone': 'professional',
        'status': 'draft',
        'created_at': '2026-03-01T11:00:00.000Z',
      };

      final draft = ResponseDraft.fromJson(json);
      expect(draft.id, 'resp_1');
      expect(draft.tone, 'professional');
      expect(draft.status, 'draft');
    });

    test('DashboardSummary model parses correctly', () {
      final json = {
        'reputation_score': {
          'current_score': 82.0,
          'change_7d': 3.5,
          'tier': 'Good',
        },
        'sentiment_distribution': {
          'positive': 65,
          'neutral': 20,
          'negative': 15,
          'positive_percentage': 0.65,
          'neutral_percentage': 0.20,
          'negative_percentage': 0.15,
        },
        'sentiment_trends': [
          {'date': '2026-03-01', 'score': 80.0, 'mention_count': 10},
        ],
        'platform_statistics': [
          {'platform': 'reddit', 'mention_count': 15, 'average_sentiment': 0.7},
        ],
        'total_mentions': 120,
        'pending_alerts_count': 2,
        'active_crisis_count': 0,
      };

      final summary = DashboardSummary.fromJson(json);
      expect(summary.reputationScore.currentScore, 82.0);
      expect(summary.totalMentions, 120);
      expect(summary.sentimentDistribution.positive, 65);
    });

    test('SentimentAnalytics model parses correctly', () {
      final json = {
        'distribution': {
          'positive': 65,
          'neutral': 20,
          'negative': 15,
          'positive_percentage': 0.65,
          'neutral_percentage': 0.20,
          'negative_percentage': 0.15,
        },
        'trends': [
          {'date': '2026-03-01', 'score': 80.0, 'mention_count': 10},
        ],
        'platform_breakdown': [
          {'platform': 'reddit', 'mention_count': 15, 'average_sentiment': 0.7},
        ],
        'overall_score': 0.72,
        'total_reviews_analyzed': 120,
      };

      final analytics = SentimentAnalytics.fromJson(json);
      expect(analytics.overallScore, 0.72);
      expect(analytics.totalReviewsAnalyzed, 120);
      expect(analytics.distribution.positive, 65);
    });
  });
}
