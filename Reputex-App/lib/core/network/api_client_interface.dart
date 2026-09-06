import '../../features/alerts/domain/models/alert_item.dart';
import '../../features/auth/domain/models/auth_response.dart';
import '../../features/auth/domain/models/auth_tokens.dart';
import '../../features/auth/domain/models/user.dart';
import '../../features/crisis/domain/models/crisis_event.dart';
import '../../features/dashboard/domain/models/dashboard_summary.dart';
import '../../features/dashboard/domain/models/platform_statistics.dart';
import '../../features/dashboard/domain/models/reputation_score.dart';
import '../../features/dashboard/domain/models/sentiment_distribution.dart';
import '../../features/dashboard/domain/models/sentiment_trend.dart';
import '../../features/findings/domain/models/finding_item.dart';
import '../../features/fraud/domain/models/fraud_result.dart';
import '../../features/issues/domain/models/customer_issue.dart';
import '../../features/mentions/domain/models/mention.dart';
import '../../features/mentions/domain/models/mentions_filter.dart';
import '../../features/mentions/domain/models/paginated_mentions.dart';
import '../../features/onboarding/domain/models/brand_keyword.dart';
import '../../features/onboarding/domain/models/business.dart';
import '../../features/responses/domain/models/response_draft.dart';
import '../../features/sentiment/domain/models/sentiment_analytics.dart';

/// Clean API service interface abstracting all REST communication.
///
/// Both [MockApiService] and [RealApiService] implement this contract.
abstract class IApiService {
  // ── Authentication ──
  Future<AuthResponse> login({required String email, required String password});

  Future<AuthResponse> register({
    required String email,
    required String password,
    required String fullName,
    required String businessName,
    required String businessCategory,
  });

  Future<AuthTokens> refreshToken({required String refreshToken});

  Future<void> logout();

  Future<User> getCurrentUser();

  // ── Business & Keywords ──
  Future<Business?> getBusiness();

  Future<Business> setupBusiness({
    required String name,
    required String category,
    String? website,
    String? location,
    String? phone,
    required List<String> keywords,
    required List<String> platforms,
  });

  Future<List<BrandKeyword>> getKeywords();

  Future<BrandKeyword> addKeyword({
    required String keyword,
    String category = 'brand',
  });

  Future<void> deleteKeyword(String id);

  // ── Dashboard & Analytics ──
  Future<DashboardSummary> getDashboardSummary();

  Future<ReputationScore> getReputationScore();

  Future<SentimentDistribution> getSentimentDistribution();

  Future<List<SentimentTrend>> getSentimentTrends({int days = 7});

  Future<List<PlatformStatistics>> getPlatformStatistics();

  Future<SentimentAnalytics> getSentimentAnalytics();

  // ── Mentions / Reviews ──
  Future<PaginatedMentions> getMentions({
    MentionsFilter filter = const MentionsFilter(),
  });

  Future<Mention> getMentionById(String id);

  // ── Fraud Detection ──
  Future<List<FraudResult>> getFraudReviews();

  Future<FraudResult> getFraudAnalysis(String mentionId);

  // ── Crisis Monitoring ──
  Future<List<CrisisEvent>> getCrisisEvents();

  Future<CrisisEvent?> getActiveCrisis();

  Future<CrisisEvent> getCrisisById(String id);

  // ── Alerts ──
  Future<List<AlertItem>> getAlerts();

  Future<void> markAlertAsRead(String id);

  // ── AI Responses ──
  Future<ResponseDraft> generateResponse({
    required String mentionId,
    required String tone,
    String? customInstructions,
  });

  Future<List<ResponseDraft>> getResponses();

  Future<ResponseDraft> getResponseById(String id);

  Future<ResponseDraft> approveResponse({
    required String id,
    required String responseText,
  });

  Future<ResponseDraft> dispatchResponse(String id);

  // ── Full Platform Scan ──
  Future<Map<String, dynamic>> triggerScan();

  Future<Map<String, dynamic>> getScanStatus();

  // ── Customer Issues & Complaints ──
  Future<List<CustomerIssue>> getIssues({
    String? category,
    String? severity,
    String? status,
  });

  Future<CustomerIssue> getIssueById(String id);

  // ── Findings & Review Authenticity ──
  Future<List<FindingItem>> getFindings({
    String? type,
    String? severity,
  });

  Future<List<FindingItem>> getSuspiciousReviews();

  Future<List<FindingItem>> getManipulationClusters();
}
