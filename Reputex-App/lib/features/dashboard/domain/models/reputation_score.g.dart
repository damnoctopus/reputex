// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'reputation_score.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_ReputationScore _$ReputationScoreFromJson(Map<String, dynamic> json) =>
    _ReputationScore(
      currentScore: (json['current_score'] as num).toDouble(),
      previousScore: (json['previous_score'] as num?)?.toDouble(),
      change: (json['change'] as num?)?.toDouble() ?? 0.0,
      trend: json['trend'] as String? ?? 'stable',
      calculatedAt: json['calculated_at'] == null
          ? null
          : DateTime.parse(json['calculated_at'] as String),
    );

Map<String, dynamic> _$ReputationScoreToJson(_ReputationScore instance) =>
    <String, dynamic>{
      'current_score': instance.currentScore,
      'previous_score': instance.previousScore,
      'change': instance.change,
      'trend': instance.trend,
      'calculated_at': instance.calculatedAt?.toIso8601String(),
    };
