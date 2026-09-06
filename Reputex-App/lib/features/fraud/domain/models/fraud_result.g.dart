// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'fraud_result.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_SuspiciousPattern _$SuspiciousPatternFromJson(Map<String, dynamic> json) =>
    _SuspiciousPattern(
      patternName: json['pattern_name'] as String,
      description: json['description'] as String,
      severity: json['severity'] as String? ?? 'medium',
    );

Map<String, dynamic> _$SuspiciousPatternToJson(_SuspiciousPattern instance) =>
    <String, dynamic>{
      'pattern_name': instance.patternName,
      'description': instance.description,
      'severity': instance.severity,
    };

_FraudResult _$FraudResultFromJson(Map<String, dynamic> json) => _FraudResult(
  mentionId: json['mention_id'] as String,
  isFraudulent: json['is_fraudulent'] as bool,
  confidence: (json['confidence'] as num).toDouble(),
  riskLevel: json['risk_level'] as String,
  reasons:
      (json['reasons'] as List<dynamic>?)?.map((e) => e as String).toList() ??
      const [],
  patterns:
      (json['patterns'] as List<dynamic>?)
          ?.map((e) => SuspiciousPattern.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  reviewContent: json['review_content'] as String?,
  author: json['author'] as String?,
  platform: json['platform'] as String?,
  timestamp: json['timestamp'] == null
      ? null
      : DateTime.parse(json['timestamp'] as String),
);

Map<String, dynamic> _$FraudResultToJson(_FraudResult instance) =>
    <String, dynamic>{
      'mention_id': instance.mentionId,
      'is_fraudulent': instance.isFraudulent,
      'confidence': instance.confidence,
      'risk_level': instance.riskLevel,
      'reasons': instance.reasons,
      'patterns': instance.patterns,
      'review_content': instance.reviewContent,
      'author': instance.author,
      'platform': instance.platform,
      'timestamp': instance.timestamp?.toIso8601String(),
    };
