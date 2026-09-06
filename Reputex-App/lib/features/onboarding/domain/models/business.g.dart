// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'business.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_Business _$BusinessFromJson(Map<String, dynamic> json) => _Business(
  id: json['id'] as String,
  name: json['name'] as String,
  category: json['category'] as String,
  website: json['website'] as String?,
  location: json['location'] as String?,
  phone: json['phone'] as String?,
  monitoredPlatforms:
      (json['monitored_platforms'] as List<dynamic>?)
          ?.map((e) => e as String)
          .toList() ??
      const [],
  keywords:
      (json['keywords'] as List<dynamic>?)
          ?.map((e) => BrandKeyword.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  ownerId: json['owner_id'] as String?,
  createdAt: json['created_at'] == null
      ? null
      : DateTime.parse(json['created_at'] as String),
);

Map<String, dynamic> _$BusinessToJson(_Business instance) => <String, dynamic>{
  'id': instance.id,
  'name': instance.name,
  'category': instance.category,
  'website': instance.website,
  'location': instance.location,
  'phone': instance.phone,
  'monitored_platforms': instance.monitoredPlatforms,
  'keywords': instance.keywords,
  'owner_id': instance.ownerId,
  'created_at': instance.createdAt?.toIso8601String(),
};
