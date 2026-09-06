// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'sentiment_distribution.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$SentimentDistribution {

 int get positive; int get neutral; int get negative; int get total;@JsonKey(name: 'positive_percentage') double get positivePercentage;@JsonKey(name: 'neutral_percentage') double get neutralPercentage;@JsonKey(name: 'negative_percentage') double get negativePercentage;
/// Create a copy of SentimentDistribution
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$SentimentDistributionCopyWith<SentimentDistribution> get copyWith => _$SentimentDistributionCopyWithImpl<SentimentDistribution>(this as SentimentDistribution, _$identity);

  /// Serializes this SentimentDistribution to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is SentimentDistribution&&(identical(other.positive, positive) || other.positive == positive)&&(identical(other.neutral, neutral) || other.neutral == neutral)&&(identical(other.negative, negative) || other.negative == negative)&&(identical(other.total, total) || other.total == total)&&(identical(other.positivePercentage, positivePercentage) || other.positivePercentage == positivePercentage)&&(identical(other.neutralPercentage, neutralPercentage) || other.neutralPercentage == neutralPercentage)&&(identical(other.negativePercentage, negativePercentage) || other.negativePercentage == negativePercentage));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,positive,neutral,negative,total,positivePercentage,neutralPercentage,negativePercentage);

@override
String toString() {
  return 'SentimentDistribution(positive: $positive, neutral: $neutral, negative: $negative, total: $total, positivePercentage: $positivePercentage, neutralPercentage: $neutralPercentage, negativePercentage: $negativePercentage)';
}


}

/// @nodoc
abstract mixin class $SentimentDistributionCopyWith<$Res>  {
  factory $SentimentDistributionCopyWith(SentimentDistribution value, $Res Function(SentimentDistribution) _then) = _$SentimentDistributionCopyWithImpl;
@useResult
$Res call({
 int positive, int neutral, int negative, int total,@JsonKey(name: 'positive_percentage') double positivePercentage,@JsonKey(name: 'neutral_percentage') double neutralPercentage,@JsonKey(name: 'negative_percentage') double negativePercentage
});




}
/// @nodoc
class _$SentimentDistributionCopyWithImpl<$Res>
    implements $SentimentDistributionCopyWith<$Res> {
  _$SentimentDistributionCopyWithImpl(this._self, this._then);

  final SentimentDistribution _self;
  final $Res Function(SentimentDistribution) _then;

/// Create a copy of SentimentDistribution
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? positive = null,Object? neutral = null,Object? negative = null,Object? total = null,Object? positivePercentage = null,Object? neutralPercentage = null,Object? negativePercentage = null,}) {
  return _then(_self.copyWith(
positive: null == positive ? _self.positive : positive // ignore: cast_nullable_to_non_nullable
as int,neutral: null == neutral ? _self.neutral : neutral // ignore: cast_nullable_to_non_nullable
as int,negative: null == negative ? _self.negative : negative // ignore: cast_nullable_to_non_nullable
as int,total: null == total ? _self.total : total // ignore: cast_nullable_to_non_nullable
as int,positivePercentage: null == positivePercentage ? _self.positivePercentage : positivePercentage // ignore: cast_nullable_to_non_nullable
as double,neutralPercentage: null == neutralPercentage ? _self.neutralPercentage : neutralPercentage // ignore: cast_nullable_to_non_nullable
as double,negativePercentage: null == negativePercentage ? _self.negativePercentage : negativePercentage // ignore: cast_nullable_to_non_nullable
as double,
  ));
}

}


