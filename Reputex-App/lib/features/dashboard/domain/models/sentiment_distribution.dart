import 'package:freezed_annotation/freezed_annotation.dart';

part 'sentiment_distribution.freezed.dart';
part 'sentiment_distribution.g.dart';

@freezed
abstract class SentimentDistribution with _$SentimentDistribution {
  const factory SentimentDistribution({
    @Default(0) int positive,
    @Default(0) int neutral,
    @Default(0) int negative,
    @Default(0) int total,
    @JsonKey(name: 'positive_percentage')
    @Default(0.0)
    double positivePercentage,
    @JsonKey(name: 'neutral_percentage') @Default(0.0) double neutralPercentage,
    @JsonKey(name: 'negative_percentage')
    @Default(0.0)
    double negativePercentage,
  }) = _SentimentDistribution;

  factory SentimentDistribution.fromJson(Map<String, dynamic> json) =>
      _$SentimentDistributionFromJson(json);
}
