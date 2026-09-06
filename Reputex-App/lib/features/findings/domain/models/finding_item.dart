import 'package:freezed_annotation/freezed_annotation.dart';

part 'finding_item.freezed.dart';
part 'finding_item.g.dart';

@freezed
abstract class FindingEvidenceItem with _$FindingEvidenceItem {
  const factory FindingEvidenceItem({
    required String id,
    @JsonKey(name: 'finding_id') required String findingId,
    @JsonKey(name: 'mention_id') required String mentionId,
    @JsonKey(name: 'evidence_type') @Default('review') String evidenceType,
    String? snippet,
    @JsonKey(name: 'relevance_score') @Default(1.0) double relevanceScore,
    @JsonKey(name: 'created_at') required DateTime createdAt,
  }) = _FindingEvidenceItem;

  factory FindingEvidenceItem.fromJson(Map<String, dynamic> json) =>
      _$FindingEvidenceItemFromJson(json);
}

@freezed
abstract class FindingItem with _$FindingItem {
  const factory FindingItem({
    required String id,
    @JsonKey(name: 'business_id') required String businessId,
    @JsonKey(name: 'finding_type') required String findingType,
    @Default('medium') String severity,
    @Default(0.8) double confidence,
    @Default(0.0) double score,
    required String title,
    required String description,
    @JsonKey(name: 'detected_at') required DateTime detectedAt,
    @JsonKey(name: 'first_seen_at') required DateTime firstSeenAt,
    @JsonKey(name: 'last_seen_at') required DateTime lastSeenAt,
    @JsonKey(name: 'metadata_json')
    @Default({})
    Map<String, dynamic> metadataJson,
    @Default([]) List<FindingEvidenceItem> evidence,
  }) = _FindingItem;

  factory FindingItem.fromJson(Map<String, dynamic> json) =>
      _$FindingItemFromJson(json);
}
