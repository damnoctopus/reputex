import 'package:freezed_annotation/freezed_annotation.dart';

part 'crisis_event.freezed.dart';
part 'crisis_event.g.dart';

@freezed
abstract class CrisisEvent with _$CrisisEvent {
  const factory CrisisEvent({
    required String id,
    required String title,
    required String severity,
    @Default('active') String status,
    @JsonKey(name: 'trigger_reason') required String triggerReason,
    @Default(0.0) double velocity,
    @JsonKey(name: 'negative_mentions_count')
    @Default(0)
    int negativeMentionsCount,
    @JsonKey(name: 'affected_platforms')
    @Default([])
    List<String> affectedPlatforms,
    @JsonKey(name: 'started_at') required DateTime startedAt,
    @JsonKey(name: 'resolved_at') DateTime? resolvedAt,
    @JsonKey(name: 'suggested_actions')
    @Default([])
    List<String> suggestedActions,
    @JsonKey(name: 'estimated_reach') @Default(0) int estimatedReach,
    @JsonKey(name: 'peak_volume_per_hour') @Default(0) int peakVolumePerHour,
  }) = _CrisisEvent;

  factory CrisisEvent.fromJson(Map<String, dynamic> json) =>
      _$CrisisEventFromJson(json);
}
