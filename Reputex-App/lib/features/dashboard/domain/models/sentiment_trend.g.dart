// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'sentiment_trend.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_SentimentTrend _$SentimentTrendFromJson(Map<String, dynamic> json) =>
    _SentimentTrend(
      date: json['date'] as String,
      positive: (json['positive'] as num?)?.toInt() ?? 0,
      neutral: (json['neutral'] as num?)?.toInt() ?? 0,
      negative: (json['negative'] as num?)?.toInt() ?? 0,
      score: (json['score'] as num?)?.toDouble() ?? 0.0,
    );

Map<String, dynamic> _$SentimentTrendToJson(_SentimentTrend instance) =>
    <String, dynamic>{
      'date': instance.date,
      'positive': instance.positive,
      'neutral': instance.neutral,
      'negative': instance.negative,
      'score': instance.score,
    };
