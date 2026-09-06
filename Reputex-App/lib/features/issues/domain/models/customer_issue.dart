import 'package:freezed_annotation/freezed_annotation.dart';

part 'customer_issue.freezed.dart';
part 'customer_issue.g.dart';

@freezed
abstract class IssueEvidence with _$IssueEvidence {
  const factory IssueEvidence({
    required String id,
    @JsonKey(name: 'mention_id') required String mentionId,
    @JsonKey(name: 'relevance_score') @Default(1.0) double relevanceScore,
    String? excerpt,
    @JsonKey(name: 'created_at') required DateTime createdAt,
  }) = _IssueEvidence;

  factory IssueEvidence.fromJson(Map<String, dynamic> json) =>
      _$IssueEvidenceFromJson(json);
}

@freezed
abstract class CustomerIssue with _$CustomerIssue {
  const factory CustomerIssue({
    required String id,
    @JsonKey(name: 'business_id') required String businessId,
    required String category,
    required String subtopic,
    @Default('medium') String severity,
    @Default('emerging') String status,
    @JsonKey(name: 'mention_count') @Default(0) int mentionCount,
    @JsonKey(name: 'platforms_breakdown')
    @Default({})
    Map<String, int> platformsBreakdown,
    @JsonKey(name: 'sentiment_breakdown')
    @Default({})
    Map<String, int> sentimentBreakdown,
    @JsonKey(name: 'first_seen_at') required DateTime firstSeenAt,
    @JsonKey(name: 'last_seen_at') required DateTime lastSeenAt,
    @Default([]) List<IssueEvidence> evidence,
  }) = _CustomerIssue;

  factory CustomerIssue.fromJson(Map<String, dynamic> json) =>
      _$CustomerIssueFromJson(json);
}
