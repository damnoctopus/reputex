import 'package:freezed_annotation/freezed_annotation.dart';

part 'response_draft.freezed.dart';
part 'response_draft.g.dart';

@freezed
abstract class ResponseDraft with _$ResponseDraft {
  const factory ResponseDraft({
    required String id,
    @JsonKey(name: 'mention_id') required String mentionId,
    @JsonKey(name: 'original_review') required String originalReview,
    @JsonKey(name: 'generated_response') required String generatedResponse,
    @Default('empathetic') String tone,
    @Default('drafted') String status,
    @JsonKey(name: 'created_at') required DateTime createdAt,
    @JsonKey(name: 'approved_at') DateTime? approvedAt,
    @JsonKey(name: 'dispatched_at') DateTime? dispatchedAt,
  }) = _ResponseDraft;

  factory ResponseDraft.fromJson(Map<String, dynamic> json) =>
      _$ResponseDraftFromJson(json);
}
