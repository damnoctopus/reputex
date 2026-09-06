// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'crisis_event.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_CrisisEvent _$CrisisEventFromJson(Map<String, dynamic> json) => _CrisisEvent(
  id: json['id'] as String,
  title: json['title'] as String,
  severity: json['severity'] as String,
  status: json['status'] as String? ?? 'active',
  triggerReason: json['trigger_reason'] as String,
  velocity: (json['velocity'] as num?)?.toDouble() ?? 0.0,
  negativeMentionsCount:
      (json['negative_mentions_count'] as num?)?.toInt() ?? 0,
  affectedPlatforms:
      (json['affected_platforms'] as List<dynamic>?)
          ?.map((e) => e as String)
          .toList() ??
      const [],
  startedAt: DateTime.parse(json['started_at'] as String),
  resolvedAt: json['resolved_at'] == null
      ? null
      : DateTime.parse(json['resolved_at'] as String),
  suggestedActions:
      (json['suggested_actions'] as List<dynamic>?)
          ?.map((e) => e as String)
          .toList() ??
      const [],
  estimatedReach: (json['estimated_reach'] as num?)?.toInt() ?? 0,
  peakVolumePerHour: (json['peak_volume_per_hour'] as num?)?.toInt() ?? 0,
);

Map<String, dynamic> _$CrisisEventToJson(_CrisisEvent instance) =>
    <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'severity': instance.severity,
      'status': instance.status,
      'trigger_reason': instance.triggerReason,
      'velocity': instance.velocity,
      'negative_mentions_count': instance.negativeMentionsCount,
      'affected_platforms': instance.affectedPlatforms,
      'started_at': instance.startedAt.toIso8601String(),
      'resolved_at': instance.resolvedAt?.toIso8601String(),
      'suggested_actions': instance.suggestedActions,
      'estimated_reach': instance.estimatedReach,
      'peak_volume_per_hour': instance.peakVolumePerHour,
    };
