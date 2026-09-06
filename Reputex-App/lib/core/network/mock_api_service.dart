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
import '../../features/fraud/domain/models/fraud_result.dart';
import '../../features/mentions/domain/models/mention.dart';
import '../../features/mentions/domain/models/mention_engagement.dart';
import '../../features/mentions/domain/models/mentions_filter.dart';
import '../../features/mentions/domain/models/paginated_mentions.dart';
import '../../features/onboarding/domain/models/brand_keyword.dart';
import '../../features/onboarding/domain/models/business.dart';
import '../../features/responses/domain/models/response_draft.dart';
import '../../features/sentiment/domain/models/sentiment_analytics.dart';
import 'api_client_interface.dart';

/// In-memory mock implementation of [IApiService] providing realistic
/// simulated backend responses, artificial network latency, filtering, and pagination.
class MockApiService implements IApiService {
  MockApiService({this.simulatedDelay = const Duration(milliseconds: 600)});

  final Duration simulatedDelay;

  Future<void> _delay() async {
    if (simulatedDelay > Duration.zero) {
      await Future<void>.delayed(simulatedDelay);
    }
  }

  // ── In-Memory State ──
  User _currentUser = User(
    id: 'usr_001',
    email: 'adithya@spicesymphony.com',
    fullName: 'Adithya',
    role: 'owner',
    businessId: 'biz_001',
    isActive: true,
    createdAt: DateTime.now().subtract(const Duration(days: 30)),
  );

  Business _currentBusiness = Business(
    id: 'biz_001',
    name: 'Spice Symphony',
    category: 'Restaurant & Hospitality',
    website: 'https://spicesymphony.in',
    location: 'Indiranagar, Bengaluru',
    phone: '+91 98765 43210',
    monitoredPlatforms: const [
      'Google',
      'JustDial',
      'Reddit',
      'X',
      'Sulekha',
      'IndiaMART',
    ],
    keywords: [
      const BrandKeyword(id: 'kw_1', keyword: 'Spice Symphony'),
      const BrandKeyword(id: 'kw_2', keyword: 'Spice Symphony Indiranagar'),
      const BrandKeyword(id: 'kw_3', keyword: 'best biryani Indiranagar'),
    ],
    ownerId: 'usr_001',
    createdAt: DateTime.now().subtract(const Duration(days: 30)),
  );

  final List<AlertItem> _alerts = [
    AlertItem(
      id: 'alt_1',
      type: 'crisis',
      title: 'Active Reputation Crisis Detected',
      message: 'Negative mention velocity surged on Reddit (+14.5 mentions/hr) regarding food quality.',
      severity: 'high',
      timestamp: DateTime.now().subtract(const Duration(minutes: 25)),
      isRead: false,
      referenceId: 'crs_1',
      referenceType: 'crisis',
    ),
    AlertItem(
      id: 'alt_2',
      type: 'fraud',
      title: 'Suspicious Review Wave Flagged',
      message: '4 reviews posted within 8 minutes from fresh accounts on JustDial show coordinated behavior.',
      severity: 'critical',
      timestamp: DateTime.now().subtract(const Duration(hours: 2)),
      isRead: false,
      referenceId: 'men_fraud_1',
      referenceType: 'mention',
    ),
    AlertItem(
      id: 'alt_3',
      type: 'negative_spike',
      title: 'Negative Sentiment Alert',
      message: 'Sudden dip in daily sentiment score from 82 to 74 on Google.',
      severity: 'medium',
      timestamp: DateTime.now().subtract(const Duration(hours: 5)),
      isRead: true,
    ),
    AlertItem(
      id: 'alt_4',
      type: 'mention',
      title: 'High-Reach Mention',
      message: 'Influencer @foodie_bangalore praised your signature dish on X.',
      severity: 'low',
      timestamp: DateTime.now().subtract(const Duration(hours: 18)),
      isRead: true,
      referenceId: 'men_2',
      referenceType: 'mention',
    ),
  ];

