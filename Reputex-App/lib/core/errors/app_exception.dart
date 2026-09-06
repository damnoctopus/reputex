/// Custom exception hierarchy for RepuTex.
///
/// All exceptions thrown by the data layer are mapped to one of these
/// types so the presentation layer can display appropriate error messages.
sealed class AppException implements Exception {
  const AppException(this.message);
  final String message;

  @override
  String toString() => message;
}

/// Network-related errors (no internet, timeout, DNS).
class NetworkException extends AppException {
  const NetworkException([
    super.message = 'Network error. Please check your connection.',
  ]);
}

/// Authentication errors (invalid credentials, expired token).
class AuthException extends AppException {
  const AuthException([
    super.message = 'Authentication failed. Please log in again.',
  ]);
}

/// Backend returned an error response.
class ServerException extends AppException {
  const ServerException({
    String message = 'Something went wrong. Please try again.',
    this.statusCode,
  }) : super(message);

  final int? statusCode;
}

/// Local cache/storage errors.
class CacheException extends AppException {
  const CacheException([super.message = 'Failed to access local storage.']);
}

/// Validation errors (bad input).
class ValidationException extends AppException {
  const ValidationException([
    super.message = 'Invalid input. Please check your data.',
  ]);
}
