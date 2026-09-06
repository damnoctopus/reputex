// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'sentiment_analytics.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_SentimentAnalytics _$SentimentAnalyticsFromJson(
  Map<String, dynamic> json,
) => _SentimentAnalytics(
  distribution: SentimentDistribution.fromJson(
    json['distribution'] as Map<String, dynamic>,
  ),
  trends:
      (json['trends'] as List<dynamic>?)
          ?.map((e) => SentimentTrend.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  platformBreakdown:
      (json['platform_breakdown'] as List<dynamic>?)
          ?.map((e) => PlatformStatistics.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  overallScore: (json['overall_score'] as num?)?.toDouble() ?? 0.0,
  totalReviewsAnalyzed: (json['total_reviews_analyzed'] as num?)?.toInt() ?? 0,
);

Map<String, dynamic> _$SentimentAnalyticsToJson(_SentimentAnalytics instance) =>
    <String, dynamic>{
      'distribution': instance.distribution,
      'trends': instance.trends,
      'platform_breakdown': instance.platformBreakdown,
      'overall_score': instance.overallScore,
      'total_reviews_analyzed': instance.totalReviewsAnalyzed,
    };
