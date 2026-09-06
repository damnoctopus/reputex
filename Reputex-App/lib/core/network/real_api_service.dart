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
import '../constants/api_constants.dart';
import 'api_client_interface.dart';
import 'dio_client.dart';

/// Real REST implementation of [IApiService] calling the FastAPI backend via [DioClient].
class RealApiService implements IApiService {
  RealApiService({required DioClient dioClient}) : _client = dioClient;

  final DioClient _client;

  // ── Authentication ──
  @override
  Future<AuthResponse> login({
    required String email,
    required String password,
  }) async {
    final response = await _client.post(
      ApiConstants.login,
      data: {'email': email, 'password': password},
    );
    return AuthResponse.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<AuthResponse> register({
    required String email,
    required String password,
    required String fullName,
    required String businessName,
    required String businessCategory,
  }) async {
    final response = await _client.post(
      ApiConstants.register,
      data: {
        'email': email,
        'password': password,
        'full_name': fullName,
        'business_name': businessName,
        'business_category': businessCategory,
      },
    );
    return AuthResponse.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<AuthTokens> refreshToken({required String refreshToken}) async {
    final response = await _client.post(
      ApiConstants.refreshToken,
      data: {'refresh_token': refreshToken},
    );
    return AuthTokens.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<void> logout() async {
    await _client.post(ApiConstants.logout);
  }

  @override
  Future<User> getCurrentUser() async {
    final response = await _client.get('/auth/me');
    return User.fromJson(response.data as Map<String, dynamic>);
  }

  // ── Business & Keywords ──
  @override
  Future<Business?> getBusiness() async {
    final response = await _client.get(ApiConstants.business);
    if (response.data == null) return null;
    return Business.fromJson(response.data as Map<String, dynamic>);
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
    final response = await _client.post(
      ApiConstants.business,
      data: {
        'name': name,
        'category': category,
        'website': website,
        'location': location,
        'phone': phone,
        'keywords': keywords,
        'platforms': platforms,
      },
    );
    return Business.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<List<BrandKeyword>> getKeywords() async {
    final response = await _client.get(ApiConstants.keywords);
    final list = response.data as List<dynamic>;
    return list
        .map((e) => BrandKeyword.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  @override
  Future<BrandKeyword> addKeyword({
    required String keyword,
    String category = 'brand',
  }) async {
    final response = await _client.post(
      ApiConstants.keywords,
      data: {'keyword': keyword, 'category': category},
    );
    return BrandKeyword.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<void> deleteKeyword(String id) async {
    await _client.delete('${ApiConstants.keywords}/$id');
  }

  // ── Dashboard & Analytics ──
  @override
  Future<DashboardSummary> getDashboardSummary() async {
    final response = await _client.get(ApiConstants.dashboard);
    return DashboardSummary.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<ReputationScore> getReputationScore() async {
    final response = await _client.get('${ApiConstants.dashboard}/score');
    return ReputationScore.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<SentimentDistribution> getSentimentDistribution() async {
    final response = await _client.get(ApiConstants.dashboardSentiment);
    return SentimentDistribution.fromJson(
      response.data as Map<String, dynamic>,
    );
  }

  @override
  Future<List<SentimentTrend>> getSentimentTrends({int days = 7}) async {
    final response = await _client.get(
      ApiConstants.dashboardTrends,
      queryParameters: {'days': days},
    );
    final list = response.data as List<dynamic>;
    return list
        .map((e) => SentimentTrend.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  @override
  Future<List<PlatformStatistics>> getPlatformStatistics() async {
    final response = await _client.get(ApiConstants.dashboardPlatforms);
    final list = response.data as List<dynamic>;
    return list
        .map((e) => PlatformStatistics.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  @override
  Future<SentimentAnalytics> getSentimentAnalytics() async {
    final response = await _client.get('/analytics/sentiment');
    return SentimentAnalytics.fromJson(response.data as Map<String, dynamic>);
  }

  // ── Mentions / Reviews ──
  @override
  Future<PaginatedMentions> getMentions({
    MentionsFilter filter = const MentionsFilter(),
  }) async {
    final query = <String, dynamic>{
      'page': filter.page,
      'limit': filter.limit,
      if (filter.platform != null && filter.platform != 'All')
        'platform': filter.platform,
      if (filter.sentiment != null && filter.sentiment != 'All')
        'sentiment': filter.sentiment,
      if (filter.isFake != null) 'is_fake': filter.isFake,
      if (filter.searchQuery != null && filter.searchQuery!.isNotEmpty)
        'q': filter.searchQuery,
      'sort_by': filter.sortBy,
    };

    final response = await _client.get(
      ApiConstants.mentions,
      queryParameters: query,
    );
    return PaginatedMentions.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<Mention> getMentionById(String id) async {
    final response = await _client.get('${ApiConstants.mentions}/$id');
    return Mention.fromJson(response.data as Map<String, dynamic>);
  }

  // ── Fraud Detection ──
  @override
  Future<List<FraudResult>> getFraudReviews() async {
    final response = await _client.get(ApiConstants.fraud);
    final list = response.data as List<dynamic>;
    return list
        .map((e) => FraudResult.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  @override
  Future<FraudResult> getFraudAnalysis(String mentionId) async {
    final response = await _client.get('${ApiConstants.fraud}/$mentionId');
    return FraudResult.fromJson(response.data as Map<String, dynamic>);
  }

  // ── Crisis Monitoring ──
  @override
  Future<List<CrisisEvent>> getCrisisEvents() async {
    final response = await _client.get(ApiConstants.crisis);
    final list = response.data as List<dynamic>;
    return list
        .map((e) => CrisisEvent.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  @override
  Future<CrisisEvent?> getActiveCrisis() async {
    final response = await _client.get(ApiConstants.crisisActive);
    if (response.data == null) return null;
    return CrisisEvent.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<CrisisEvent> getCrisisById(String id) async {
    final response = await _client.get('${ApiConstants.crisis}/$id');
    return CrisisEvent.fromJson(response.data as Map<String, dynamic>);
  }

  // ── Alerts ──
  @override
  Future<List<AlertItem>> getAlerts() async {
    final response = await _client.get(ApiConstants.alerts);
    final list = response.data as List<dynamic>;
    return list
        .map((e) => AlertItem.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  @override
  Future<void> markAlertAsRead(String id) async {
    await _client.put('${ApiConstants.alerts}/$id/read');
  }

  // ── AI Responses ──
  @override
  Future<ResponseDraft> generateResponse({
    required String mentionId,
    required String tone,
    String? customInstructions,
  }) async {
    final response = await _client.post(
      ApiConstants.responsesGenerate,
      data: {
        'mention_id': mentionId,
        'tone': tone,
        'custom_instructions': ?customInstructions,
      },
    );
    return ResponseDraft.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<List<ResponseDraft>> getResponses() async {
    final response = await _client.get(ApiConstants.responses);
    final list = response.data as List<dynamic>;
    return list
        .map((e) => ResponseDraft.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  @override
  Future<ResponseDraft> getResponseById(String id) async {
    final response = await _client.get('${ApiConstants.responses}/$id');
    return ResponseDraft.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<ResponseDraft> approveResponse({
    required String id,
    required String responseText,
  }) async {
    final response = await _client.post(
      '${ApiConstants.responses}/$id/approve',
      data: {'response_text': responseText},
    );
    return ResponseDraft.fromJson(response.data as Map<String, dynamic>);
  }

  @override
  Future<ResponseDraft> dispatchResponse(String id) async {
    final response = await _client.post(
      '${ApiConstants.responses}/$id/dispatch',
    );
    return ResponseDraft.fromJson(response.data as Map<String, dynamic>);
  }

  // ── Full Platform Scan ──
  @override
  Future<Map<String, dynamic>> triggerScan() async {
    final response = await _client.post('/business/scan');
    return response.data as Map<String, dynamic>;
  }

  @override
  Future<Map<String, dynamic>> getScanStatus() async {
    final response = await _client.get('/business/scan/status');
    return response.data as Map<String, dynamic>;
  }

  // ── Customer Issues & Complaints ──
  @override
  Future<List<CustomerIssue>> getIssues({
    String? category,
    String? severity,
    String? status,
  }) async {
    final queryParams = <String, dynamic>{};
    if (category != null) queryParams['category'] = category;
    if (severity != null) queryParams['severity'] = severity;
    if (status != null) queryParams['status'] = status;

    final response = await _client.get(
      '/issues',
      queryParameters: queryParams,
    );
    final data = response.data as Map<String, dynamic>;
    final items = data['items'] as List<dynamic>? ?? [];
    return items
        .map((e) => CustomerIssue.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  @override
  Future<CustomerIssue> getIssueById(String id) async {
    final response = await _client.get('/issues/$id');
    return CustomerIssue.fromJson(response.data as Map<String, dynamic>);
  }

  // ── Findings & Review Authenticity ──
  @override
  Future<List<FindingItem>> getFindings({
    String? type,
    String? severity,
  }) async {
    final queryParams = <String, dynamic>{};
    if (type != null) queryParams['finding_type'] = type;
    if (severity != null) queryParams['severity'] = severity;

    final response = await _client.get(
      '/findings',
      queryParameters: queryParams,
    );
    final data = response.data as Map<String, dynamic>;
    final items = data['items'] as List<dynamic>? ?? [];
    return items
        .map((e) => FindingItem.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  @override
  Future<List<FindingItem>> getSuspiciousReviews() async {
    final response = await _client.get('/suspicious-reviews');
    final data = response.data as Map<String, dynamic>;
    final items = data['items'] as List<dynamic>? ?? [];
    return items
        .map((e) => FindingItem.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  @override
  Future<List<FindingItem>> getManipulationClusters() async {
    final response = await _client.get('/manipulation-clusters');
    final data = response.data as Map<String, dynamic>;
    final items = data['items'] as List<dynamic>? ?? [];
    return items
        .map((e) => FindingItem.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}
