/// Application-wide constants.
class AppConstants {
  AppConstants._();

  static const String appName = 'RepuTex';
  static const String appTagline = 'AI-Powered Reputation Intelligence';

  // ── Pagination ──
  static const int defaultPageSize = 20;

  // ── Platforms ──
  static const List<String> platforms = [
    'Reddit',
    'X',
    'Google News',
    'JustDial',
    'Sulekha',
    'IndiaMART',
  ];

  // ── Sentiment labels ──
  static const String positive = 'Positive';
  static const String neutral = 'Neutral';
  static const String negative = 'Negative';

  // ── Risk levels ──
  static const String riskCritical = 'Critical';
  static const String riskHigh = 'High';
  static const String riskMedium = 'Medium';
  static const String riskLow = 'Low';

  // ── Response tones ──
  static const List<String> responseTones = [
    'Professional',
    'Friendly',
    'Apologetic',
    'Concise',
  ];

  // ── Notification types ──
  static const String crisisDetected = 'CRISIS_DETECTED';
  static const String crisisResolved = 'CRISIS_RESOLVED';
  static const String highFraudActivity = 'HIGH_FRAUD_ACTIVITY';
  static const String newNegativeSpike = 'NEW_NEGATIVE_SPIKE';
  static const String aiResponseReady = 'AI_RESPONSE_READY';

  // ── Crisis defaults ──
  static const double defaultCrisisThreshold = 40.0;
  static const Duration crisisTimeWindow = Duration(hours: 2);
}
