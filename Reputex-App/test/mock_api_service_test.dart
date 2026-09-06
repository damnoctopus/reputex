import 'package:flutter_test/flutter_test.dart';
import 'package:reputex_mobile/core/network/mock_api_service.dart';
import 'package:reputex_mobile/features/mentions/domain/models/mentions_filter.dart';

void main() {
  late MockApiService api;

  setUp(() {
    api = MockApiService();
  });

  group('MockApiService Tests', () {
    test('login returns valid auth response', () async {
      final auth = await api.login(
        email: 'adira@spicesymphony.com',
        password: 'password123',
      );

      expect(auth.user.email, 'adira@spicesymphony.com');
      expect(auth.tokens.accessToken, isNotEmpty);
      expect(auth.tokens.refreshToken, isNotEmpty);
    });

    test('register creates new user and business', () async {
      final auth = await api.register(
        email: 'newuser@test.com',
        password: 'password123',
        fullName: 'New Owner',
        businessName: 'My Cafe',
        businessCategory: 'Cafe',
      );

      expect(auth.user.email, 'newuser@test.com');
      expect(auth.user.fullName, 'New Owner');
    });

    test('getDashboardSummary returns valid dashboard data', () async {
      final summary = await api.getDashboardSummary();

      expect(summary.reputationScore.currentScore, greaterThan(0));
      expect(summary.totalMentions, greaterThan(0));
      expect(summary.sentimentDistribution.positivePercentage, greaterThan(0));
    });

    test('getMentions supports pagination and filtering', () async {
      // First page
      final page1 = await api.getMentions(
        filter: const MentionsFilter(page: 1, limit: 2),
      );
      expect(page1.items.length, 2);
      expect(page1.hasMore, true);
      expect(page1.page, 1);

      // Filter by positive sentiment
      final positiveOnly = await api.getMentions(
        filter: const MentionsFilter(sentiment: 'positive'),
      );
      expect(
        positiveOnly.items.every((m) => m.sentiment == 'positive'),
        true,
      );
    });

    test('fraud analysis returns report for valid mention', () async {
      final fraud = await api.getFraudAnalysis('men_fraud_1');

      expect(fraud.mentionId, 'men_fraud_1');
      expect(fraud.isFraudulent, true);
      expect(fraud.confidence, greaterThan(0.5));
    });

    test('crisis management can fetch active crisis and crisis details', () async {
      final crises = await api.getCrisisEvents();
      expect(crises, isNotEmpty);

      final activeCrisis = await api.getActiveCrisis();
      expect(activeCrisis, isNotNull);
      expect(activeCrisis!.status, 'active');

      final target = await api.getCrisisById(activeCrisis.id);
      expect(target.id, activeCrisis.id);
    });

    test('alerts can be marked as read', () async {
      final alerts = await api.getAlerts();
      final unread = alerts.firstWhere((a) => !a.isRead);

      await api.markAlertAsRead(unread.id);

      final updated = await api.getAlerts();
      final target = updated.firstWhere((a) => a.id == unread.id);
      expect(target.isRead, true);
    });

    test('AI response flow: generate, approve, dispatch', () async {
      final draft = await api.generateResponse(
        mentionId: 'm1',
        tone: 'professional',
        customInstructions: 'Be warm and inviting',
      );

      expect(draft.mentionId, 'm1');
      expect(draft.tone, 'professional');

      final approved = await api.approveResponse(
        id: draft.id,
        responseText: 'Customized response text',
      );

      expect(approved.status, 'approved');
      expect(approved.generatedResponse, 'Customized response text');

      final dispatched = await api.dispatchResponse(draft.id);
      expect(dispatched.status, 'dispatched');
    });

    test('scan workflow can trigger scan and fetch status', () async {
      final scanResult = await api.triggerScan();
      expect(scanResult['status'], 'completed');

      final status = await api.getScanStatus();
      expect(status['status'], 'completed');
      expect(status['active_platforms'], contains('Google'));
    });

    test('customer issues can be fetched and retrieved by ID', () async {
      final issues = await api.getIssues();
      expect(issues, isNotEmpty);
      expect(issues.first.category, isNotEmpty);
      expect(issues.first.mentionCount, greaterThan(0));

      final issue = await api.getIssueById(issues.first.id);
      expect(issue.id, issues.first.id);
      expect(issue.subtopic, issues.first.subtopic);
      expect(issue.platformsBreakdown, isNotEmpty);
    });

    test('findings, suspicious reviews and clusters can be retrieved', () async {
      final findings = await api.getFindings();
      expect(findings, isNotEmpty);

      final suspicious = await api.getSuspiciousReviews();
      expect(suspicious, isNotEmpty);
      expect(suspicious.first.findingType, 'review_authenticity');
      expect(suspicious.first.metadataJson['signals'], isNotNull);

      final clusters = await api.getManipulationClusters();
      expect(clusters, isNotEmpty);
      expect(clusters.first.findingType, 'manipulation_cluster');
    });

    test('dashboard summary includes customer issues and manipulation count', () async {
      final summary = await api.getDashboardSummary();
      expect(summary.topIssues, isNotEmpty);
      expect(summary.suspiciousReviewsCount, greaterThan(0));
      expect(summary.activeClustersCount, greaterThan(0));
      expect(summary.crisisRiskLevel, 'High Risk');
    });
  });
}
