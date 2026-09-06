import 'package:freezed_annotation/freezed_annotation.dart';

part 'platform_statistics.freezed.dart';
part 'platform_statistics.g.dart';

@freezed
abstract class PlatformStatistics with _$PlatformStatistics {
  const factory PlatformStatistics({
    required String platform,
    @Default(0) int count,
    @JsonKey(name: 'positive_percentage')
    @Default(0.0)
    double positivePercentage,
    @JsonKey(name: 'negative_percentage')
    @Default(0.0)
    double negativePercentage,
    @JsonKey(name: 'neutral_percentage') @Default(0.0) double neutralPercentage,
    @JsonKey(name: 'average_rating') double? averageRating,
  }) = _PlatformStatistics;

  factory PlatformStatistics.fromJson(Map<String, dynamic> json) =>
      _$PlatformStatisticsFromJson(json);
}
