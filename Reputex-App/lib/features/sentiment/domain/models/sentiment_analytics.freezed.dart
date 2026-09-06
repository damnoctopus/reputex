// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'sentiment_analytics.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$SentimentAnalytics {

 SentimentDistribution get distribution; List<SentimentTrend> get trends;@JsonKey(name: 'platform_breakdown') List<PlatformStatistics> get platformBreakdown;@JsonKey(name: 'overall_score') double get overallScore;@JsonKey(name: 'total_reviews_analyzed') int get totalReviewsAnalyzed;
/// Create a copy of SentimentAnalytics
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$SentimentAnalyticsCopyWith<SentimentAnalytics> get copyWith => _$SentimentAnalyticsCopyWithImpl<SentimentAnalytics>(this as SentimentAnalytics, _$identity);

  /// Serializes this SentimentAnalytics to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is SentimentAnalytics&&(identical(other.distribution, distribution) || other.distribution == distribution)&&const DeepCollectionEquality().equals(other.trends, trends)&&const DeepCollectionEquality().equals(other.platformBreakdown, platformBreakdown)&&(identical(other.overallScore, overallScore) || other.overallScore == overallScore)&&(identical(other.totalReviewsAnalyzed, totalReviewsAnalyzed) || other.totalReviewsAnalyzed == totalReviewsAnalyzed));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,distribution,const DeepCollectionEquality().hash(trends),const DeepCollectionEquality().hash(platformBreakdown),overallScore,totalReviewsAnalyzed);

@override
String toString() {
  return 'SentimentAnalytics(distribution: $distribution, trends: $trends, platformBreakdown: $platformBreakdown, overallScore: $overallScore, totalReviewsAnalyzed: $totalReviewsAnalyzed)';
}


}

/// @nodoc
abstract mixin class $SentimentAnalyticsCopyWith<$Res>  {
  factory $SentimentAnalyticsCopyWith(SentimentAnalytics value, $Res Function(SentimentAnalytics) _then) = _$SentimentAnalyticsCopyWithImpl;
@useResult
$Res call({
 SentimentDistribution distribution, List<SentimentTrend> trends,@JsonKey(name: 'platform_breakdown') List<PlatformStatistics> platformBreakdown,@JsonKey(name: 'overall_score') double overallScore,@JsonKey(name: 'total_reviews_analyzed') int totalReviewsAnalyzed
});


$SentimentDistributionCopyWith<$Res> get distribution;

}
/// @nodoc
class _$SentimentAnalyticsCopyWithImpl<$Res>
    implements $SentimentAnalyticsCopyWith<$Res> {
  _$SentimentAnalyticsCopyWithImpl(this._self, this._then);

  final SentimentAnalytics _self;
  final $Res Function(SentimentAnalytics) _then;

/// Create a copy of SentimentAnalytics
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? distribution = null,Object? trends = null,Object? platformBreakdown = null,Object? overallScore = null,Object? totalReviewsAnalyzed = null,}) {
  return _then(_self.copyWith(
distribution: null == distribution ? _self.distribution : distribution // ignore: cast_nullable_to_non_nullable
as SentimentDistribution,trends: null == trends ? _self.trends : trends // ignore: cast_nullable_to_non_nullable
as List<SentimentTrend>,platformBreakdown: null == platformBreakdown ? _self.platformBreakdown : platformBreakdown // ignore: cast_nullable_to_non_nullable
as List<PlatformStatistics>,overallScore: null == overallScore ? _self.overallScore : overallScore // ignore: cast_nullable_to_non_nullable
as double,totalReviewsAnalyzed: null == totalReviewsAnalyzed ? _self.totalReviewsAnalyzed : totalReviewsAnalyzed // ignore: cast_nullable_to_non_nullable
as int,
  ));
}
/// Create a copy of SentimentAnalytics
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$SentimentDistributionCopyWith<$Res> get distribution {
  
  return $SentimentDistributionCopyWith<$Res>(_self.distribution, (value) {
    return _then(_self.copyWith(distribution: value));
  });
}
}


