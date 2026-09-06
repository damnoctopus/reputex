import 'dart:io';

import 'package:dio/dio.dart';

import 'app_exception.dart';

/// Maps raw errors (Dio, platform, etc.) to [AppException] subtypes.
class ErrorHandler {
  ErrorHandler._();

  static AppException handle(dynamic error) {
    if (error is AppException) return error;

    if (error is DioException) {
      return _handleDioError(error);
    }

    if (error is SocketException) {
      return const NetworkException();
    }

    return ServerException(message: error.toString());
  }

  static AppException _handleDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return const NetworkException(
          'Connection timed out. Please try again.',
        );

      case DioExceptionType.connectionError:
        return const NetworkException();

      case DioExceptionType.badResponse:
        return _handleStatusCode(
          error.response?.statusCode,
          error.response?.data,
        );

      case DioExceptionType.cancel:
        return const ServerException(message: 'Request was cancelled.');

      case DioExceptionType.badCertificate:
        return const ServerException(message: 'Security certificate error.');

      case DioExceptionType.unknown:
      default:
        if (error.error is SocketException) {
          return const NetworkException();
        }
        return const ServerException();
    }
  }

  static AppException _handleStatusCode(int? statusCode, dynamic data) {
    final serverMessage = _extractMessage(data);

    switch (statusCode) {
      case 400:
        return ValidationException(serverMessage ?? 'Bad request.');
      case 401:
        return AuthException(
          serverMessage ?? 'Session expired. Please log in again.',
        );
      case 403:
        return AuthException(serverMessage ?? 'Access denied.');
      case 404:
        return ServerException(message: serverMessage ?? 'Resource not found.');
      case 422:
        return ValidationException(serverMessage ?? 'Invalid data provided.');
      case 429:
        return const ServerException(
          message: 'Too many requests. Please wait.',
        );
      case 500:
      case 502:
      case 503:
        return const ServerException(
          message: 'Server error. Please try again later.',
        );
      default:
        return ServerException(
          message: serverMessage ?? 'Unexpected error.',
          statusCode: statusCode,
        );
    }
  }

  static String? _extractMessage(dynamic data) {
    if (data is Map<String, dynamic>) {
      return data['message'] as String? ?? data['detail'] as String?;
    }
    return null;
  }
}
