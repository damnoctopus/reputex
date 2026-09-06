// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'dashboard_summary.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$DashboardSummary {

@JsonKey(name: 'reputation_score') ReputationScore get reputationScore;@JsonKey(name: 'sentiment_distribution') SentimentDistribution get sentimentDistribution;@JsonKey(name: 'total_mentions') int get totalMentions;@JsonKey(name: 'crisis_active') bool get crisisActive;@JsonKey(name: 'crisis_count') int get crisisCount;@JsonKey(name: 'pending_responses_count') int get pendingResponsesCount;@JsonKey(name: 'fraud_alerts_count') int get fraudAlertsCount;@JsonKey(name: 'crisis_risk_level') String get crisisRiskLevel;@JsonKey(name: 'suspicious_reviews_count') int get suspiciousReviewsCount;@JsonKey(name: 'active_clusters_count') int get activeClustersCount;@JsonKey(name: 'top_issues') List<Map<String, dynamic>> get topIssues;@JsonKey(name: 'recent_mentions') List<Mention> get recentMentions;
/// Create a copy of DashboardSummary
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$DashboardSummaryCopyWith<DashboardSummary> get copyWith => _$DashboardSummaryCopyWithImpl<DashboardSummary>(this as DashboardSummary, _$identity);

  /// Serializes this DashboardSummary to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is DashboardSummary&&(identical(other.reputationScore, reputationScore) || other.reputationScore == reputationScore)&&(identical(other.sentimentDistribution, sentimentDistribution) || other.sentimentDistribution == sentimentDistribution)&&(identical(other.totalMentions, totalMentions) || other.totalMentions == totalMentions)&&(identical(other.crisisActive, crisisActive) || other.crisisActive == crisisActive)&&(identical(other.crisisCount, crisisCount) || other.crisisCount == crisisCount)&&(identical(other.pendingResponsesCount, pendingResponsesCount) || other.pendingResponsesCount == pendingResponsesCount)&&(identical(other.fraudAlertsCount, fraudAlertsCount) || other.fraudAlertsCount == fraudAlertsCount)&&(identical(other.crisisRiskLevel, crisisRiskLevel) || other.crisisRiskLevel == crisisRiskLevel)&&(identical(other.suspiciousReviewsCount, suspiciousReviewsCount) || other.suspiciousReviewsCount == suspiciousReviewsCount)&&(identical(other.activeClustersCount, activeClustersCount) || other.activeClustersCount == activeClustersCount)&&const DeepCollectionEquality().equals(other.topIssues, topIssues)&&const DeepCollectionEquality().equals(other.recentMentions, recentMentions));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,reputationScore,sentimentDistribution,totalMentions,crisisActive,crisisCount,pendingResponsesCount,fraudAlertsCount,crisisRiskLevel,suspiciousReviewsCount,activeClustersCount,const DeepCollectionEquality().hash(topIssues),const DeepCollectionEquality().hash(recentMentions));

@override
String toString() {
  return 'DashboardSummary(reputationScore: $reputationScore, sentimentDistribution: $sentimentDistribution, totalMentions: $totalMentions, crisisActive: $crisisActive, crisisCount: $crisisCount, pendingResponsesCount: $pendingResponsesCount, fraudAlertsCount: $fraudAlertsCount, crisisRiskLevel: $crisisRiskLevel, suspiciousReviewsCount: $suspiciousReviewsCount, activeClustersCount: $activeClustersCount, topIssues: $topIssues, recentMentions: $recentMentions)';
}


}

