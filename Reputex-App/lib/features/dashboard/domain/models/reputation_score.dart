import 'package:freezed_annotation/freezed_annotation.dart';

part 'reputation_score.freezed.dart';
part 'reputation_score.g.dart';

@freezed
abstract class ReputationScore with _$ReputationScore {
  const factory ReputationScore({
    @JsonKey(name: 'current_score') required double currentScore,
    @JsonKey(name: 'previous_score') double? previousScore,
    @Default(0.0) double change,
    @Default('stable') String trend,
    @JsonKey(name: 'calculated_at') DateTime? calculatedAt,
  }) = _ReputationScore;

  factory ReputationScore.fromJson(Map<String, dynamic> json) =>
      _$ReputationScoreFromJson(json);
}
