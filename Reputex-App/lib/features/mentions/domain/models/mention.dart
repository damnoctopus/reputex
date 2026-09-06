import 'package:freezed_annotation/freezed_annotation.dart';

import 'mention_engagement.dart';

part 'mention.freezed.dart';
part 'mention.g.dart';

@freezed
abstract class Mention with _$Mention {
  const factory Mention({
    required String id,
    required String platform,
    required String author,
    required String content,
    required String sentiment,
    @JsonKey(name: 'sentiment_score') @Default(0.0) double sentimentScore,
    @JsonKey(name: 'is_fake') @Default(false) bool isFake,
    @JsonKey(name: 'fraud_confidence') double? fraudConfidence,
    String? url,
    required DateTime timestamp,
    @Default(MentionEngagement()) MentionEngagement engagement,
    double? rating,
    @JsonKey(name: 'response_status') @Default('none') String responseStatus,
    @JsonKey(name: 'response_text') String? responseText,
    @JsonKey(name: 'author_avatar') String? authorAvatar,
  }) = _Mention;

  factory Mention.fromJson(Map<String, dynamic> json) =>
      _$MentionFromJson(json);
}
