// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'response_draft.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_ResponseDraft _$ResponseDraftFromJson(Map<String, dynamic> json) =>
    _ResponseDraft(
      id: json['id'] as String,
      mentionId: json['mention_id'] as String,
      originalReview: json['original_review'] as String,
      generatedResponse: json['generated_response'] as String,
      tone: json['tone'] as String? ?? 'empathetic',
      status: json['status'] as String? ?? 'drafted',
      createdAt: DateTime.parse(json['created_at'] as String),
      approvedAt: json['approved_at'] == null
          ? null
          : DateTime.parse(json['approved_at'] as String),
      dispatchedAt: json['dispatched_at'] == null
          ? null
          : DateTime.parse(json['dispatched_at'] as String),
    );

Map<String, dynamic> _$ResponseDraftToJson(_ResponseDraft instance) =>
    <String, dynamic>{
      'id': instance.id,
      'mention_id': instance.mentionId,
      'original_review': instance.originalReview,
      'generated_response': instance.generatedResponse,
      'tone': instance.tone,
      'status': instance.status,
      'created_at': instance.createdAt.toIso8601String(),
      'approved_at': instance.approvedAt?.toIso8601String(),
      'dispatched_at': instance.dispatchedAt?.toIso8601String(),
    };
