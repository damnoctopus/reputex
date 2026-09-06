// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'reputation_score.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$ReputationScore {

@JsonKey(name: 'current_score') double get currentScore;@JsonKey(name: 'previous_score') double? get previousScore; double get change; String get trend;@JsonKey(name: 'calculated_at') DateTime? get calculatedAt;
/// Create a copy of ReputationScore
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$ReputationScoreCopyWith<ReputationScore> get copyWith => _$ReputationScoreCopyWithImpl<ReputationScore>(this as ReputationScore, _$identity);

  /// Serializes this ReputationScore to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is ReputationScore&&(identical(other.currentScore, currentScore) || other.currentScore == currentScore)&&(identical(other.previousScore, previousScore) || other.previousScore == previousScore)&&(identical(other.change, change) || other.change == change)&&(identical(other.trend, trend) || other.trend == trend)&&(identical(other.calculatedAt, calculatedAt) || other.calculatedAt == calculatedAt));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,currentScore,previousScore,change,trend,calculatedAt);

@override
String toString() {
  return 'ReputationScore(currentScore: $currentScore, previousScore: $previousScore, change: $change, trend: $trend, calculatedAt: $calculatedAt)';
}


}

/// @nodoc
abstract mixin class $ReputationScoreCopyWith<$Res>  {
  factory $ReputationScoreCopyWith(ReputationScore value, $Res Function(ReputationScore) _then) = _$ReputationScoreCopyWithImpl;
@useResult
$Res call({
@JsonKey(name: 'current_score') double currentScore,@JsonKey(name: 'previous_score') double? previousScore, double change, String trend,@JsonKey(name: 'calculated_at') DateTime? calculatedAt
});




}
/// @nodoc
class _$ReputationScoreCopyWithImpl<$Res>
    implements $ReputationScoreCopyWith<$Res> {
  _$ReputationScoreCopyWithImpl(this._self, this._then);

  final ReputationScore _self;
  final $Res Function(ReputationScore) _then;

/// Create a copy of ReputationScore
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? currentScore = null,Object? previousScore = freezed,Object? change = null,Object? trend = null,Object? calculatedAt = freezed,}) {
  return _then(_self.copyWith(
currentScore: null == currentScore ? _self.currentScore : currentScore // ignore: cast_nullable_to_non_nullable
as double,previousScore: freezed == previousScore ? _self.previousScore : previousScore // ignore: cast_nullable_to_non_nullable
as double?,change: null == change ? _self.change : change // ignore: cast_nullable_to_non_nullable
as double,trend: null == trend ? _self.trend : trend // ignore: cast_nullable_to_non_nullable
as String,calculatedAt: freezed == calculatedAt ? _self.calculatedAt : calculatedAt // ignore: cast_nullable_to_non_nullable
as DateTime?,
  ));
}

}


/// Adds pattern-matching-related methods to [ReputationScore].
extension ReputationScorePatterns on ReputationScore {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _ReputationScore value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _ReputationScore() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _ReputationScore value)  $default,){
final _that = this;
switch (_that) {
case _ReputationScore():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _ReputationScore value)?  $default,){
final _that = this;
switch (_that) {
case _ReputationScore() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function(@JsonKey(name: 'current_score')  double currentScore, @JsonKey(name: 'previous_score')  double? previousScore,  double change,  String trend, @JsonKey(name: 'calculated_at')  DateTime? calculatedAt)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _ReputationScore() when $default != null:
return $default(_that.currentScore,_that.previousScore,_that.change,_that.trend,_that.calculatedAt);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function(@JsonKey(name: 'current_score')  double currentScore, @JsonKey(name: 'previous_score')  double? previousScore,  double change,  String trend, @JsonKey(name: 'calculated_at')  DateTime? calculatedAt)  $default,) {final _that = this;
switch (_that) {
case _ReputationScore():
return $default(_that.currentScore,_that.previousScore,_that.change,_that.trend,_that.calculatedAt);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function(@JsonKey(name: 'current_score')  double currentScore, @JsonKey(name: 'previous_score')  double? previousScore,  double change,  String trend, @JsonKey(name: 'calculated_at')  DateTime? calculatedAt)?  $default,) {final _that = this;
switch (_that) {
case _ReputationScore() when $default != null:
return $default(_that.currentScore,_that.previousScore,_that.change,_that.trend,_that.calculatedAt);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _ReputationScore implements ReputationScore {
  const _ReputationScore({@JsonKey(name: 'current_score') required this.currentScore, @JsonKey(name: 'previous_score') this.previousScore, this.change = 0.0, this.trend = 'stable', @JsonKey(name: 'calculated_at') this.calculatedAt});
  factory _ReputationScore.fromJson(Map<String, dynamic> json) => _$ReputationScoreFromJson(json);

@override@JsonKey(name: 'current_score') final  double currentScore;
@override@JsonKey(name: 'previous_score') final  double? previousScore;
@override@JsonKey() final  double change;
@override@JsonKey() final  String trend;
@override@JsonKey(name: 'calculated_at') final  DateTime? calculatedAt;

/// Create a copy of ReputationScore
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$ReputationScoreCopyWith<_ReputationScore> get copyWith => __$ReputationScoreCopyWithImpl<_ReputationScore>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$ReputationScoreToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _ReputationScore&&(identical(other.currentScore, currentScore) || other.currentScore == currentScore)&&(identical(other.previousScore, previousScore) || other.previousScore == previousScore)&&(identical(other.change, change) || other.change == change)&&(identical(other.trend, trend) || other.trend == trend)&&(identical(other.calculatedAt, calculatedAt) || other.calculatedAt == calculatedAt));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,currentScore,previousScore,change,trend,calculatedAt);

@override
String toString() {
  return 'ReputationScore(currentScore: $currentScore, previousScore: $previousScore, change: $change, trend: $trend, calculatedAt: $calculatedAt)';
}


}

/// @nodoc
abstract mixin class _$ReputationScoreCopyWith<$Res> implements $ReputationScoreCopyWith<$Res> {
  factory _$ReputationScoreCopyWith(_ReputationScore value, $Res Function(_ReputationScore) _then) = __$ReputationScoreCopyWithImpl;
@override @useResult
$Res call({
@JsonKey(name: 'current_score') double currentScore,@JsonKey(name: 'previous_score') double? previousScore, double change, String trend,@JsonKey(name: 'calculated_at') DateTime? calculatedAt
});




}
/// @nodoc
class __$ReputationScoreCopyWithImpl<$Res>
    implements _$ReputationScoreCopyWith<$Res> {
  __$ReputationScoreCopyWithImpl(this._self, this._then);

  final _ReputationScore _self;
  final $Res Function(_ReputationScore) _then;

/// Create a copy of ReputationScore
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? currentScore = null,Object? previousScore = freezed,Object? change = null,Object? trend = null,Object? calculatedAt = freezed,}) {
  return _then(_ReputationScore(
currentScore: null == currentScore ? _self.currentScore : currentScore // ignore: cast_nullable_to_non_nullable
as double,previousScore: freezed == previousScore ? _self.previousScore : previousScore // ignore: cast_nullable_to_non_nullable
as double?,change: null == change ? _self.change : change // ignore: cast_nullable_to_non_nullable
as double,trend: null == trend ? _self.trend : trend // ignore: cast_nullable_to_non_nullable
as String,calculatedAt: freezed == calculatedAt ? _self.calculatedAt : calculatedAt // ignore: cast_nullable_to_non_nullable
as DateTime?,
  ));
}


}

// dart format on
