// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'alert_item.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_AlertItem _$AlertItemFromJson(Map<String, dynamic> json) => _AlertItem(
  id: json['id'] as String,
  type: json['type'] as String,
  title: json['title'] as String,
  message: json['message'] as String,
  severity: json['severity'] as String? ?? 'medium',
  timestamp: DateTime.parse(json['timestamp'] as String),
  isRead: json['is_read'] as bool? ?? false,
  referenceId: json['reference_id'] as String?,
  referenceType: json['reference_type'] as String?,
);

Map<String, dynamic> _$AlertItemToJson(_AlertItem instance) =>
    <String, dynamic>{
      'id': instance.id,
      'type': instance.type,
      'title': instance.title,
      'message': instance.message,
      'severity': instance.severity,
      'timestamp': instance.timestamp.toIso8601String(),
      'is_read': instance.isRead,
      'reference_id': instance.referenceId,
      'reference_type': instance.referenceType,
    };