/// Adds pattern-matching-related methods to [SentimentDistribution].
extension SentimentDistributionPatterns on SentimentDistribution {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _SentimentDistribution value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _SentimentDistribution() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _SentimentDistribution value)  $default,){
final _that = this;
switch (_that) {
case _SentimentDistribution():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _SentimentDistribution value)?  $default,){
final _that = this;
switch (_that) {
case _SentimentDistribution() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( int positive,  int neutral,  int negative,  int total, @JsonKey(name: 'positive_percentage')  double positivePercentage, @JsonKey(name: 'neutral_percentage')  double neutralPercentage, @JsonKey(name: 'negative_percentage')  double negativePercentage)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _SentimentDistribution() when $default != null:
return $default(_that.positive,_that.neutral,_that.negative,_that.total,_that.positivePercentage,_that.neutralPercentage,_that.negativePercentage);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( int positive,  int neutral,  int negative,  int total, @JsonKey(name: 'positive_percentage')  double positivePercentage, @JsonKey(name: 'neutral_percentage')  double neutralPercentage, @JsonKey(name: 'negative_percentage')  double negativePercentage)  $default,) {final _that = this;
switch (_that) {
case _SentimentDistribution():
return $default(_that.positive,_that.neutral,_that.negative,_that.total,_that.positivePercentage,_that.neutralPercentage,_that.negativePercentage);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( int positive,  int neutral,  int negative,  int total, @JsonKey(name: 'positive_percentage')  double positivePercentage, @JsonKey(name: 'neutral_percentage')  double neutralPercentage, @JsonKey(name: 'negative_percentage')  double negativePercentage)?  $default,) {final _that = this;
switch (_that) {
case _SentimentDistribution() when $default != null:
return $default(_that.positive,_that.neutral,_that.negative,_that.total,_that.positivePercentage,_that.neutralPercentage,_that.negativePercentage);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _SentimentDistribution implements SentimentDistribution {
  const _SentimentDistribution({this.positive = 0, this.neutral = 0, this.negative = 0, this.total = 0, @JsonKey(name: 'positive_percentage') this.positivePercentage = 0.0, @JsonKey(name: 'neutral_percentage') this.neutralPercentage = 0.0, @JsonKey(name: 'negative_percentage') this.negativePercentage = 0.0});
  factory _SentimentDistribution.fromJson(Map<String, dynamic> json) => _$SentimentDistributionFromJson(json);

@override@JsonKey() final  int positive;
@override@JsonKey() final  int neutral;
@override@JsonKey() final  int negative;
@override@JsonKey() final  int total;
@override@JsonKey(name: 'positive_percentage') final  double positivePercentage;
@override@JsonKey(name: 'neutral_percentage') final  double neutralPercentage;
@override@JsonKey(name: 'negative_percentage') final  double negativePercentage;

/// Create a copy of SentimentDistribution
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$SentimentDistributionCopyWith<_SentimentDistribution> get copyWith => __$SentimentDistributionCopyWithImpl<_SentimentDistribution>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$SentimentDistributionToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _SentimentDistribution&&(identical(other.positive, positive) || other.positive == positive)&&(identical(other.neutral, neutral) || other.neutral == neutral)&&(identical(other.negative, negative) || other.negative == negative)&&(identical(other.total, total) || other.total == total)&&(identical(other.positivePercentage, positivePercentage) || other.positivePercentage == positivePercentage)&&(identical(other.neutralPercentage, neutralPercentage) || other.neutralPercentage == neutralPercentage)&&(identical(other.negativePercentage, negativePercentage) || other.negativePercentage == negativePercentage));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,positive,neutral,negative,total,positivePercentage,neutralPercentage,negativePercentage);

@override
String toString() {
  return 'SentimentDistribution(positive: $positive, neutral: $neutral, negative: $negative, total: $total, positivePercentage: $positivePercentage, neutralPercentage: $neutralPercentage, negativePercentage: $negativePercentage)';
}


}

/// @nodoc
abstract mixin class _$SentimentDistributionCopyWith<$Res> implements $SentimentDistributionCopyWith<$Res> {
  factory _$SentimentDistributionCopyWith(_SentimentDistribution value, $Res Function(_SentimentDistribution) _then) = __$SentimentDistributionCopyWithImpl;
@override @useResult
$Res call({
 int positive, int neutral, int negative, int total,@JsonKey(name: 'positive_percentage') double positivePercentage,@JsonKey(name: 'neutral_percentage') double neutralPercentage,@JsonKey(name: 'negative_percentage') double negativePercentage
});




}
/// @nodoc
class __$SentimentDistributionCopyWithImpl<$Res>
    implements _$SentimentDistributionCopyWith<$Res> {
  __$SentimentDistributionCopyWithImpl(this._self, this._then);

  final _SentimentDistribution _self;
  final $Res Function(_SentimentDistribution) _then;

/// Create a copy of SentimentDistribution
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? positive = null,Object? neutral = null,Object? negative = null,Object? total = null,Object? positivePercentage = null,Object? neutralPercentage = null,Object? negativePercentage = null,}) {
  return _then(_SentimentDistribution(
positive: null == positive ? _self.positive : positive // ignore: cast_nullable_to_non_nullable
as int,neutral: null == neutral ? _self.neutral : neutral // ignore: cast_nullable_to_non_nullable
as int,negative: null == negative ? _self.negative : negative // ignore: cast_nullable_to_non_nullable
as int,total: null == total ? _self.total : total // ignore: cast_nullable_to_non_nullable
as int,positivePercentage: null == positivePercentage ? _self.positivePercentage : positivePercentage // ignore: cast_nullable_to_non_nullable
as double,neutralPercentage: null == neutralPercentage ? _self.neutralPercentage : neutralPercentage // ignore: cast_nullable_to_non_nullable
as double,negativePercentage: null == negativePercentage ? _self.negativePercentage : negativePercentage // ignore: cast_nullable_to_non_nullable
as double,
  ));
}


}

// dart format on
