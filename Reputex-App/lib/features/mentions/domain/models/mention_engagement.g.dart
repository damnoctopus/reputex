// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'mention_engagement.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_MentionEngagement _$MentionEngagementFromJson(Map<String, dynamic> json) =>
    _MentionEngagement(
      likes: (json['likes'] as num?)?.toInt() ?? 0,
      shares: (json['shares'] as num?)?.toInt() ?? 0,
      comments: (json['comments'] as num?)?.toInt() ?? 0,
    );

Map<String, dynamic> _$MentionEngagementToJson(_MentionEngagement instance) =>
    <String, dynamic>{
      'likes': instance.likes,
      'shares': instance.shares,
      'comments': instance.comments,
    };