/// @nodoc
abstract mixin class $DashboardSummaryCopyWith<$Res>  {
  factory $DashboardSummaryCopyWith(DashboardSummary value, $Res Function(DashboardSummary) _then) = _$DashboardSummaryCopyWithImpl;
@useResult
$Res call({
@JsonKey(name: 'reputation_score') ReputationScore reputationScore,@JsonKey(name: 'sentiment_distribution') SentimentDistribution sentimentDistribution,@JsonKey(name: 'total_mentions') int totalMentions,@JsonKey(name: 'crisis_active') bool crisisActive,@JsonKey(name: 'crisis_count') int crisisCount,@JsonKey(name: 'pending_responses_count') int pendingResponsesCount,@JsonKey(name: 'fraud_alerts_count') int fraudAlertsCount,@JsonKey(name: 'crisis_risk_level') String crisisRiskLevel,@JsonKey(name: 'suspicious_reviews_count') int suspiciousReviewsCount,@JsonKey(name: 'active_clusters_count') int activeClustersCount,@JsonKey(name: 'top_issues') List<Map<String, dynamic>> topIssues,@JsonKey(name: 'recent_mentions') List<Mention> recentMentions
});


$ReputationScoreCopyWith<$Res> get reputationScore;$SentimentDistributionCopyWith<$Res> get sentimentDistribution;

}
/// @nodoc
class _$DashboardSummaryCopyWithImpl<$Res>
    implements $DashboardSummaryCopyWith<$Res> {
  _$DashboardSummaryCopyWithImpl(this._self, this._then);

  final DashboardSummary _self;
  final $Res Function(DashboardSummary) _then;

/// Create a copy of DashboardSummary
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? reputationScore = null,Object? sentimentDistribution = null,Object? totalMentions = null,Object? crisisActive = null,Object? crisisCount = null,Object? pendingResponsesCount = null,Object? fraudAlertsCount = null,Object? crisisRiskLevel = null,Object? suspiciousReviewsCount = null,Object? activeClustersCount = null,Object? topIssues = null,Object? recentMentions = null,}) {
  return _then(_self.copyWith(
reputationScore: null == reputationScore ? _self.reputationScore : reputationScore // ignore: cast_nullable_to_non_nullable
as ReputationScore,sentimentDistribution: null == sentimentDistribution ? _self.sentimentDistribution : sentimentDistribution // ignore: cast_nullable_to_non_nullable
as SentimentDistribution,totalMentions: null == totalMentions ? _self.totalMentions : totalMentions // ignore: cast_nullable_to_non_nullable
as int,crisisActive: null == crisisActive ? _self.crisisActive : crisisActive // ignore: cast_nullable_to_non_nullable
as bool,crisisCount: null == crisisCount ? _self.crisisCount : crisisCount // ignore: cast_nullable_to_non_nullable
as int,pendingResponsesCount: null == pendingResponsesCount ? _self.pendingResponsesCount : pendingResponsesCount // ignore: cast_nullable_to_non_nullable
as int,fraudAlertsCount: null == fraudAlertsCount ? _self.fraudAlertsCount : fraudAlertsCount // ignore: cast_nullable_to_non_nullable
as int,crisisRiskLevel: null == crisisRiskLevel ? _self.crisisRiskLevel : crisisRiskLevel // ignore: cast_nullable_to_non_nullable
as String,suspiciousReviewsCount: null == suspiciousReviewsCount ? _self.suspiciousReviewsCount : suspiciousReviewsCount // ignore: cast_nullable_to_non_nullable
as int,activeClustersCount: null == activeClustersCount ? _self.activeClustersCount : activeClustersCount // ignore: cast_nullable_to_non_nullable
as int,topIssues: null == topIssues ? _self.topIssues : topIssues // ignore: cast_nullable_to_non_nullable
as List<Map<String, dynamic>>,recentMentions: null == recentMentions ? _self.recentMentions : recentMentions // ignore: cast_nullable_to_non_nullable
as List<Mention>,
  ));
}
/// Create a copy of DashboardSummary
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$ReputationScoreCopyWith<$Res> get reputationScore {
  
  return $ReputationScoreCopyWith<$Res>(_self.reputationScore, (value) {
    return _then(_self.copyWith(reputationScore: value));
  });
}/// Create a copy of DashboardSummary
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$SentimentDistributionCopyWith<$Res> get sentimentDistribution {
  
  return $SentimentDistributionCopyWith<$Res>(_self.sentimentDistribution, (value) {
    return _then(_self.copyWith(sentimentDistribution: value));
  });
}
}


