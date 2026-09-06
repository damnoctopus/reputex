import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:reputex_mobile/features/mentions/domain/models/mention.dart';

import 'reputation_score.dart';
import 'sentiment_distribution.dart';

part 'dashboard_summary.freezed.dart';
part 'dashboard_summary.g.dart';

@freezed
abstract class DashboardSummary with _$DashboardSummary {
  const factory DashboardSummary({
    @JsonKey(name: 'reputation_score') required ReputationScore reputationScore,
    @JsonKey(name: 'sentiment_distribution')
    required SentimentDistribution sentimentDistribution,
    @JsonKey(name: 'total_mentions') @Default(0) int totalMentions,
    @JsonKey(name: 'crisis_active') @Default(false) bool crisisActive,
    @JsonKey(name: 'crisis_count') @Default(0) int crisisCount,
    @JsonKey(name: 'pending_responses_count')
    @Default(0)
    int pendingResponsesCount,
    @JsonKey(name: 'fraud_alerts_count') @Default(0) int fraudAlertsCount,
    @JsonKey(name: 'recent_mentions') @Default([]) List<Mention> recentMentions,
  }) = _DashboardSummary;

  factory DashboardSummary.fromJson(Map<String, dynamic> json) =>
      _$DashboardSummaryFromJson(json);
}
