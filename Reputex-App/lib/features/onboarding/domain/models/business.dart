import 'package:freezed_annotation/freezed_annotation.dart';

import 'brand_keyword.dart';

part 'business.freezed.dart';
part 'business.g.dart';

@freezed
abstract class Business with _$Business {
  const factory Business({
    required String id,
    required String name,
    required String category,
    String? website,
    String? location,
    String? phone,
    @JsonKey(name: 'monitored_platforms')
    @Default([])
    List<String> monitoredPlatforms,
    @Default([]) List<BrandKeyword> keywords,
    @JsonKey(name: 'owner_id') String? ownerId,
    @JsonKey(name: 'created_at') DateTime? createdAt,
  }) = _Business;

  factory Business.fromJson(Map<String, dynamic> json) =>
      _$BusinessFromJson(json);
}