  late final List<Mention> _mentions = [
    Mention(
      id: 'men_1',
      platform: 'Reddit',
      author: 'u/bangalore_foodie',
      content: 'Had dinner at Spice Symphony yesterday. The mutton biryani was cold and smelled off. When we informed staff, they were dismissive. Never going back! Beware guys.',
      sentiment: 'negative',
      sentimentScore: -0.84,
      isFake: false,
      fraudConfidence: 0.12,
      url: 'https://reddit.com/r/bangalore/comments/example1',
      timestamp: DateTime.now().subtract(const Duration(hours: 2)),
      engagement: const MentionEngagement(likes: 47, shares: 12, comments: 23),
      rating: 1.0,
      responseStatus: 'drafted',
      responseText: 'Dear guest, we sincerely apologize for the unacceptable experience with the mutton biryani. Quality and food safety are our highest priorities. Please call our manager directly at +91 98765 43210 so we can make this right.',
    ),
    Mention(
      id: 'men_2',
      platform: 'X',
      author: '@foodie_bangalore',
      content: 'Spice Symphony in Indiranagar has the crispiest butter garlic naan in the city! Service was top notch too. Highly recommended for family dinners. ⭐⭐⭐⭐⭐',
      sentiment: 'positive',
      sentimentScore: 0.92,
      isFake: false,
      fraudConfidence: 0.05,
      url: 'https://x.com/foodie_bangalore/status/123456',
      timestamp: DateTime.now().subtract(const Duration(hours: 5)),
      engagement: const MentionEngagement(likes: 128, shares: 34, comments: 15),
      rating: 5.0,
      responseStatus: 'none',
    ),
    Mention(
      id: 'men_fraud_1',
      platform: 'JustDial',
      author: 'Ramesh K.',
      content: 'Worst hotel ever scam business fraud owners food poisoning don’t visit go to Royal Treat opposite instead!',
      sentiment: 'negative',
      sentimentScore: -0.95,
      isFake: true,
      fraudConfidence: 0.94,
      url: 'https://justdial.com/reviews/123',
      timestamp: DateTime.now().subtract(const Duration(hours: 8)),
      engagement: const MentionEngagement(likes: 2, shares: 0, comments: 1),
      rating: 1.0,
      responseStatus: 'none',
    ),
    Mention(
      id: 'men_3',
      platform: 'Google',
      author: 'Priya Sharma',
      content: 'Pleasant ambiance and courteous staff. Paneer tikka was delightful, but the wait time on Friday evening was almost 45 minutes even with a reservation.',
      sentiment: 'neutral',
      sentimentScore: 0.15,
      isFake: false,
      fraudConfidence: 0.08,
      timestamp: DateTime.now().subtract(const Duration(hours: 12)),
      engagement: const MentionEngagement(likes: 8, shares: 1, comments: 2),
      rating: 3.0,
      responseStatus: 'approved',
      responseText: 'Thank you Priya for dining with us! We are thrilled you enjoyed the paneer tikka. We apologize for the extended wait on Friday — we are streamlining weekend table turnaround to ensure seamless reservations.',
    ),
    Mention(
      id: 'men_4',
      platform: 'Sulekha',
      author: 'Deepak Verma',
      content: 'Catered a corporate lunch for 40 people through Spice Symphony. Flawless execution, authentic flavors, everyone in our office loved the food!',
      sentiment: 'positive',
      sentimentScore: 0.88,
      isFake: false,
      fraudConfidence: 0.04,
      timestamp: DateTime.now().subtract(const Duration(days: 1)),
      engagement: const MentionEngagement(likes: 19, shares: 5, comments: 4),
      rating: 5.0,
      responseStatus: 'none',
    ),
    Mention(
      id: 'men_5',
      platform: 'IndiaMART',
      author: 'Vendor Inquiry',
      content: 'Looking for wholesale spice supply partnership with Spice Symphony Bengaluru branch. Kindly connect on listed business email.',
      sentiment: 'neutral',
      sentimentScore: 0.05,
      isFake: false,
      fraudConfidence: 0.02,
      timestamp: DateTime.now().subtract(const Duration(days: 2)),
      engagement: const MentionEngagement(likes: 1, shares: 0, comments: 0),
      responseStatus: 'none',
    ),
    Mention(
      id: 'men_6',
      platform: 'Google',
      author: 'Ananya Rao',
      content: 'The gulab jamun with rabri was heavenly! One of the few authentic North Indian spots that gets spices balanced just right.',
      sentiment: 'positive',
      sentimentScore: 0.89,
      isFake: false,
      fraudConfidence: 0.03,
      timestamp: DateTime.now().subtract(const Duration(days: 3)),
      engagement: const MentionEngagement(likes: 14, shares: 2, comments: 3),
      rating: 5.0,
      responseStatus: 'none',
    ),
  ];

