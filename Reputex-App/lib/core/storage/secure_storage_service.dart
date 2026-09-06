import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Secure token and credentials storage wrapper around [FlutterSecureStorage].
class SecureStorageService {
  SecureStorageService({FlutterSecureStorage? storage})
    : _storage =
          storage ??
          const FlutterSecureStorage(
            aOptions: AndroidOptions(encryptedSharedPreferences: true),
            iOptions: IOSOptions(
              accessibility: KeychainAccessibility.first_unlock,
            ),
          );

  final FlutterSecureStorage _storage;

  static const String _accessTokenKey = 'reputex_access_token';
  static const String _refreshTokenKey = 'reputex_refresh_token';
  static const String _userIdKey = 'reputex_user_id';
  static const String _userEmailKey = 'reputex_user_email';
  static const String _userNameKey = 'reputex_user_name';
  static const String _businessIdKey = 'reputex_business_id';

  /// Save authentication tokens.
  Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  }) async {
    await _storage.write(key: _accessTokenKey, value: accessToken);
    await _storage.write(key: _refreshTokenKey, value: refreshToken);
  }

  /// Get stored access token.
  Future<String?> getAccessToken() async {
    return _storage.read(key: _accessTokenKey);
  }

  /// Get stored refresh token.
  Future<String?> getRefreshToken() async {
    return _storage.read(key: _refreshTokenKey);
  }

  /// Save user session identifiers.
  Future<void> saveUserSession({
    required String userId,
    required String email,
    required String fullName,
    String? businessId,
  }) async {
    await _storage.write(key: _userIdKey, value: userId);
    await _storage.write(key: _userEmailKey, value: email);
    await _storage.write(key: _userNameKey, value: fullName);
    if (businessId != null) {
      await _storage.write(key: _businessIdKey, value: businessId);
    }
  }

  Future<String?> getUserId() async => _storage.read(key: _userIdKey);
  Future<String?> getUserEmail() async => _storage.read(key: _userEmailKey);
  Future<String?> getUserName() async => _storage.read(key: _userNameKey);
  Future<String?> getBusinessId() async => _storage.read(key: _businessIdKey);

  /// Check if user has an access token stored.
  Future<bool> hasToken() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }

  /// Clear all stored tokens and session data (e.g. on logout).
  Future<void> clearAll() async {
    await _storage.deleteAll();
  }
}
