// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'finding_item.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_FindingEvidenceItem _$FindingEvidenceItemFromJson(Map<String, dynamic> json) =>
    _FindingEvidenceItem(
      id: json['id'] as String,
      findingId: json['finding_id'] as String,
      mentionId: json['mention_id'] as String,
      evidenceType: json['evidence_type'] as String? ?? 'review',
      snippet: json['snippet'] as String?,
      relevanceScore: (json['relevance_score'] as num?)?.toDouble() ?? 1.0,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$FindingEvidenceItemToJson(
  _FindingEvidenceItem instance,
) => <String, dynamic>{
  'id': instance.id,
  'finding_id': instance.findingId,
  'mention_id': instance.mentionId,
  'evidence_type': instance.evidenceType,
  'snippet': instance.snippet,
  'relevance_score': instance.relevanceScore,
  'created_at': instance.createdAt.toIso8601String(),
};

_FindingItem _$FindingItemFromJson(Map<String, dynamic> json) => _FindingItem(
  id: json['id'] as String,
  businessId: json['business_id'] as String,
  findingType: json['finding_type'] as String,
  severity: json['severity'] as String? ?? 'medium',
  confidence: (json['confidence'] as num?)?.toDouble() ?? 0.8,
  score: (json['score'] as num?)?.toDouble() ?? 0.0,
  title: json['title'] as String,
  description: json['description'] as String,
  detectedAt: DateTime.parse(json['detected_at'] as String),
  firstSeenAt: DateTime.parse(json['first_seen_at'] as String),
  lastSeenAt: DateTime.parse(json['last_seen_at'] as String),
  metadataJson: json['metadata_json'] as Map<String, dynamic>? ?? const {},
  evidence:
      (json['evidence'] as List<dynamic>?)
          ?.map((e) => FindingEvidenceItem.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
);

Map<String, dynamic> _$FindingItemToJson(_FindingItem instance) =>
    <String, dynamic>{
      'id': instance.id,
      'business_id': instance.businessId,
      'finding_type': instance.findingType,
      'severity': instance.severity,
      'confidence': instance.confidence,
      'score': instance.score,
      'title': instance.title,
      'description': instance.description,
      'detected_at': instance.detectedAt.toIso8601String(),
      'first_seen_at': instance.firstSeenAt.toIso8601String(),
      'last_seen_at': instance.lastSeenAt.toIso8601String(),
      'metadata_json': instance.metadataJson,
      'evidence': instance.evidence,
    };