  final List<FraudResult> _fraudResults = [
    FraudResult(
      mentionId: 'men_fraud_1',
      isFraudulent: true,
      confidence: 0.94,
      riskLevel: 'critical',
      author: 'Ramesh K.',
      platform: 'JustDial',
      timestamp: DateTime.now().subtract(const Duration(hours: 8)),
      reviewContent: 'Worst hotel ever scam business fraud owners food poisoning don’t visit go to Royal Treat opposite instead!',
      reasons: const [
        'Account created < 2 hours before posting',
        'Direct competitor plug ("Royal Treat") detected',
        'Extreme negative sentiment with no specific transaction details',
        'Coordinated burst: 3 other similar 1-star reviews in 15 minutes',
      ],
      patterns: const [
        SuspiciousPattern(
          patternName: 'Competitor Mention',
          description: 'Reviewer urges patrons to visit direct competitor.',
          severity: 'high',
        ),
        SuspiciousPattern(
          patternName: 'Review Burst Anomaly',
          description: 'Multiple 1-star reviews from identical IP subnet.',
          severity: 'critical',
        ),
      ],
    ),
  ];

  final List<CrisisEvent> _crisisEvents = [
    CrisisEvent(
      id: 'crs_1',
      title: 'Food Quality Allegation on r/bangalore',
      severity: 'high',
      status: 'active',
      triggerReason: 'Viral Reddit post alleging food spoilage reached 47 upvotes in 2 hours with 23 comments.',
      velocity: 14.5,
      negativeMentionsCount: 24,
      affectedPlatforms: const ['Reddit', 'X'],
      startedAt: DateTime.now().subtract(const Duration(hours: 3)),
      estimatedReach: 8500,
      peakVolumePerHour: 18,
      suggestedActions: const [
        'Post empathetic public response offering immediate inspection findings',
        'Provide kitchen hygiene certification audit in thread',
        'Contact original poster privately with food safety manager contact',
      ],
    ),
    CrisisEvent(
      id: 'crs_2',
      title: 'False Billing Rumor Spread on WhatsApp/JustDial',
      severity: 'medium',
      status: 'resolved',
      triggerReason: 'Rumors of overcharging during New Year Eve event resolved via invoice verification post.',
      velocity: 2.1,
      negativeMentionsCount: 12,
      affectedPlatforms: const ['JustDial'],
      startedAt: DateTime.now().subtract(const Duration(days: 14)),
      resolvedAt: DateTime.now().subtract(const Duration(days: 13)),
      estimatedReach: 2400,
      peakVolumePerHour: 6,
      suggestedActions: const [
        'Published itemized billing policy clarification',
        'Resolved with affected patrons',
      ],
    ),
  ];

  final Map<String, ResponseDraft> _responses = {};

  // ── Authentication Implementations ──
  @override
  Future<AuthResponse> login({
    required String email,
    required String password,
  }) async {
    await _delay();
    if (email.isEmpty || password.isEmpty) {
      throw Exception('Email and password cannot be empty');
    }
    _currentUser = _currentUser.copyWith(email: email);
    return AuthResponse(
      user: _currentUser,
      tokens: const AuthTokens(
        accessToken: 'mock_jwt_access_token_spice_symphony',
        refreshToken: 'mock_jwt_refresh_token_spice_symphony',
        tokenType: 'bearer',
        expiresIn: 3600,
      ),
    );
  }

  @override
  Future<AuthResponse> register({
    required String email,
    required String password,
    required String fullName,
    required String businessName,
    required String businessCategory,
  }) async {
    await _delay();
    _currentUser = User(
      id: 'usr_new_001',
      email: email,
      fullName: fullName,
      role: 'owner',
      isActive: true,
      createdAt: DateTime.now(),
    );
    _currentBusiness = Business(
      id: 'biz_new_001',
      name: businessName,
      category: businessCategory,
      monitoredPlatforms: const ['Google', 'JustDial', 'Reddit'],
      keywords: [BrandKeyword(id: 'kw_1', keyword: businessName)],
      ownerId: _currentUser.id,
      createdAt: DateTime.now(),
    );
    return AuthResponse(
      user: _currentUser,
      tokens: const AuthTokens(
        accessToken: 'mock_jwt_access_token_registered',
        refreshToken: 'mock_jwt_refresh_token_registered',
        tokenType: 'bearer',
        expiresIn: 3600,
      ),
    );
  }

