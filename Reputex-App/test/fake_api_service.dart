import 'package:reputex_mobile/core/network/api_client_interface.dart';
import 'package:reputex_mobile/features/alerts/domain/models/alert_item.dart';
import 'package:reputex_mobile/features/auth/domain/models/auth_response.dart';
import 'package:reputex_mobile/features/auth/domain/models/auth_tokens.dart';
import 'package:reputex_mobile/features/auth/domain/models/user.dart';
import 'package:reputex_mobile/features/crisis/domain/models/crisis_event.dart';
import 'package:reputex_mobile/features/dashboard/domain/models/dashboard_summary.dart';
import 'package:reputex_mobile/features/dashboard/domain/models/platform_statistics.dart';
import 'package:reputex_mobile/features/dashboard/domain/models/reputation_score.dart';
import 'package:reputex_mobile/features/dashboard/domain/models/sentiment_distribution.dart';
import 'package:reputex_mobile/features/dashboard/domain/models/sentiment_trend.dart';
import 'package:reputex_mobile/features/findings/domain/models/finding_item.dart';
import 'package:reputex_mobile/features/fraud/domain/models/fraud_result.dart';
import 'package:reputex_mobile/features/issues/domain/models/customer_issue.dart';
import 'package:reputex_mobile/features/mentions/domain/models/mention.dart';
import 'package:reputex_mobile/features/mentions/domain/models/mentions_filter.dart';
import 'package:reputex_mobile/features/mentions/domain/models/paginated_mentions.dart';
import 'package:reputex_mobile/features/onboarding/domain/models/brand_keyword.dart';
import 'package:reputex_mobile/features/onboarding/domain/models/business.dart';
import 'package:reputex_mobile/features/responses/domain/models/response_draft.dart';
import 'package:reputex_mobile/features/sentiment/domain/models/sentiment_analytics.dart';

/// Test-only fake implementation of [IApiService] for unit testing providers.
class FakeApiService implements IApiService {
  List<AlertItem> _alerts = [
    AlertItem(
      id: 'alert_1',
      type: 'spike',
      title: 'Sudden spike in negative mentions',
      message: 'Detected 5 negative mentions in the last 2 hours',
      severity: 'high',
      timestamp: DateTime.now(),
      isRead: false,
    ),
  ];

  @override
  Future<AuthResponse> login({required String email, required String password}) async {
    final user = User(
      id: 'u_test',
      email: email,
      fullName: 'Test User',
      businessId: 'biz_1',
      role: 'owner',
      createdAt: DateTime.now(),
    );
    const tokens = AuthTokens(accessToken: 'token_123', refreshToken: 'refresh_123');
    return AuthResponse(user: user, tokens: tokens);
  }

  @override
  Future<AuthResponse> register({
    required String email,
    required String password,
    required String fullName,
    required String businessName,
    required String businessCategory,
  }) async {
    final user = User(
      id: 'u_test_reg',
      email: email,
      fullName: fullName,
      businessId: 'biz_1',
      role: 'owner',
      createdAt: DateTime.now(),
    );
    const tokens = AuthTokens(accessToken: 'token_123', refreshToken: 'refresh_123');
    return AuthResponse(user: user, tokens: tokens);
  }

  @override
  Future<AuthTokens> refreshToken({required String refreshToken}) async {
    return const AuthTokens(accessToken: 'refreshed_token', refreshToken: 'refreshed_refresh');
  }

  @override
  Future<void> logout() async {}

  @override
  Future<User> getCurrentUser() async {
    return User(
      id: 'u_test',
      email: 'adira@spicesymphony.com',
      fullName: 'Test User',
      businessId: 'biz_1',
      role: 'owner',
      createdAt: DateTime.now(),
    );
  }

  @override
  Future<Business?> getBusiness() async {
    return Business(
      id: 'biz_1',
      name: 'Test Business',
      category: 'Restaurant',
      createdAt: DateTime.now(),
    );
  }

  @override
  Future<Business> setupBusiness({
    required String name,
    required String category,
    String? website,
    String? location,
    String? phone,
    required List<String> keywords,
    required List<String> platforms,
  }) async {
    return Business(
      id: 'biz_1',
      name: name,
      category: category,
      location: location,
      createdAt: DateTime.now(),
    );
  }

  @override
  Future<List<BrandKeyword>> getKeywords() async => [];

  @override
  Future<BrandKeyword> addKeyword({required String keyword, String category = 'brand'}) async {
    return BrandKeyword(id: 'k1', keyword: keyword, category: category);
  }

  @override
  Future<void> deleteKeyword(String id) async {}

  @override
  Future<DashboardSummary> getDashboardSummary() async {
    return const DashboardSummary(
      reputationScore: ReputationScore(currentScore: 82.5, change: 3.0),
      sentimentDistribution: SentimentDistribution(
        positivePercentage: 72.0,
        negativePercentage: 16.0,
        neutralPercentage: 12.0,
      ),
      totalMentions: 25,
      recentMentions: [],
    );
  }

  @override
  Future<ReputationScore> getReputationScore() async {
    return const ReputationScore(currentScore: 82.5, change: 3.0);
  }

