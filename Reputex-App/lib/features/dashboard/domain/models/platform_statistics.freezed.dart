// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'platform_statistics.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$PlatformStatistics {

 String get platform; int get count;@JsonKey(name: 'positive_percentage') double get positivePercentage;@JsonKey(name: 'negative_percentage') double get negativePercentage;@JsonKey(name: 'neutral_percentage') double get neutralPercentage;@JsonKey(name: 'average_rating') double? get averageRating;
/// Create a copy of PlatformStatistics
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$PlatformStatisticsCopyWith<PlatformStatistics> get copyWith => _$PlatformStatisticsCopyWithImpl<PlatformStatistics>(this as PlatformStatistics, _$identity);

  /// Serializes this PlatformStatistics to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is PlatformStatistics&&(identical(other.platform, platform) || other.platform == platform)&&(identical(other.count, count) || other.count == count)&&(identical(other.positivePercentage, positivePercentage) || other.positivePercentage == positivePercentage)&&(identical(other.negativePercentage, negativePercentage) || other.negativePercentage == negativePercentage)&&(identical(other.neutralPercentage, neutralPercentage) || other.neutralPercentage == neutralPercentage)&&(identical(other.averageRating, averageRating) || other.averageRating == averageRating));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,platform,count,positivePercentage,negativePercentage,neutralPercentage,averageRating);

@override
String toString() {
  return 'PlatformStatistics(platform: $platform, count: $count, positivePercentage: $positivePercentage, negativePercentage: $negativePercentage, neutralPercentage: $neutralPercentage, averageRating: $averageRating)';
}


}

/// @nodoc
abstract mixin class $PlatformStatisticsCopyWith<$Res>  {
  factory $PlatformStatisticsCopyWith(PlatformStatistics value, $Res Function(PlatformStatistics) _then) = _$PlatformStatisticsCopyWithImpl;
@useResult
$Res call({
 String platform, int count,@JsonKey(name: 'positive_percentage') double positivePercentage,@JsonKey(name: 'negative_percentage') double negativePercentage,@JsonKey(name: 'neutral_percentage') double neutralPercentage,@JsonKey(name: 'average_rating') double? averageRating
});




}
/// @nodoc
class _$PlatformStatisticsCopyWithImpl<$Res>
    implements $PlatformStatisticsCopyWith<$Res> {
  _$PlatformStatisticsCopyWithImpl(this._self, this._then);

  final PlatformStatistics _self;
  final $Res Function(PlatformStatistics) _then;

/// Create a copy of PlatformStatistics
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? platform = null,Object? count = null,Object? positivePercentage = null,Object? negativePercentage = null,Object? neutralPercentage = null,Object? averageRating = freezed,}) {
  return _then(_self.copyWith(
platform: null == platform ? _self.platform : platform // ignore: cast_nullable_to_non_nullable
as String,count: null == count ? _self.count : count // ignore: cast_nullable_to_non_nullable
as int,positivePercentage: null == positivePercentage ? _self.positivePercentage : positivePercentage // ignore: cast_nullable_to_non_nullable
as double,negativePercentage: null == negativePercentage ? _self.negativePercentage : negativePercentage // ignore: cast_nullable_to_non_nullable
as double,neutralPercentage: null == neutralPercentage ? _self.neutralPercentage : neutralPercentage // ignore: cast_nullable_to_non_nullable
as double,averageRating: freezed == averageRating ? _self.averageRating : averageRating // ignore: cast_nullable_to_non_nullable
as double?,
  ));
}

}


