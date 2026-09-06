// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'paginated_mentions.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_PaginatedMentions _$PaginatedMentionsFromJson(Map<String, dynamic> json) =>
    _PaginatedMentions(
      items: (json['items'] as List<dynamic>)
          .map((e) => Mention.fromJson(e as Map<String, dynamic>))
          .toList(),
      totalCount: (json['total_count'] as num).toInt(),
      page: (json['page'] as num?)?.toInt() ?? 1,
      totalPages: (json['total_pages'] as num?)?.toInt() ?? 1,
      hasMore: json['has_more'] as bool? ?? false,
    );

Map<String, dynamic> _$PaginatedMentionsToJson(_PaginatedMentions instance) =>
    <String, dynamic>{
      'items': instance.items,
      'total_count': instance.totalCount,
      'page': instance.page,
      'total_pages': instance.totalPages,
      'has_more': instance.hasMore,
    };