  @override
  Future<AuthTokens> refreshToken({required String refreshToken}) async {
    await _delay();
    return const AuthTokens(
      accessToken: 'mock_jwt_access_token_refreshed',
      refreshToken: 'mock_jwt_refresh_token_refreshed',
      tokenType: 'bearer',
      expiresIn: 3600,
    );
  }

  @override
  Future<void> logout() async {
    await _delay();
  }

  @override
  Future<User> getCurrentUser() async {
    await _delay();
    return _currentUser;
  }

  // ── Business Implementations ──
  @override
  Future<Business?> getBusiness() async {
    await _delay();
    return _currentBusiness;
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
    await _delay();
    _currentBusiness = Business(
      id: 'biz_${DateTime.now().millisecondsSinceEpoch}',
      name: name,
      category: category,
      website: website,
      location: location,
      phone: phone,
      monitoredPlatforms: platforms,
      keywords: keywords
          .map((kw) => BrandKeyword(id: 'kw_${kw.hashCode}', keyword: kw))
          .toList(),
      ownerId: _currentUser.id,
      createdAt: DateTime.now(),
    );
    return _currentBusiness;
  }

  @override
  Future<List<BrandKeyword>> getKeywords() async {
    await _delay();
    return _currentBusiness.keywords;
  }

  @override
  Future<BrandKeyword> addKeyword({
    required String keyword,
    String category = 'brand',
  }) async {
    await _delay();
    final newKw = BrandKeyword(
      id: 'kw_${DateTime.now().millisecondsSinceEpoch}',
      keyword: keyword,
      category: category,
    );
    _currentBusiness = _currentBusiness.copyWith(
      keywords: [..._currentBusiness.keywords, newKw],
    );
    return newKw;
  }

  @override
  Future<void> deleteKeyword(String id) async {
    await _delay();
    _currentBusiness = _currentBusiness.copyWith(
      keywords: _currentBusiness.keywords.where((kw) => kw.id != id).toList(),
    );
  }

  // ── Dashboard & Analytics Implementations ──
  @override
  Future<DashboardSummary> getDashboardSummary() async {
    await _delay();
    final score = await getReputationScore();
    final sentiment = await getSentimentDistribution();
    final activeCrisis = await getActiveCrisis();

    return DashboardSummary(
      reputationScore: score,
      sentimentDistribution: sentiment,
      totalMentions: 230,
      crisisActive: activeCrisis != null,
      crisisCount: activeCrisis != null ? 1 : 0,
      pendingResponsesCount: 3,
      fraudAlertsCount: 1,
      recentMentions: _mentions.take(4).toList(),
    );
  }

  @override
  Future<ReputationScore> getReputationScore() async {
    await _delay();
    return ReputationScore(
      currentScore: 78.4,
      previousScore: 74.2,
      change: 4.2,
      trend: 'up',
      calculatedAt: DateTime.now(),
    );
  }

  @override
  Future<SentimentDistribution> getSentimentDistribution() async {
    await _delay();
    return const SentimentDistribution(
      positive: 142,
      neutral: 58,
      negative: 30,
      total: 230,
      positivePercentage: 61.7,
      neutralPercentage: 25.2,
      negativePercentage: 13.1,
    );
  }

  @override
  Future<List<SentimentTrend>> getSentimentTrends({int days = 7}) async {
    await _delay();
    return [
      const SentimentTrend(
        date: 'Mon',
        positive: 18,
        neutral: 6,
        negative: 3,
        score: 75.0,
      ),
      const SentimentTrend(
        date: 'Tue',
        positive: 22,
        neutral: 8,
        negative: 2,
        score: 79.0,
      ),
      const SentimentTrend(
        date: 'Wed',
        positive: 19,
        neutral: 7,
        negative: 4,
        score: 76.5,
      ),
      const SentimentTrend(
        date: 'Thu',
        positive: 25,
        neutral: 9,
        negative: 1,
        score: 83.0,
      ),
      const SentimentTrend(
        date: 'Fri',
        positive: 30,
        neutral: 12,
        negative: 8,
        score: 74.0,
      ),
      const SentimentTrend(
        date: 'Sat',
        positive: 32,
        neutral: 10,
        negative: 5,
        score: 77.5,
      ),
      const SentimentTrend(
        date: 'Sun',
        positive: 28,
        neutral: 8,
        negative: 3,
        score: 81.0,
      ),
    ];
  }

