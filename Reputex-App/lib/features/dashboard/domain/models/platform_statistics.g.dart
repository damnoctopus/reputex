// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'platform_statistics.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_PlatformStatistics _$PlatformStatisticsFromJson(
  Map<String, dynamic> json,
) => _PlatformStatistics(
  platform: json['platform'] as String,
  count: (json['count'] as num?)?.toInt() ?? 0,
  positivePercentage: (json['positive_percentage'] as num?)?.toDouble() ?? 0.0,
  negativePercentage: (json['negative_percentage'] as num?)?.toDouble() ?? 0.0,
  neutralPercentage: (json['neutral_percentage'] as num?)?.toDouble() ?? 0.0,
  averageRating: (json['average_rating'] as num?)?.toDouble(),
);

Map<String, dynamic> _$PlatformStatisticsToJson(_PlatformStatistics instance) =>
    <String, dynamic>{
      'platform': instance.platform,
      'count': instance.count,
      'positive_percentage': instance.positivePercentage,
      'negative_percentage': instance.negativePercentage,
      'neutral_percentage': instance.neutralPercentage,
      'average_rating': instance.averageRating,
    };
