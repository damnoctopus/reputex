// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'mention.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_Mention _$MentionFromJson(Map<String, dynamic> json) => _Mention(
  id: json['id'] as String,
  platform: json['platform'] as String,
  author: json['author'] as String,
  content: json['content'] as String,
  sentiment: json['sentiment'] as String,
  sentimentScore: (json['sentiment_score'] as num?)?.toDouble() ?? 0.0,
  isFake: json['is_fake'] as bool? ?? false,
  fraudConfidence: (json['fraud_confidence'] as num?)?.toDouble(),
  url: json['url'] as String?,
  timestamp: DateTime.parse(json['timestamp'] as String),
  engagement: json['engagement'] == null
      ? const MentionEngagement()
      : MentionEngagement.fromJson(json['engagement'] as Map<String, dynamic>),
  rating: (json['rating'] as num?)?.toDouble(),
  responseStatus: json['response_status'] as String? ?? 'none',
  responseText: json['response_text'] as String?,
  authorAvatar: json['author_avatar'] as String?,
);

Map<String, dynamic> _$MentionToJson(_Mention instance) => <String, dynamic>{
  'id': instance.id,
  'platform': instance.platform,
  'author': instance.author,
  'content': instance.content,
  'sentiment': instance.sentiment,
  'sentiment_score': instance.sentimentScore,
  'is_fake': instance.isFake,
  'fraud_confidence': instance.fraudConfidence,
  'url': instance.url,
  'timestamp': instance.timestamp.toIso8601String(),
  'engagement': instance.engagement,
  'rating': instance.rating,
  'response_status': instance.responseStatus,
  'response_text': instance.responseText,
  'author_avatar': instance.authorAvatar,
};
