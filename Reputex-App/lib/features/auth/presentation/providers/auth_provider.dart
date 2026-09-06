import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/auth_repository.dart';
import '../../domain/models/user.dart';

/// Authentication state holder.
class AuthState {
  const AuthState({
    this.user,
    this.isLoading = false,
    this.errorMessage,
    this.isInitialized = false,
  });

  final User? user;
  final bool isLoading;
  final String? errorMessage;
  final bool isInitialized;

  bool get isAuthenticated => user != null;

  AuthState copyWith({
    User? user,
    bool? isLoading,
    String? errorMessage,
    bool? isInitialized,
    bool clearUser = false,
    bool clearError = false,
  }) {
    return AuthState(
      user: clearUser ? null : (user ?? this.user),
      isLoading: isLoading ?? this.isLoading,
      errorMessage: clearError ? null : (errorMessage ?? this.errorMessage),
      isInitialized: isInitialized ?? this.isInitialized,
    );
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier({required AuthRepository authRepository})
    : _repository = authRepository,
      super(const AuthState()) {
    restoreSession();
  }

  final AuthRepository _repository;

  /// Check stored token and restore session on app launch.
  Future<void> restoreSession() async {
    state = state.copyWith(isLoading: true, clearError: true);
    try {
      final user = await _repository.restoreSession();
      state = state.copyWith(user: user, isLoading: false, isInitialized: true);
    } catch (_) {
      state = state.copyWith(
        clearUser: true,
        isLoading: false,
        isInitialized: true,
      );
    }
  }

  /// Log in with email and password.
  Future<bool> login({required String email, required String password}) async {
    state = state.copyWith(isLoading: true, clearError: true);
    try {
      final response = await _repository.login(
        email: email,
        password: password,
      );
      state = state.copyWith(user: response.user, isLoading: false);
      return true;
    } catch (e) {
      state = state.copyWith(isLoading: false, errorMessage: e.toString());
      return false;
    }
  }

  /// Register new user and business.
  Future<bool> register({
    required String email,
    required String password,
    required String fullName,
    required String businessName,
    required String businessCategory,
  }) async {
    state = state.copyWith(isLoading: true, clearError: true);
    try {
      final response = await _repository.register(
        email: email,
        password: password,
        fullName: fullName,
        businessName: businessName,
        businessCategory: businessCategory,
      );
      state = state.copyWith(user: response.user, isLoading: false);
      return true;
    } catch (e) {
      state = state.copyWith(isLoading: false, errorMessage: e.toString());
      return false;
    }
  }

  /// Log out and clear state.
  Future<void> logout() async {
    state = state.copyWith(isLoading: true);
    try {
      await _repository.logout();
    } finally {
      state = const AuthState(isInitialized: true);
    }
  }

  void clearError() {
    state = state.copyWith(clearError: true);
  }
}

/// Global authentication provider.
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  final repo = ref.watch(authRepositoryProvider);
  return AuthNotifier(authRepository: repo);
});
