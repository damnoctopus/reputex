import 'package:freezed_annotation/freezed_annotation.dart';

part 'mention_engagement.freezed.dart';
part 'mention_engagement.g.dart';

@freezed
abstract class MentionEngagement with _$MentionEngagement {
  const factory MentionEngagement({
    @Default(0) int likes,
    @Default(0) int shares,
    @Default(0) int comments,
  }) = _MentionEngagement;

  factory MentionEngagement.fromJson(Map<String, dynamic> json) =>
      _$MentionEngagementFromJson(json);
}
