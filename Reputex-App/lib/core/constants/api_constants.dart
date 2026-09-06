/// API endpoint constants for the RepuTex backend.
///
/// All paths are relative to [baseUrl]. The mobile app accesses
/// everything through these endpoints via the API abstraction layer.
class ApiConstants {
  ApiConstants._();

  /// Toggle between mock and real backend.
  static const bool useMockApi = true;

  /// Base URL for the FastAPI backend.
  static const String baseUrl = 'http://10.0.2.2:8000/api';

  /// Request timeout.
  static const Duration connectTimeout = Duration(seconds: 15);
  static const Duration receiveTimeout = Duration(seconds: 15);

  // ── Authentication ──
  static const String login = '/auth/login';
  static const String register = '/auth/register';
  static const String refreshToken = '/auth/refresh';
  static const String logout = '/auth/logout';

  // ── Business ──
  static const String business = '/business';

  // ── Keywords ──
  static const String keywords = '/keywords';

  // ── Dashboard ──
  static const String dashboard = '/dashboard';
  static const String dashboardSentiment = '/dashboard/sentiment';
  static const String dashboardPlatforms = '/dashboard/platforms';
  static const String dashboardTrends = '/dashboard/trends';

  // ── Mentions ──
  static const String mentions = '/mentions';

  // ── Fraud ──
  static const String fraud = '/fraud';

  // ── Crisis ──
  static const String crisis = '/crisis';
  static const String crisisActive = '/crisis/active';

  // ── Alerts ──
  static const String alerts = '/alerts';

  // ── AI Responses ──
  static const String responses = '/responses';
  static const String responsesGenerate = '/responses/generate';

  // ── Devices (FCM) ──
  static const String devicesRegister = '/devices/register';
}