  @override
  Future<List<PlatformStatistics>> getPlatformStatistics() async {
    await _delay();
    return const [
      PlatformStatistics(
        platform: 'Google',
        count: 110,
        positivePercentage: 68.0,
        negativePercentage: 12.0,
        neutralPercentage: 20.0,
        averageRating: 4.2,
      ),
      PlatformStatistics(
        platform: 'JustDial',
        count: 45,
        positivePercentage: 55.0,
        negativePercentage: 22.0,
        neutralPercentage: 23.0,
        averageRating: 3.8,
      ),
      PlatformStatistics(
        platform: 'Sulekha',
        count: 35,
        positivePercentage: 65.0,
        negativePercentage: 10.0,
        neutralPercentage: 25.0,
        averageRating: 4.1,
      ),
      PlatformStatistics(
        platform: 'Reddit',
        count: 25,
        positivePercentage: 40.0,
        negativePercentage: 36.0,
        neutralPercentage: 24.0,
        averageRating: 3.1,
      ),
      PlatformStatistics(
        platform: 'X',
        count: 15,
        positivePercentage: 73.0,
        negativePercentage: 14.0,
        neutralPercentage: 13.0,
        averageRating: 4.4,
      ),
    ];
  }

  @override
  Future<SentimentAnalytics> getSentimentAnalytics() async {
    await _delay();
    final dist = await getSentimentDistribution();
    final trends = await getSentimentTrends();
    final platforms = await getPlatformStatistics();

    return SentimentAnalytics(
      distribution: dist,
      trends: trends,
      platformBreakdown: platforms,
      overallScore: 78.4,
      totalReviewsAnalyzed: 230,
    );
  }

  // ── Mentions Implementations ──
  @override
  Future<PaginatedMentions> getMentions({
    MentionsFilter filter = const MentionsFilter(),
  }) async {
    await _delay();

    var filtered = List<Mention>.from(_mentions);

    if (filter.platform != null &&
        filter.platform!.isNotEmpty &&
        filter.platform != 'All') {
      filtered = filtered
          .where(
            (m) => m.platform.toLowerCase() == filter.platform!.toLowerCase(),
          )
          .toList();
    }

    if (filter.sentiment != null &&
        filter.sentiment!.isNotEmpty &&
        filter.sentiment != 'All') {
      filtered = filtered
          .where(
            (m) => m.sentiment.toLowerCase() == filter.sentiment!.toLowerCase(),
          )
          .toList();
    }

    if (filter.isFake != null) {
      filtered = filtered.where((m) => m.isFake == filter.isFake).toList();
    }

    if (filter.searchQuery != null && filter.searchQuery!.isNotEmpty) {
      final q = filter.searchQuery!.toLowerCase();
      filtered = filtered
          .where(
            (m) =>
                m.content.toLowerCase().contains(q) ||
                m.author.toLowerCase().contains(q),
          )
          .toList();
    }

    final totalCount = filtered.length;
    final startIndex = (filter.page - 1) * filter.limit;
    final endIndex = (startIndex + filter.limit).clamp(0, totalCount);

    final pagedItems = startIndex < totalCount
        ? filtered.sublist(startIndex, endIndex)
        : <Mention>[];

    final totalPages = (totalCount / filter.limit).ceil();
    final hasMore = filter.page < totalPages;

    return PaginatedMentions(
      items: pagedItems,
      totalCount: totalCount,
      page: filter.page,
      totalPages: totalPages > 0 ? totalPages : 1,
      hasMore: hasMore,
    );
  }

  @override
  Future<Mention> getMentionById(String id) async {
    await _delay();
    return _mentions.firstWhere(
      (m) => m.id == id,
      orElse: () => _mentions.first,
    );
  }

  // ── Fraud Detection Implementations ──
  @override
  Future<List<FraudResult>> getFraudReviews() async {
    await _delay();
    return _fraudResults;
  }

  @override
  Future<FraudResult> getFraudAnalysis(String mentionId) async {
    await _delay();
    return _fraudResults.firstWhere(
      (f) => f.mentionId == mentionId,
      orElse: () => FraudResult(
        mentionId: mentionId,
        isFraudulent: false,
        confidence: 0.05,
        riskLevel: 'low',
        reasons: const ['No suspicious indicators detected'],
      ),
    );
  }

  // ── Crisis Monitoring Implementations ──
  @override
  Future<List<CrisisEvent>> getCrisisEvents() async {
    await _delay();
    return _crisisEvents;
  }

