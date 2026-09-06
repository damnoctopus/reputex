// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'sentiment_distribution.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_SentimentDistribution _$SentimentDistributionFromJson(
  Map<String, dynamic> json,
) => _SentimentDistribution(
  positive: (json['positive'] as num?)?.toInt() ?? 0,
  neutral: (json['neutral'] as num?)?.toInt() ?? 0,
  negative: (json['negative'] as num?)?.toInt() ?? 0,
  total: (json['total'] as num?)?.toInt() ?? 0,
  positivePercentage: (json['positive_percentage'] as num?)?.toDouble() ?? 0.0,
  neutralPercentage: (json['neutral_percentage'] as num?)?.toDouble() ?? 0.0,
  negativePercentage: (json['negative_percentage'] as num?)?.toDouble() ?? 0.0,
);

Map<String, dynamic> _$SentimentDistributionToJson(
  _SentimentDistribution instance,
) => <String, dynamic>{
  'positive': instance.positive,
  'neutral': instance.neutral,
  'negative': instance.negative,
  'total': instance.total,
  'positive_percentage': instance.positivePercentage,
  'neutral_percentage': instance.neutralPercentage,
  'negative_percentage': instance.negativePercentage,
};
