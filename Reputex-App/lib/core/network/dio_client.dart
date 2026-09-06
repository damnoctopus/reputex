import 'package:dio/dio.dart';

import '../constants/api_constants.dart';
import '../errors/app_exception.dart';
import '../errors/error_handler.dart';
import '../storage/secure_storage_service.dart';

/// Centralized Dio HTTP client configured with JWT interceptors,
/// token refresh handling, and error mapping.
class DioClient {
  DioClient({required this.storageService, Dio? dio}) : _dio = dio ?? Dio() {
    _dio.options = BaseOptions(
      baseUrl: ApiConstants.baseUrl,
      connectTimeout: ApiConstants.connectTimeout,
      receiveTimeout: ApiConstants.receiveTimeout,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    );

    _dio.interceptors.addAll([
      _AuthInterceptor(dio: _dio, storageService: storageService),
      LogInterceptor(
        requestBody: true,
        responseBody: true,
        logPrint: (obj) {
          // Log only in debug mode without spamming
        },
      ),
    ]);
  }

  final Dio _dio;
  final SecureStorageService storageService;

  Dio get dio => _dio;

  /// GET request
  Future<Response<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
  }) async {
    try {
      return await _dio.get<T>(
        path,
        queryParameters: queryParameters,
        options: options,
        cancelToken: cancelToken,
      );
    } catch (e) {
      throw ErrorHandler.handle(e);
    }
  }

  /// POST request
  Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
  }) async {
    try {
      return await _dio.post<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
        cancelToken: cancelToken,
      );
    } catch (e) {
      throw ErrorHandler.handle(e);
    }
  }

  /// PUT request
  Future<Response<T>> put<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
  }) async {
    try {
      return await _dio.put<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
        cancelToken: cancelToken,
      );
    } catch (e) {
      throw ErrorHandler.handle(e);
    }
  }

  /// DELETE request
  Future<Response<T>> delete<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
  }) async {
    try {
      return await _dio.delete<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
        cancelToken: cancelToken,
      );
    } catch (e) {
      throw ErrorHandler.handle(e);
    }
  }
}

/// JWT interceptor that attaches bearer token and handles 401 token refreshes.
class _AuthInterceptor extends QueuedInterceptor {
  _AuthInterceptor({required this.dio, required this.storageService});

  final Dio dio;
  final SecureStorageService storageService;

  bool _isAuthEndpoint(String path) {
    return path.contains(ApiConstants.login) ||
        path.contains(ApiConstants.register) ||
        path.contains(ApiConstants.refreshToken);
  }

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    if (!_isAuthEndpoint(options.path)) {
      final token = await storageService.getAccessToken();
      if (token != null && token.isNotEmpty) {
        options.headers['Authorization'] = 'Bearer $token';
      }
    }
    handler.next(options);
  }

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    if (err.response?.statusCode == 401 &&
        !_isAuthEndpoint(err.requestOptions.path)) {
      // Attempt token refresh
      final refreshToken = await storageService.getRefreshToken();
      if (refreshToken != null && refreshToken.isNotEmpty) {
        try {
          // Create isolated Dio to prevent infinite interceptor loop
          final refreshDio = Dio(
            BaseOptions(
              baseUrl: ApiConstants.baseUrl,
              connectTimeout: ApiConstants.connectTimeout,
            ),
          );

          final response = await refreshDio.post(
            ApiConstants.refreshToken,
            data: {'refresh_token': refreshToken},
          );

          if (response.statusCode == 200 && response.data != null) {
            final newAccessToken = response.data['access_token'] as String;
            final newRefreshToken =
                response.data['refresh_token'] as String? ?? refreshToken;

            await storageService.saveTokens(
              accessToken: newAccessToken,
              refreshToken: newRefreshToken,
            );

            // Retry original request with new token
            final requestOptions = err.requestOptions;
            requestOptions.headers['Authorization'] = 'Bearer $newAccessToken';

            final retryResponse = await dio.fetch(requestOptions);
            return handler.resolve(retryResponse);
          }
        } catch (_) {
          // Token refresh failed, clear session
          await storageService.clearAll();
          return handler.reject(
            DioException(
              requestOptions: err.requestOptions,
              error: const AuthException(
                'Session expired. Please log in again.',
              ),
              type: DioExceptionType.badResponse,
            ),
          );
        }
      }
    }

    handler.next(err);
  }
}
