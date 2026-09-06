import 'package:freezed_annotation/freezed_annotation.dart';

part 'fraud_result.freezed.dart';
part 'fraud_result.g.dart';

@freezed
abstract class SuspiciousPattern with _$SuspiciousPattern {
  const factory SuspiciousPattern({
    @JsonKey(name: 'pattern_name') required String patternName,
    required String description,
    @Default('medium') String severity,
  }) = _SuspiciousPattern;

  factory SuspiciousPattern.fromJson(Map<String, dynamic> json) =>
      _$SuspiciousPatternFromJson(json);
}

@freezed
abstract class FraudResult with _$FraudResult {
  const factory FraudResult({
    @JsonKey(name: 'mention_id') required String mentionId,
    @JsonKey(name: 'is_fraudulent') required bool isFraudulent,
    required double confidence,
    @JsonKey(name: 'risk_level') required String riskLevel,
    @Default([]) List<String> reasons,
    @Default([]) List<SuspiciousPattern> patterns,
    @JsonKey(name: 'review_content') String? reviewContent,
    String? author,
    String? platform,
    DateTime? timestamp,
  }) = _FraudResult;

  factory FraudResult.fromJson(Map<String, dynamic> json) =>
      _$FraudResultFromJson(json);
}