/// Adds pattern-matching-related methods to [DashboardSummary].
extension DashboardSummaryPatterns on DashboardSummary {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _DashboardSummary value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _DashboardSummary() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _DashboardSummary value)  $default,){
final _that = this;
switch (_that) {
case _DashboardSummary():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _DashboardSummary value)?  $default,){
final _that = this;
switch (_that) {
case _DashboardSummary() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function(@JsonKey(name: 'reputation_score')  ReputationScore reputationScore, @JsonKey(name: 'sentiment_distribution')  SentimentDistribution sentimentDistribution, @JsonKey(name: 'total_mentions')  int totalMentions, @JsonKey(name: 'crisis_active')  bool crisisActive, @JsonKey(name: 'crisis_count')  int crisisCount, @JsonKey(name: 'pending_responses_count')  int pendingResponsesCount, @JsonKey(name: 'fraud_alerts_count')  int fraudAlertsCount, @JsonKey(name: 'crisis_risk_level')  String crisisRiskLevel, @JsonKey(name: 'suspicious_reviews_count')  int suspiciousReviewsCount, @JsonKey(name: 'active_clusters_count')  int activeClustersCount, @JsonKey(name: 'top_issues')  List<Map<String, dynamic>> topIssues, @JsonKey(name: 'recent_mentions')  List<Mention> recentMentions)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _DashboardSummary() when $default != null:
return $default(_that.reputationScore,_that.sentimentDistribution,_that.totalMentions,_that.crisisActive,_that.crisisCount,_that.pendingResponsesCount,_that.fraudAlertsCount,_that.crisisRiskLevel,_that.suspiciousReviewsCount,_that.activeClustersCount,_that.topIssues,_that.recentMentions);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function(@JsonKey(name: 'reputation_score')  ReputationScore reputationScore, @JsonKey(name: 'sentiment_distribution')  SentimentDistribution sentimentDistribution, @JsonKey(name: 'total_mentions')  int totalMentions, @JsonKey(name: 'crisis_active')  bool crisisActive, @JsonKey(name: 'crisis_count')  int crisisCount, @JsonKey(name: 'pending_responses_count')  int pendingResponsesCount, @JsonKey(name: 'fraud_alerts_count')  int fraudAlertsCount, @JsonKey(name: 'crisis_risk_level')  String crisisRiskLevel, @JsonKey(name: 'suspicious_reviews_count')  int suspiciousReviewsCount, @JsonKey(name: 'active_clusters_count')  int activeClustersCount, @JsonKey(name: 'top_issues')  List<Map<String, dynamic>> topIssues, @JsonKey(name: 'recent_mentions')  List<Mention> recentMentions)  $default,) {final _that = this;
switch (_that) {
case _DashboardSummary():
return $default(_that.reputationScore,_that.sentimentDistribution,_that.totalMentions,_that.crisisActive,_that.crisisCount,_that.pendingResponsesCount,_that.fraudAlertsCount,_that.crisisRiskLevel,_that.suspiciousReviewsCount,_that.activeClustersCount,_that.topIssues,_that.recentMentions);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function(@JsonKey(name: 'reputation_score')  ReputationScore reputationScore, @JsonKey(name: 'sentiment_distribution')  SentimentDistribution sentimentDistribution, @JsonKey(name: 'total_mentions')  int totalMentions, @JsonKey(name: 'crisis_active')  bool crisisActive, @JsonKey(name: 'crisis_count')  int crisisCount, @JsonKey(name: 'pending_responses_count')  int pendingResponsesCount, @JsonKey(name: 'fraud_alerts_count')  int fraudAlertsCount, @JsonKey(name: 'crisis_risk_level')  String crisisRiskLevel, @JsonKey(name: 'suspicious_reviews_count')  int suspiciousReviewsCount, @JsonKey(name: 'active_clusters_count')  int activeClustersCount, @JsonKey(name: 'top_issues')  List<Map<String, dynamic>> topIssues, @JsonKey(name: 'recent_mentions')  List<Mention> recentMentions)?  $default,) {final _that = this;
switch (_that) {
case _DashboardSummary() when $default != null:
return $default(_that.reputationScore,_that.sentimentDistribution,_that.totalMentions,_that.crisisActive,_that.crisisCount,_that.pendingResponsesCount,_that.fraudAlertsCount,_that.crisisRiskLevel,_that.suspiciousReviewsCount,_that.activeClustersCount,_that.topIssues,_that.recentMentions);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _DashboardSummary implements DashboardSummary {
  const _DashboardSummary({@JsonKey(name: 'reputation_score') required this.reputationScore, @JsonKey(name: 'sentiment_distribution') required this.sentimentDistribution, @JsonKey(name: 'total_mentions') this.totalMentions = 0, @JsonKey(name: 'crisis_active') this.crisisActive = false, @JsonKey(name: 'crisis_count') this.crisisCount = 0, @JsonKey(name: 'pending_responses_count') this.pendingResponsesCount = 0, @JsonKey(name: 'fraud_alerts_count') this.fraudAlertsCount = 0, @JsonKey(name: 'crisis_risk_level') this.crisisRiskLevel = 'Normal', @JsonKey(name: 'suspicious_reviews_count') this.suspiciousReviewsCount = 0, @JsonKey(name: 'active_clusters_count') this.activeClustersCount = 0, @JsonKey(name: 'top_issues') this.topIssues = const [], @JsonKey(name: 'recent_mentions') this.recentMentions = const []});
  factory _DashboardSummary.fromJson(Map<String, dynamic> json) => _$DashboardSummaryFromJson(json);

@override@JsonKey(name: 'reputation_score') final  ReputationScore reputationScore;
@override@JsonKey(name: 'sentiment_distribution') final  SentimentDistribution sentimentDistribution;
@override@JsonKey(name: 'total_mentions') final  int totalMentions;
@override@JsonKey(name: 'crisis_active') final  bool crisisActive;
@override@JsonKey(name: 'crisis_count') final  int crisisCount;
@override@JsonKey(name: 'pending_responses_count') final  int pendingResponsesCount;
@override@JsonKey(name: 'fraud_alerts_count') final  int fraudAlertsCount;
@override@JsonKey(name: 'crisis_risk_level') final  String crisisRiskLevel;
@override@JsonKey(name: 'suspicious_reviews_count') final  int suspiciousReviewsCount;
@override@JsonKey(name: 'active_clusters_count') final  int activeClustersCount;
@override@JsonKey(name: 'top_issues') final  List<Map<String, dynamic>> topIssues;
@override@JsonKey(name: 'recent_mentions') final  List<Mention> recentMentions;

/// Create a copy of DashboardSummary
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$DashboardSummaryCopyWith<_DashboardSummary> get copyWith => __$DashboardSummaryCopyWithImpl<_DashboardSummary>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$DashboardSummaryToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _DashboardSummary&&(identical(other.reputationScore, reputationScore) || other.reputationScore == reputationScore)&&(identical(other.sentimentDistribution, sentimentDistribution) || other.sentimentDistribution == sentimentDistribution)&&(identical(other.totalMentions, totalMentions) || other.totalMentions == totalMentions)&&(identical(other.crisisActive, crisisActive) || other.crisisActive == crisisActive)&&(identical(other.crisisCount, crisisCount) || other.crisisCount == crisisCount)&&(identical(other.pendingResponsesCount, pendingResponsesCount) || other.pendingResponsesCount == pendingResponsesCount)&&(identical(other.fraudAlertsCount, fraudAlertsCount) || other.fraudAlertsCount == fraudAlertsCount)&&(identical(other.crisisRiskLevel, crisisRiskLevel) || other.crisisRiskLevel == crisisRiskLevel)&&(identical(other.suspiciousReviewsCount, suspiciousReviewsCount) || other.suspiciousReviewsCount == suspiciousReviewsCount)&&(identical(other.activeClustersCount, activeClustersCount) || other.activeClustersCount == activeClustersCount)&&const DeepCollectionEquality().equals(other.topIssues, topIssues)&&const DeepCollectionEquality().equals(other.recentMentions, recentMentions));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,reputationScore,sentimentDistribution,totalMentions,crisisActive,crisisCount,pendingResponsesCount,fraudAlertsCount,crisisRiskLevel,suspiciousReviewsCount,activeClustersCount,const DeepCollectionEquality().hash(topIssues),const DeepCollectionEquality().hash(recentMentions));

@override
String toString() {
  return 'DashboardSummary(reputationScore: $reputationScore, sentimentDistribution: $sentimentDistribution, totalMentions: $totalMentions, crisisActive: $crisisActive, crisisCount: $crisisCount, pendingResponsesCount: $pendingResponsesCount, fraudAlertsCount: $fraudAlertsCount, crisisRiskLevel: $crisisRiskLevel, suspiciousReviewsCount: $suspiciousReviewsCount, activeClustersCount: $activeClustersCount, topIssues: $topIssues, recentMentions: $recentMentions)';
}


}

/// @nodoc
abstract mixin class _$DashboardSummaryCopyWith<$Res> implements $DashboardSummaryCopyWith<$Res> {
  factory _$DashboardSummaryCopyWith(_DashboardSummary value, $Res Function(_DashboardSummary) _then) = __$DashboardSummaryCopyWithImpl;
@override @useResult
$Res call({
@JsonKey(name: 'reputation_score') ReputationScore reputationScore,@JsonKey(name: 'sentiment_distribution') SentimentDistribution sentimentDistribution,@JsonKey(name: 'total_mentions') int totalMentions,@JsonKey(name: 'crisis_active') bool crisisActive,@JsonKey(name: 'crisis_count') int crisisCount,@JsonKey(name: 'pending_responses_count') int pendingResponsesCount,@JsonKey(name: 'fraud_alerts_count') int fraudAlertsCount,@JsonKey(name: 'crisis_risk_level') String crisisRiskLevel,@JsonKey(name: 'suspicious_reviews_count') int suspiciousReviewsCount,@JsonKey(name: 'active_clusters_count') int activeClustersCount,@JsonKey(name: 'top_issues') List<Map<String, dynamic>> topIssues,@JsonKey(name: 'recent_mentions') List<Mention> recentMentions
});


@override $ReputationScoreCopyWith<$Res> get reputationScore;@override $SentimentDistributionCopyWith<$Res> get sentimentDistribution;

}
/// @nodoc
class __$DashboardSummaryCopyWithImpl<$Res>
    implements _$DashboardSummaryCopyWith<$Res> {
  __$DashboardSummaryCopyWithImpl(this._self, this._then);

  final _DashboardSummary _self;
  final $Res Function(_DashboardSummary) _then;

/// Create a copy of DashboardSummary
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? reputationScore = null,Object? sentimentDistribution = null,Object? totalMentions = null,Object? crisisActive = null,Object? crisisCount = null,Object? pendingResponsesCount = null,Object? fraudAlertsCount = null,Object? crisisRiskLevel = null,Object? suspiciousReviewsCount = null,Object? activeClustersCount = null,Object? topIssues = null,Object? recentMentions = null,}) {
  return _then(_DashboardSummary(
reputationScore: null == reputationScore ? _self.reputationScore : reputationScore // ignore: cast_nullable_to_non_nullable
as ReputationScore,sentimentDistribution: null == sentimentDistribution ? _self.sentimentDistribution : sentimentDistribution // ignore: cast_nullable_to_non_nullable
as SentimentDistribution,totalMentions: null == totalMentions ? _self.totalMentions : totalMentions // ignore: cast_nullable_to_non_nullable
as int,crisisActive: null == crisisActive ? _self.crisisActive : crisisActive // ignore: cast_nullable_to_non_nullable
as bool,crisisCount: null == crisisCount ? _self.crisisCount : crisisCount // ignore: cast_nullable_to_non_nullable
as int,pendingResponsesCount: null == pendingResponsesCount ? _self.pendingResponsesCount : pendingResponsesCount // ignore: cast_nullable_to_non_nullable
as int,fraudAlertsCount: null == fraudAlertsCount ? _self.fraudAlertsCount : fraudAlertsCount // ignore: cast_nullable_to_non_nullable
as int,crisisRiskLevel: null == crisisRiskLevel ? _self.crisisRiskLevel : crisisRiskLevel // ignore: cast_nullable_to_non_nullable
as String,suspiciousReviewsCount: null == suspiciousReviewsCount ? _self.suspiciousReviewsCount : suspiciousReviewsCount // ignore: cast_nullable_to_non_nullable
as int,activeClustersCount: null == activeClustersCount ? _self.activeClustersCount : activeClustersCount // ignore: cast_nullable_to_non_nullable
as int,topIssues: null == topIssues ? _self.topIssues : topIssues // ignore: cast_nullable_to_non_nullable
as List<Map<String, dynamic>>,recentMentions: null == recentMentions ? _self.recentMentions : recentMentions // ignore: cast_nullable_to_non_nullable
as List<Mention>,
  ));
}

/// Create a copy of DashboardSummary
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$ReputationScoreCopyWith<$Res> get reputationScore {
  
  return $ReputationScoreCopyWith<$Res>(_self.reputationScore, (value) {
    return _then(_self.copyWith(reputationScore: value));
  });
}/// Create a copy of DashboardSummary
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$SentimentDistributionCopyWith<$Res> get sentimentDistribution {
  
  return $SentimentDistributionCopyWith<$Res>(_self.sentimentDistribution, (value) {
    return _then(_self.copyWith(sentimentDistribution: value));
  });
}
}

// dart format on
