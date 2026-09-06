import 'package:freezed_annotation/freezed_annotation.dart';

part 'sentiment_trend.freezed.dart';
part 'sentiment_trend.g.dart';

@freezed
abstract class SentimentTrend with _$SentimentTrend {
  const factory SentimentTrend({
    required String date,
    @Default(0) int positive,
    @Default(0) int neutral,
    @Default(0) int negative,
    @Default(0.0) double score,
  }) = _SentimentTrend;

  factory SentimentTrend.fromJson(Map<String, dynamic> json) =>
      _$SentimentTrendFromJson(json);
}