  @override
  Future<CrisisEvent?> getActiveCrisis() async {
    await _delay();
    try {
      return _crisisEvents.firstWhere((c) => c.status == 'active');
    } catch (_) {
      return null;
    }
  }

  @override
  Future<CrisisEvent> getCrisisById(String id) async {
    await _delay();
    return _crisisEvents.firstWhere(
      (c) => c.id == id,
      orElse: () => _crisisEvents.first,
    );
  }

  // ── Alerts Implementations ──
  @override
  Future<List<AlertItem>> getAlerts() async {
    await _delay();
    return List.unmodifiable(_alerts);
  }

  @override
  Future<void> markAlertAsRead(String id) async {
    await _delay();
    final index = _alerts.indexWhere((a) => a.id == id);
    if (index != -1) {
      _alerts[index] = _alerts[index].copyWith(isRead: true);
    }
  }

  // ── AI Responses Implementations ──
  @override
  Future<ResponseDraft> generateResponse({
    required String mentionId,
    required String tone,
    String? customInstructions,
  }) async {
    await _delay();
    final mention = await getMentionById(mentionId);

    String responseBody;
    switch (tone.toLowerCase()) {
      case 'professional':
        responseBody =
            'Dear ${mention.author}, thank you for your feedback regarding your experience at ${mention.platform}. We take all guest commentary into account and our management team is reviewing this with the kitchen department.';
        break;
      case 'firm':
        responseBody = 'We appreciate all genuine patron feedback. However, our records show strict adherence to culinary hygiene standards. If this reflects an actual order, please provide the receipt number so we can investigate immediately.';
        break;
      case 'promotional':
        responseBody =
            'Thank you ${mention.author}! We love delighting food lovers across Bengaluru. Be sure to try our weekend Chef Specials on your next visit!';
        break;
      case 'empathetic':
      default:
        responseBody =
            'Dear ${mention.author}, we are genuinely sorry to hear that your dining experience did not meet our high standards. Quality and customer delight are everything to us. Please reach out to our manager at +91 98765 43210 so we can personally make amends.';
        break;
    }

    if (customInstructions != null && customInstructions.isNotEmpty) {
      responseBody += ' Note: $customInstructions';
    }

    final draft = ResponseDraft(
      id: 'res_${DateTime.now().millisecondsSinceEpoch}',
      mentionId: mentionId,
      originalReview: mention.content,
      generatedResponse: responseBody,
      tone: tone,
      status: 'drafted',
      createdAt: DateTime.now(),
    );

    _responses[draft.id] = draft;

    // Update mention response status
    final mIndex = _mentions.indexWhere((m) => m.id == mentionId);
    if (mIndex != -1) {
      _mentions[mIndex] = _mentions[mIndex].copyWith(
        responseStatus: 'drafted',
        responseText: responseBody,
      );
    }

    return draft;
  }

  @override
  Future<List<ResponseDraft>> getResponses() async {
    await _delay();
    return _responses.values.toList();
  }

  @override
  Future<ResponseDraft> getResponseById(String id) async {
    await _delay();
    final draft = _responses[id];
    if (draft != null) return draft;
    return ResponseDraft(
      id: id,
      mentionId: 'men_1',
      originalReview: 'Sample review',
      generatedResponse: 'Sample response',
      createdAt: DateTime.now(),
    );
  }

  @override
  Future<ResponseDraft> approveResponse({
    required String id,
    required String responseText,
  }) async {
    await _delay();
    final existing = await getResponseById(id);
    final approved = existing.copyWith(
      generatedResponse: responseText,
      status: 'approved',
      approvedAt: DateTime.now(),
    );
    _responses[id] = approved;

    // Update mention
    final mIndex = _mentions.indexWhere((m) => m.id == approved.mentionId);
    if (mIndex != -1) {
      _mentions[mIndex] = _mentions[mIndex].copyWith(
        responseStatus: 'approved',
        responseText: responseText,
      );
    }

    return approved;
  }

  @override
  Future<ResponseDraft> dispatchResponse(String id) async {
    await _delay();
    final existing = await getResponseById(id);
    final dispatched = existing.copyWith(
      status: 'dispatched',
      dispatchedAt: DateTime.now(),
    );
    _responses[id] = dispatched;

    final mIndex = _mentions.indexWhere((m) => m.id == dispatched.mentionId);
    if (mIndex != -1) {
      _mentions[mIndex] = _mentions[mIndex].copyWith(
        responseStatus: 'dispatched',
      );
    }

    return dispatched;
  }
}
