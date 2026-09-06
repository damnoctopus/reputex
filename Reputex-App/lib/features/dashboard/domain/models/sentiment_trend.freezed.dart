// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'sentiment_trend.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$SentimentTrend {

 String get date; int get positive; int get neutral; int get negative; double get score;
/// Create a copy of SentimentTrend
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$SentimentTrendCopyWith<SentimentTrend> get copyWith => _$SentimentTrendCopyWithImpl<SentimentTrend>(this as SentimentTrend, _$identity);

  /// Serializes this SentimentTrend to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is SentimentTrend&&(identical(other.date, date) || other.date == date)&&(identical(other.positive, positive) || other.positive == positive)&&(identical(other.neutral, neutral) || other.neutral == neutral)&&(identical(other.negative, negative) || other.negative == negative)&&(identical(other.score, score) || other.score == score));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,date,positive,neutral,negative,score);

@override
String toString() {
  return 'SentimentTrend(date: $date, positive: $positive, neutral: $neutral, negative: $negative, score: $score)';
}


}

/// @nodoc
abstract mixin class $SentimentTrendCopyWith<$Res>  {
  factory $SentimentTrendCopyWith(SentimentTrend value, $Res Function(SentimentTrend) _then) = _$SentimentTrendCopyWithImpl;
@useResult
$Res call({
 String date, int positive, int neutral, int negative, double score
});




}
/// @nodoc
class _$SentimentTrendCopyWithImpl<$Res>
    implements $SentimentTrendCopyWith<$Res> {
  _$SentimentTrendCopyWithImpl(this._self, this._then);

  final SentimentTrend _self;
  final $Res Function(SentimentTrend) _then;

/// Create a copy of SentimentTrend
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? date = null,Object? positive = null,Object? neutral = null,Object? negative = null,Object? score = null,}) {
  return _then(_self.copyWith(
date: null == date ? _self.date : date // ignore: cast_nullable_to_non_nullable
as String,positive: null == positive ? _self.positive : positive // ignore: cast_nullable_to_non_nullable
as int,neutral: null == neutral ? _self.neutral : neutral // ignore: cast_nullable_to_non_nullable
as int,negative: null == negative ? _self.negative : negative // ignore: cast_nullable_to_non_nullable
as int,score: null == score ? _self.score : score // ignore: cast_nullable_to_non_nullable
as double,
  ));
}

}


/// Adds pattern-matching-related methods to [SentimentTrend].
extension SentimentTrendPatterns on SentimentTrend {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _SentimentTrend value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _SentimentTrend() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _SentimentTrend value)  $default,){
final _that = this;
switch (_that) {
case _SentimentTrend():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _SentimentTrend value)?  $default,){
final _that = this;
switch (_that) {
case _SentimentTrend() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String date,  int positive,  int neutral,  int negative,  double score)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _SentimentTrend() when $default != null:
return $default(_that.date,_that.positive,_that.neutral,_that.negative,_that.score);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String date,  int positive,  int neutral,  int negative,  double score)  $default,) {final _that = this;
switch (_that) {
case _SentimentTrend():
return $default(_that.date,_that.positive,_that.neutral,_that.negative,_that.score);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String date,  int positive,  int neutral,  int negative,  double score)?  $default,) {final _that = this;
switch (_that) {
case _SentimentTrend() when $default != null:
return $default(_that.date,_that.positive,_that.neutral,_that.negative,_that.score);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _SentimentTrend implements SentimentTrend {
  const _SentimentTrend({required this.date, this.positive = 0, this.neutral = 0, this.negative = 0, this.score = 0.0});
  factory _SentimentTrend.fromJson(Map<String, dynamic> json) => _$SentimentTrendFromJson(json);

@override final  String date;
@override@JsonKey() final  int positive;
@override@JsonKey() final  int neutral;
@override@JsonKey() final  int negative;
@override@JsonKey() final  double score;

/// Create a copy of SentimentTrend
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$SentimentTrendCopyWith<_SentimentTrend> get copyWith => __$SentimentTrendCopyWithImpl<_SentimentTrend>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$SentimentTrendToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _SentimentTrend&&(identical(other.date, date) || other.date == date)&&(identical(other.positive, positive) || other.positive == positive)&&(identical(other.neutral, neutral) || other.neutral == neutral)&&(identical(other.negative, negative) || other.negative == negative)&&(identical(other.score, score) || other.score == score));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,date,positive,neutral,negative,score);

@override
String toString() {
  return 'SentimentTrend(date: $date, positive: $positive, neutral: $neutral, negative: $negative, score: $score)';
}


}

/// @nodoc
abstract mixin class _$SentimentTrendCopyWith<$Res> implements $SentimentTrendCopyWith<$Res> {
  factory _$SentimentTrendCopyWith(_SentimentTrend value, $Res Function(_SentimentTrend) _then) = __$SentimentTrendCopyWithImpl;
@override @useResult
$Res call({
 String date, int positive, int neutral, int negative, double score
});




}
/// @nodoc
class __$SentimentTrendCopyWithImpl<$Res>
    implements _$SentimentTrendCopyWith<$Res> {
  __$SentimentTrendCopyWithImpl(this._self, this._then);

  final _SentimentTrend _self;
  final $Res Function(_SentimentTrend) _then;

/// Create a copy of SentimentTrend
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? date = null,Object? positive = null,Object? neutral = null,Object? negative = null,Object? score = null,}) {
  return _then(_SentimentTrend(
date: null == date ? _self.date : date // ignore: cast_nullable_to_non_nullable
as String,positive: null == positive ? _self.positive : positive // ignore: cast_nullable_to_non_nullable
as int,neutral: null == neutral ? _self.neutral : neutral // ignore: cast_nullable_to_non_nullable
as int,negative: null == negative ? _self.negative : negative // ignore: cast_nullable_to_non_nullable
as int,score: null == score ? _self.score : score // ignore: cast_nullable_to_non_nullable
as double,
  ));
}


}

// dart format on