/// Adds pattern-matching-related methods to [PlatformStatistics].
extension PlatformStatisticsPatterns on PlatformStatistics {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _PlatformStatistics value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _PlatformStatistics() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _PlatformStatistics value)  $default,){
final _that = this;
switch (_that) {
case _PlatformStatistics():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _PlatformStatistics value)?  $default,){
final _that = this;
switch (_that) {
case _PlatformStatistics() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String platform,  int count, @JsonKey(name: 'positive_percentage')  double positivePercentage, @JsonKey(name: 'negative_percentage')  double negativePercentage, @JsonKey(name: 'neutral_percentage')  double neutralPercentage, @JsonKey(name: 'average_rating')  double? averageRating)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _PlatformStatistics() when $default != null:
return $default(_that.platform,_that.count,_that.positivePercentage,_that.negativePercentage,_that.neutralPercentage,_that.averageRating);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String platform,  int count, @JsonKey(name: 'positive_percentage')  double positivePercentage, @JsonKey(name: 'negative_percentage')  double negativePercentage, @JsonKey(name: 'neutral_percentage')  double neutralPercentage, @JsonKey(name: 'average_rating')  double? averageRating)  $default,) {final _that = this;
switch (_that) {
case _PlatformStatistics():
return $default(_that.platform,_that.count,_that.positivePercentage,_that.negativePercentage,_that.neutralPercentage,_that.averageRating);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String platform,  int count, @JsonKey(name: 'positive_percentage')  double positivePercentage, @JsonKey(name: 'negative_percentage')  double negativePercentage, @JsonKey(name: 'neutral_percentage')  double neutralPercentage, @JsonKey(name: 'average_rating')  double? averageRating)?  $default,) {final _that = this;
switch (_that) {
case _PlatformStatistics() when $default != null:
return $default(_that.platform,_that.count,_that.positivePercentage,_that.negativePercentage,_that.neutralPercentage,_that.averageRating);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _PlatformStatistics implements PlatformStatistics {
  const _PlatformStatistics({required this.platform, this.count = 0, @JsonKey(name: 'positive_percentage') this.positivePercentage = 0.0, @JsonKey(name: 'negative_percentage') this.negativePercentage = 0.0, @JsonKey(name: 'neutral_percentage') this.neutralPercentage = 0.0, @JsonKey(name: 'average_rating') this.averageRating});
  factory _PlatformStatistics.fromJson(Map<String, dynamic> json) => _$PlatformStatisticsFromJson(json);

@override final  String platform;
@override@JsonKey() final  int count;
@override@JsonKey(name: 'positive_percentage') final  double positivePercentage;
@override@JsonKey(name: 'negative_percentage') final  double negativePercentage;
@override@JsonKey(name: 'neutral_percentage') final  double neutralPercentage;
@override@JsonKey(name: 'average_rating') final  double? averageRating;

/// Create a copy of PlatformStatistics
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$PlatformStatisticsCopyWith<_PlatformStatistics> get copyWith => __$PlatformStatisticsCopyWithImpl<_PlatformStatistics>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$PlatformStatisticsToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _PlatformStatistics&&(identical(other.platform, platform) || other.platform == platform)&&(identical(other.count, count) || other.count == count)&&(identical(other.positivePercentage, positivePercentage) || other.positivePercentage == positivePercentage)&&(identical(other.negativePercentage, negativePercentage) || other.negativePercentage == negativePercentage)&&(identical(other.neutralPercentage, neutralPercentage) || other.neutralPercentage == neutralPercentage)&&(identical(other.averageRating, averageRating) || other.averageRating == averageRating));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,platform,count,positivePercentage,negativePercentage,neutralPercentage,averageRating);

@override
String toString() {
  return 'PlatformStatistics(platform: $platform, count: $count, positivePercentage: $positivePercentage, negativePercentage: $negativePercentage, neutralPercentage: $neutralPercentage, averageRating: $averageRating)';
}


}

/// @nodoc
abstract mixin class _$PlatformStatisticsCopyWith<$Res> implements $PlatformStatisticsCopyWith<$Res> {
  factory _$PlatformStatisticsCopyWith(_PlatformStatistics value, $Res Function(_PlatformStatistics) _then) = __$PlatformStatisticsCopyWithImpl;
@override @useResult
$Res call({
 String platform, int count,@JsonKey(name: 'positive_percentage') double positivePercentage,@JsonKey(name: 'negative_percentage') double negativePercentage,@JsonKey(name: 'neutral_percentage') double neutralPercentage,@JsonKey(name: 'average_rating') double? averageRating
});




}
/// @nodoc
class __$PlatformStatisticsCopyWithImpl<$Res>
    implements _$PlatformStatisticsCopyWith<$Res> {
  __$PlatformStatisticsCopyWithImpl(this._self, this._then);

  final _PlatformStatistics _self;
  final $Res Function(_PlatformStatistics) _then;

/// Create a copy of PlatformStatistics
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? platform = null,Object? count = null,Object? positivePercentage = null,Object? negativePercentage = null,Object? neutralPercentage = null,Object? averageRating = freezed,}) {
  return _then(_PlatformStatistics(
platform: null == platform ? _self.platform : platform // ignore: cast_nullable_to_non_nullable
as String,count: null == count ? _self.count : count // ignore: cast_nullable_to_non_nullable
as int,positivePercentage: null == positivePercentage ? _self.positivePercentage : positivePercentage // ignore: cast_nullable_to_non_nullable
as double,negativePercentage: null == negativePercentage ? _self.negativePercentage : negativePercentage // ignore: cast_nullable_to_non_nullable
as double,neutralPercentage: null == neutralPercentage ? _self.neutralPercentage : neutralPercentage // ignore: cast_nullable_to_non_nullable
as double,averageRating: freezed == averageRating ? _self.averageRating : averageRating // ignore: cast_nullable_to_non_nullable
as double?,
  ));
}


}

// dart format on
