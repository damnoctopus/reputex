import 'package:freezed_annotation/freezed_annotation.dart';

part 'brand_keyword.freezed.dart';
part 'brand_keyword.g.dart';

@freezed
abstract class BrandKeyword with _$BrandKeyword {
  const factory BrandKeyword({
    required String id,
    required String keyword,
    @Default('brand') String category,
    @JsonKey(name: 'is_active') @Default(true) bool isActive,
    @JsonKey(name: 'business_id') String? businessId,
  }) = _BrandKeyword;

  factory BrandKeyword.fromJson(Map<String, dynamic> json) =>
      _$BrandKeywordFromJson(json);
}
