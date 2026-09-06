// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'brand_keyword.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_BrandKeyword _$BrandKeywordFromJson(Map<String, dynamic> json) =>
    _BrandKeyword(
      id: json['id'] as String,
      keyword: json['keyword'] as String,
      category: json['category'] as String? ?? 'brand',
      isActive: json['is_active'] as bool? ?? true,
      businessId: json['business_id'] as String?,
    );

Map<String, dynamic> _$BrandKeywordToJson(_BrandKeyword instance) =>
    <String, dynamic>{
      'id': instance.id,
      'keyword': instance.keyword,
      'category': instance.category,
      'is_active': instance.isActive,
      'business_id': instance.businessId,
    };
