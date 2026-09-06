// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'mentions_filter.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_MentionsFilter _$MentionsFilterFromJson(Map<String, dynamic> json) =>
    _MentionsFilter(
      platform: json['platform'] as String?,
      sentiment: json['sentiment'] as String?,
      isFake: json['is_fake'] as bool?,
      searchQuery: json['search_query'] as String?,
      page: (json['page'] as num?)?.toInt() ?? 1,
      limit: (json['limit'] as num?)?.toInt() ?? 20,
      sortBy: json['sort_by'] as String? ?? 'newest',
    );

Map<String, dynamic> _$MentionsFilterToJson(_MentionsFilter instance) =>
    <String, dynamic>{
      'platform': instance.platform,
      'sentiment': instance.sentiment,
      'is_fake': instance.isFake,
      'search_query': instance.searchQuery,
      'page': instance.page,
      'limit': instance.limit,
      'sort_by': instance.sortBy,
    };
