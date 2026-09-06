import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../constants/api_constants.dart';
import '../storage/secure_storage_service.dart';
import 'api_client_interface.dart';
import 'dio_client.dart';
import 'mock_api_service.dart';
import 'real_api_service.dart';

/// Provides the persistent secure storage instance.
final secureStorageProvider = Provider<SecureStorageService>((ref) {
  return SecureStorageService();
});

/// Provides the configured Dio HTTP client.
final dioClientProvider = Provider<DioClient>((ref) {
  final storage = ref.watch(secureStorageProvider);
  return DioClient(storageService: storage);
});

/// Global configuration flag to toggle between mock and real API.
/// Defaults to [ApiConstants.useMockApi] (true).
final useMockApiProvider = StateProvider<bool>((ref) {
  return ApiConstants.useMockApi;
});

/// Mock API service provider (singleton in memory).
final mockApiServiceProvider = Provider<MockApiService>((ref) {
  return MockApiService();
});

/// Real API service provider using Dio.
final realApiServiceProvider = Provider<RealApiService>((ref) {
  final client = ref.watch(dioClientProvider);
  return RealApiService(dioClient: client);
});

/// Active [IApiService] provider.
///
/// Swapping between MockApiService and RealApiService is achieved
/// automatically by toggling [useMockApiProvider].
final apiServiceProvider = Provider<IApiService>((ref) {
  final useMock = ref.watch(useMockApiProvider);
  if (useMock) {
    return ref.watch(mockApiServiceProvider);
  } else {
    return ref.watch(realApiServiceProvider);
  }
});