  @override
  Future<SentimentDistribution> getSentimentDistribution() async {
    return const SentimentDistribution(
      positivePercentage: 72.0,
      negativePercentage: 16.0,
      neutralPercentage: 12.0,
    );
  }

  @override
  Future<List<SentimentTrend>> getSentimentTrends({int days = 7}) async => [];

  @override
  Future<List<PlatformStatistics>> getPlatformStatistics() async => [];

  @override
  Future<SentimentAnalytics> getSentimentAnalytics() async {
    return const SentimentAnalytics(
      distribution: SentimentDistribution(
        positivePercentage: 72.0,
        negativePercentage: 16.0,
        neutralPercentage: 12.0,
      ),
      overallScore: 82.0,
      totalReviewsAnalyzed: 25,
    );
  }

  @override
  Future<PaginatedMentions> getMentions({MentionsFilter filter = const MentionsFilter()}) async {
    final items = [
      Mention(
        id: 'm1',
        platform: 'google',
        author: 'Reviewer',
        content: 'Authentic food!',
        sentiment: 'positive',
        sentimentScore: 0.9,
        timestamp: DateTime.now(),
      ),
    ];
    return PaginatedMentions(
      items: items,
      totalCount: 1,
      page: 1,
      totalPages: 1,
      hasMore: false,
    );
  }

  @override
  Future<Mention> getMentionById(String id) async {
    return Mention(
      id: id,
      platform: 'google',
      author: 'Reviewer',
      content: 'Authentic food!',
      sentiment: 'positive',
      sentimentScore: 0.9,
      timestamp: DateTime.now(),
    );
  }

  @override
  Future<List<FraudResult>> getFraudReviews() async => [];

  @override
  Future<FraudResult> getFraudAnalysis(String mentionId) async {
    return FraudResult(
      mentionId: mentionId,
      isFraudulent: false,
      riskLevel: 'low',
      confidence: 0.1,
      reasons: const [],
    );
  }

  @override
  Future<List<CrisisEvent>> getCrisisEvents() async => [];

  @override
  Future<CrisisEvent?> getActiveCrisis() async => null;

  @override
  Future<CrisisEvent> getCrisisById(String id) async {
    return CrisisEvent(
      id: id,
      title: 'Potential Surge',
      severity: 'medium',
      triggerReason: 'Negative velocity spike',
      startedAt: DateTime.now(),
    );
  }

  @override
  Future<List<AlertItem>> getAlerts() async => _alerts;

  @override
  Future<void> markAlertAsRead(String id) async {
    _alerts = _alerts.map((a) => a.id == id ? a.copyWith(isRead: true) : a).toList();
  }

  @override
  Future<ResponseDraft> generateResponse({
    required String mentionId,
    required String tone,
    String? customInstructions,
  }) async {
    return ResponseDraft(
      id: 'resp_1',
      mentionId: mentionId,
      originalReview: 'Food was great!',
      generatedResponse: 'Thank you for your review!',
      tone: tone,
      status: 'drafted',
      createdAt: DateTime.now(),
    );
  }

  @override
  Future<List<ResponseDraft>> getResponses() async => [];

  @override
  Future<ResponseDraft> getResponseById(String id) async {
    return ResponseDraft(
      id: id,
      mentionId: 'm1',
      originalReview: 'Food was great!',
      generatedResponse: 'Thank you for your review!',
      tone: 'professional',
      status: 'drafted',
      createdAt: DateTime.now(),
    );
  }

  @override
  Future<ResponseDraft> approveResponse({
    required String id,
    required String responseText,
  }) async {
    return ResponseDraft(
      id: id,
      mentionId: 'm1',
      originalReview: 'Food was great!',
      generatedResponse: responseText,
      tone: 'professional',
      status: 'approved',
      createdAt: DateTime.now(),
      approvedAt: DateTime.now(),
    );
  }

  @override
  Future<ResponseDraft> dispatchResponse(String id) async {
    return ResponseDraft(
      id: id,
      mentionId: 'm1',
      originalReview: 'Food was great!',
      generatedResponse: 'Thank you!',
      tone: 'professional',
      status: 'dispatched',
      createdAt: DateTime.now(),
      dispatchedAt: DateTime.now(),
    );
  }

  @override
  Future<Map<String, dynamic>> triggerScan() async => {'status': 'triggered'};

  @override
  Future<Map<String, dynamic>> getScanStatus() async {
    return {
      'status': 'completed',
      'active_platforms': ['google', 'reddit', 'twitter'],
      'jobs': [],
    };
  }

  @override
  Future<List<CustomerIssue>> getIssues({String? category, String? severity, String? status}) async => [];

  @override
  Future<CustomerIssue> getIssueById(String id) async {
    return CustomerIssue(
      id: id,
      businessId: 'biz_1',
      category: 'Service',
      subtopic: 'Wait time',
      severity: 'low',
      status: 'open',
      mentionCount: 1,
      firstSeenAt: DateTime.now(),
      lastSeenAt: DateTime.now(),
    );
  }

  @override
  Future<List<FindingItem>> getFindings({String? type, String? severity}) async => [];

  @override
  Future<List<FindingItem>> getSuspiciousReviews() async => [];

  @override
  Future<List<FindingItem>> getManipulationClusters() async => [];
}
