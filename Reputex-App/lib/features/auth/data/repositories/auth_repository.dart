import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/network/api_client_interface.dart';
import '../../../../core/network/api_provider.dart';
import '../../../../core/storage/secure_storage_service.dart';
import '../../domain/models/auth_response.dart';
import '../../domain/models/user.dart';

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  final api = ref.watch(apiServiceProvider);
  final storage = ref.watch(secureStorageProvider);
  return AuthRepository(apiService: api, storageService: storage);
});

class AuthRepository {
  AuthRepository({
    required IApiService apiService,
    required SecureStorageService storageService,
  }) : _api = apiService,
       _storage = storageService;

  final IApiService _api;
  final SecureStorageService _storage;

  /// Check if user has an existing stored session.
  Future<User?> restoreSession() async {
    final hasToken = await _storage.hasToken();
    if (!hasToken) return null;

    try {
      final user = await _api.getCurrentUser();
      await _storage.saveUserSession(
        userId: user.id,
        email: user.email,
        fullName: user.fullName,
        businessId: user.businessId,
      );
      return user;
    } catch (_) {
      // Token invalid or network issue, fallback to stored local identity if available
      final userId = await _storage.getUserId();
      final userEmail = await _storage.getUserEmail();
      final userName = await _storage.getUserName();
      if (userId != null && userEmail != null && userName != null) {
        return User(
          id: userId,
          email: userEmail,
          fullName: userName,
          businessId: await _storage.getBusinessId(),
        );
      }
      return null;
    }
  }

  /// Log in with email and password.
  Future<AuthResponse> login({
    required String email,
    required String password,
  }) async {
    final response = await _api.login(email: email, password: password);

    await _storage.saveTokens(
      accessToken: response.tokens.accessToken,
      refreshToken: response.tokens.refreshToken,
    );
    await _storage.saveUserSession(
      userId: response.user.id,
      email: response.user.email,
      fullName: response.user.fullName,
      businessId: response.user.businessId,
    );

    return response;
  }

  /// Register a new account and business.
  Future<AuthResponse> register({
    required String email,
    required String password,
    required String fullName,
    required String businessName,
    required String businessCategory,
  }) async {
    final response = await _api.register(
      email: email,
      password: password,
      fullName: fullName,
      businessName: businessName,
      businessCategory: businessCategory,
    );

    await _storage.saveTokens(
      accessToken: response.tokens.accessToken,
      refreshToken: response.tokens.refreshToken,
    );
    await _storage.saveUserSession(
      userId: response.user.id,
      email: response.user.email,
      fullName: response.user.fullName,
      businessId: response.user.businessId,
    );

    return response;
  }

  /// Log out and clear stored session.
  Future<void> logout() async {
    try {
      await _api.logout();
    } finally {
      await _storage.clearAll();
    }
  }
}
