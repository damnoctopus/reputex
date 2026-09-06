// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'dashboard_summary.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_DashboardSummary _$DashboardSummaryFromJson(Map<String, dynamic> json) =>
    _DashboardSummary(
      reputationScore: ReputationScore.fromJson(
        json['reputation_score'] as Map<String, dynamic>,
      ),
      sentimentDistribution: SentimentDistribution.fromJson(
        json['sentiment_distribution'] as Map<String, dynamic>,
      ),
      totalMentions: (json['total_mentions'] as num?)?.toInt() ?? 0,
      crisisActive: json['crisis_active'] as bool? ?? false,
      crisisCount: (json['crisis_count'] as num?)?.toInt() ?? 0,
      pendingResponsesCount:
          (json['pending_responses_count'] as num?)?.toInt() ?? 0,
      fraudAlertsCount: (json['fraud_alerts_count'] as num?)?.toInt() ?? 0,
      recentMentions:
          (json['recent_mentions'] as List<dynamic>?)
              ?.map((e) => Mention.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
    );

Map<String, dynamic> _$DashboardSummaryToJson(_DashboardSummary instance) =>
    <String, dynamic>{
      'reputation_score': instance.reputationScore,
      'sentiment_distribution': instance.sentimentDistribution,
      'total_mentions': instance.totalMentions,
      'crisis_active': instance.crisisActive,
      'crisis_count': instance.crisisCount,
      'pending_responses_count': instance.pendingResponsesCount,
      'fraud_alerts_count': instance.fraudAlertsCount,
      'recent_mentions': instance.recentMentions,
    };