/// Adds pattern-matching-related methods to [SentimentAnalytics].
extension SentimentAnalyticsPatterns on SentimentAnalytics {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _SentimentAnalytics value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _SentimentAnalytics() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _SentimentAnalytics value)  $default,){
final _that = this;
switch (_that) {
case _SentimentAnalytics():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _SentimentAnalytics value)?  $default,){
final _that = this;
switch (_that) {
case _SentimentAnalytics() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( SentimentDistribution distribution,  List<SentimentTrend> trends, @JsonKey(name: 'platform_breakdown')  List<PlatformStatistics> platformBreakdown, @JsonKey(name: 'overall_score')  double overallScore, @JsonKey(name: 'total_reviews_analyzed')  int totalReviewsAnalyzed)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _SentimentAnalytics() when $default != null:
return $default(_that.distribution,_that.trends,_that.platformBreakdown,_that.overallScore,_that.totalReviewsAnalyzed);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( SentimentDistribution distribution,  List<SentimentTrend> trends, @JsonKey(name: 'platform_breakdown')  List<PlatformStatistics> platformBreakdown, @JsonKey(name: 'overall_score')  double overallScore, @JsonKey(name: 'total_reviews_analyzed')  int totalReviewsAnalyzed)  $default,) {final _that = this;
switch (_that) {
case _SentimentAnalytics():
return $default(_that.distribution,_that.trends,_that.platformBreakdown,_that.overallScore,_that.totalReviewsAnalyzed);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( SentimentDistribution distribution,  List<SentimentTrend> trends, @JsonKey(name: 'platform_breakdown')  List<PlatformStatistics> platformBreakdown, @JsonKey(name: 'overall_score')  double overallScore, @JsonKey(name: 'total_reviews_analyzed')  int totalReviewsAnalyzed)?  $default,) {final _that = this;
switch (_that) {
case _SentimentAnalytics() when $default != null:
return $default(_that.distribution,_that.trends,_that.platformBreakdown,_that.overallScore,_that.totalReviewsAnalyzed);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _SentimentAnalytics implements SentimentAnalytics {
  const _SentimentAnalytics({required this.distribution, this.trends = const [], @JsonKey(name: 'platform_breakdown') this.platformBreakdown = const [], @JsonKey(name: 'overall_score') this.overallScore = 0.0, @JsonKey(name: 'total_reviews_analyzed') this.totalReviewsAnalyzed = 0});
  factory _SentimentAnalytics.fromJson(Map<String, dynamic> json) => _$SentimentAnalyticsFromJson(json);

@override final  SentimentDistribution distribution;
@override@JsonKey() final  List<SentimentTrend> trends;
@override@JsonKey(name: 'platform_breakdown') final  List<PlatformStatistics> platformBreakdown;
@override@JsonKey(name: 'overall_score') final  double overallScore;
@override@JsonKey(name: 'total_reviews_analyzed') final  int totalReviewsAnalyzed;

/// Create a copy of SentimentAnalytics
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$SentimentAnalyticsCopyWith<_SentimentAnalytics> get copyWith => __$SentimentAnalyticsCopyWithImpl<_SentimentAnalytics>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$SentimentAnalyticsToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _SentimentAnalytics&&(identical(other.distribution, distribution) || other.distribution == distribution)&&const DeepCollectionEquality().equals(other.trends, trends)&&const DeepCollectionEquality().equals(other.platformBreakdown, platformBreakdown)&&(identical(other.overallScore, overallScore) || other.overallScore == overallScore)&&(identical(other.totalReviewsAnalyzed, totalReviewsAnalyzed) || other.totalReviewsAnalyzed == totalReviewsAnalyzed));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,distribution,const DeepCollectionEquality().hash(trends),const DeepCollectionEquality().hash(platformBreakdown),overallScore,totalReviewsAnalyzed);

@override
String toString() {
  return 'SentimentAnalytics(distribution: $distribution, trends: $trends, platformBreakdown: $platformBreakdown, overallScore: $overallScore, totalReviewsAnalyzed: $totalReviewsAnalyzed)';
}


}

/// @nodoc
abstract mixin class _$SentimentAnalyticsCopyWith<$Res> implements $SentimentAnalyticsCopyWith<$Res> {
  factory _$SentimentAnalyticsCopyWith(_SentimentAnalytics value, $Res Function(_SentimentAnalytics) _then) = __$SentimentAnalyticsCopyWithImpl;
@override @useResult
$Res call({
 SentimentDistribution distribution, List<SentimentTrend> trends,@JsonKey(name: 'platform_breakdown') List<PlatformStatistics> platformBreakdown,@JsonKey(name: 'overall_score') double overallScore,@JsonKey(name: 'total_reviews_analyzed') int totalReviewsAnalyzed
});


@override $SentimentDistributionCopyWith<$Res> get distribution;

}
/// @nodoc
class __$SentimentAnalyticsCopyWithImpl<$Res>
    implements _$SentimentAnalyticsCopyWith<$Res> {
  __$SentimentAnalyticsCopyWithImpl(this._self, this._then);

  final _SentimentAnalytics _self;
  final $Res Function(_SentimentAnalytics) _then;

/// Create a copy of SentimentAnalytics
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? distribution = null,Object? trends = null,Object? platformBreakdown = null,Object? overallScore = null,Object? totalReviewsAnalyzed = null,}) {
  return _then(_SentimentAnalytics(
distribution: null == distribution ? _self.distribution : distribution // ignore: cast_nullable_to_non_nullable
as SentimentDistribution,trends: null == trends ? _self.trends : trends // ignore: cast_nullable_to_non_nullable
as List<SentimentTrend>,platformBreakdown: null == platformBreakdown ? _self.platformBreakdown : platformBreakdown // ignore: cast_nullable_to_non_nullable
as List<PlatformStatistics>,overallScore: null == overallScore ? _self.overallScore : overallScore // ignore: cast_nullable_to_non_nullable
as double,totalReviewsAnalyzed: null == totalReviewsAnalyzed ? _self.totalReviewsAnalyzed : totalReviewsAnalyzed // ignore: cast_nullable_to_non_nullable
as int,
  ));
}

/// Create a copy of SentimentAnalytics
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$SentimentDistributionCopyWith<$Res> get distribution {
  
  return $SentimentDistributionCopyWith<$Res>(_self.distribution, (value) {
    return _then(_self.copyWith(distribution: value));
  });
}
}

// dart format on
