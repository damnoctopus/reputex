// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'customer_issue.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_IssueEvidence _$IssueEvidenceFromJson(Map<String, dynamic> json) =>
    _IssueEvidence(
      id: json['id'] as String,
      mentionId: json['mention_id'] as String,
      relevanceScore: (json['relevance_score'] as num?)?.toDouble() ?? 1.0,
      excerpt: json['excerpt'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$IssueEvidenceToJson(_IssueEvidence instance) =>
    <String, dynamic>{
      'id': instance.id,
      'mention_id': instance.mentionId,
      'relevance_score': instance.relevanceScore,
      'excerpt': instance.excerpt,
      'created_at': instance.createdAt.toIso8601String(),
    };

_CustomerIssue _$CustomerIssueFromJson(Map<String, dynamic> json) =>
    _CustomerIssue(
      id: json['id'] as String,
      businessId: json['business_id'] as String,
      category: json['category'] as String,
      subtopic: json['subtopic'] as String,
      severity: json['severity'] as String? ?? 'medium',
      status: json['status'] as String? ?? 'emerging',
      mentionCount: (json['mention_count'] as num?)?.toInt() ?? 0,
      platformsBreakdown:
          (json['platforms_breakdown'] as Map<String, dynamic>?)?.map(
            (k, e) => MapEntry(k, (e as num).toInt()),
          ) ??
          const {},
      sentimentBreakdown:
          (json['sentiment_breakdown'] as Map<String, dynamic>?)?.map(
            (k, e) => MapEntry(k, (e as num).toInt()),
          ) ??
          const {},
      firstSeenAt: DateTime.parse(json['first_seen_at'] as String),
      lastSeenAt: DateTime.parse(json['last_seen_at'] as String),
      evidence:
          (json['evidence'] as List<dynamic>?)
              ?.map((e) => IssueEvidence.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
    );

Map<String, dynamic> _$CustomerIssueToJson(_CustomerIssue instance) =>
    <String, dynamic>{
      'id': instance.id,
      'business_id': instance.businessId,
      'category': instance.category,
      'subtopic': instance.subtopic,
      'severity': instance.severity,
      'status': instance.status,
      'mention_count': instance.mentionCount,
      'platforms_breakdown': instance.platformsBreakdown,
      'sentiment_breakdown': instance.sentimentBreakdown,
      'first_seen_at': instance.firstSeenAt.toIso8601String(),
      'last_seen_at': instance.lastSeenAt.toIso8601String(),
      'evidence': instance.evidence,
    };
