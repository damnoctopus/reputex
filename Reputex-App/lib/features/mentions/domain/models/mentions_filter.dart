import 'package:freezed_annotation/freezed_annotation.dart';

part 'mentions_filter.freezed.dart';
part 'mentions_filter.g.dart';

@freezed
abstract class MentionsFilter with _$MentionsFilter {
  const factory MentionsFilter({
    String? platform,
    String? sentiment,
    @JsonKey(name: 'is_fake') bool? isFake,
    @JsonKey(name: 'search_query') String? searchQuery,
    @Default(1) int page,
    @Default(20) int limit,
    @JsonKey(name: 'sort_by') @Default('newest') String sortBy,
  }) = _MentionsFilter;

  factory MentionsFilter.fromJson(Map<String, dynamic> json) =>
      _$MentionsFilterFromJson(json);
}
