import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../storage/secure_storage_service.dart';
import 'api_client_interface.dart';
import 'dio_client.dart';
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

/// Real API service provider using Dio.
final realApiServiceProvider = Provider<RealApiService>((ref) {
  final client = ref.watch(dioClientProvider);
  return RealApiService(dioClient: client);
});

/// Active [IApiService] provider pointing to the live FastAPI backend.
final apiServiceProvider = Provider<IApiService>((ref) {
  return ref.watch(realApiServiceProvider);
});
