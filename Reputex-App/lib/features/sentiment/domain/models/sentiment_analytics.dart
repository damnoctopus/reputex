import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:reputex_mobile/features/dashboard/domain/models/platform_statistics.dart';
import 'package:reputex_mobile/features/dashboard/domain/models/sentiment_distribution.dart';
import 'package:reputex_mobile/features/dashboard/domain/models/sentiment_trend.dart';

part 'sentiment_analytics.freezed.dart';
part 'sentiment_analytics.g.dart';

@freezed
abstract class SentimentAnalytics with _$SentimentAnalytics {
  const factory SentimentAnalytics({
    required SentimentDistribution distribution,
    @Default([]) List<SentimentTrend> trends,
    @JsonKey(name: 'platform_breakdown')
    @Default([])
    List<PlatformStatistics> platformBreakdown,
    @JsonKey(name: 'overall_score') @Default(0.0) double overallScore,
    @JsonKey(name: 'total_reviews_analyzed')
    @Default(0)
    int totalReviewsAnalyzed,
  }) = _SentimentAnalytics;

  factory SentimentAnalytics.fromJson(Map<String, dynamic> json) =>
      _$SentimentAnalyticsFromJson(json);
}
