import 'package:freezed_annotation/freezed_annotation.dart';

import 'mention.dart';

part 'paginated_mentions.freezed.dart';
part 'paginated_mentions.g.dart';

@freezed
abstract class PaginatedMentions with _$PaginatedMentions {
  const factory PaginatedMentions({
    required List<Mention> items,
    @JsonKey(name: 'total_count') required int totalCount,
    @Default(1) int page,
    @JsonKey(name: 'total_pages') @Default(1) int totalPages,
    @JsonKey(name: 'has_more') @Default(false) bool hasMore,
  }) = _PaginatedMentions;

  factory PaginatedMentions.fromJson(Map<String, dynamic> json) =>
      _$PaginatedMentionsFromJson(json);
}
