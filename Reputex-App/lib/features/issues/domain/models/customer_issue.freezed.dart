// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'customer_issue.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$IssueEvidence {

 String get id;@JsonKey(name: 'mention_id') String get mentionId;@JsonKey(name: 'relevance_score') double get relevanceScore; String? get excerpt;@JsonKey(name: 'created_at') DateTime get createdAt;
/// Create a copy of IssueEvidence
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$IssueEvidenceCopyWith<IssueEvidence> get copyWith => _$IssueEvidenceCopyWithImpl<IssueEvidence>(this as IssueEvidence, _$identity);

  /// Serializes this IssueEvidence to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is IssueEvidence&&(identical(other.id, id) || other.id == id)&&(identical(other.mentionId, mentionId) || other.mentionId == mentionId)&&(identical(other.relevanceScore, relevanceScore) || other.relevanceScore == relevanceScore)&&(identical(other.excerpt, excerpt) || other.excerpt == excerpt)&&(identical(other.createdAt, createdAt) || other.createdAt == createdAt));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,mentionId,relevanceScore,excerpt,createdAt);

@override
String toString() {
  return 'IssueEvidence(id: $id, mentionId: $mentionId, relevanceScore: $relevanceScore, excerpt: $excerpt, createdAt: $createdAt)';
}


}

/// @nodoc
abstract mixin class $IssueEvidenceCopyWith<$Res>  {
  factory $IssueEvidenceCopyWith(IssueEvidence value, $Res Function(IssueEvidence) _then) = _$IssueEvidenceCopyWithImpl;
@useResult
$Res call({
 String id,@JsonKey(name: 'mention_id') String mentionId,@JsonKey(name: 'relevance_score') double relevanceScore, String? excerpt,@JsonKey(name: 'created_at') DateTime createdAt
});




}
/// @nodoc
class _$IssueEvidenceCopyWithImpl<$Res>
    implements $IssueEvidenceCopyWith<$Res> {
  _$IssueEvidenceCopyWithImpl(this._self, this._then);

  final IssueEvidence _self;
  final $Res Function(IssueEvidence) _then;

/// Create a copy of IssueEvidence
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? mentionId = null,Object? relevanceScore = null,Object? excerpt = freezed,Object? createdAt = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,mentionId: null == mentionId ? _self.mentionId : mentionId // ignore: cast_nullable_to_non_nullable
as String,relevanceScore: null == relevanceScore ? _self.relevanceScore : relevanceScore // ignore: cast_nullable_to_non_nullable
as double,excerpt: freezed == excerpt ? _self.excerpt : excerpt // ignore: cast_nullable_to_non_nullable
as String?,createdAt: null == createdAt ? _self.createdAt : createdAt // ignore: cast_nullable_to_non_nullable
as DateTime,
  ));
}

}


/// Adds pattern-matching-related methods to [IssueEvidence].
extension IssueEvidencePatterns on IssueEvidence {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _IssueEvidence value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _IssueEvidence() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _IssueEvidence value)  $default,){
final _that = this;
switch (_that) {
case _IssueEvidence():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _IssueEvidence value)?  $default,){
final _that = this;
switch (_that) {
case _IssueEvidence() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'mention_id')  String mentionId, @JsonKey(name: 'relevance_score')  double relevanceScore,  String? excerpt, @JsonKey(name: 'created_at')  DateTime createdAt)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _IssueEvidence() when $default != null:
return $default(_that.id,_that.mentionId,_that.relevanceScore,_that.excerpt,_that.createdAt);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'mention_id')  String mentionId, @JsonKey(name: 'relevance_score')  double relevanceScore,  String? excerpt, @JsonKey(name: 'created_at')  DateTime createdAt)  $default,) {final _that = this;
switch (_that) {
case _IssueEvidence():
return $default(_that.id,_that.mentionId,_that.relevanceScore,_that.excerpt,_that.createdAt);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id, @JsonKey(name: 'mention_id')  String mentionId, @JsonKey(name: 'relevance_score')  double relevanceScore,  String? excerpt, @JsonKey(name: 'created_at')  DateTime createdAt)?  $default,) {final _that = this;
switch (_that) {
case _IssueEvidence() when $default != null:
return $default(_that.id,_that.mentionId,_that.relevanceScore,_that.excerpt,_that.createdAt);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _IssueEvidence implements IssueEvidence {
  const _IssueEvidence({required this.id, @JsonKey(name: 'mention_id') required this.mentionId, @JsonKey(name: 'relevance_score') this.relevanceScore = 1.0, this.excerpt, @JsonKey(name: 'created_at') required this.createdAt});
  factory _IssueEvidence.fromJson(Map<String, dynamic> json) => _$IssueEvidenceFromJson(json);

@override final  String id;
@override@JsonKey(name: 'mention_id') final  String mentionId;
@override@JsonKey(name: 'relevance_score') final  double relevanceScore;
@override final  String? excerpt;
@override@JsonKey(name: 'created_at') final  DateTime createdAt;

/// Create a copy of IssueEvidence
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$IssueEvidenceCopyWith<_IssueEvidence> get copyWith => __$IssueEvidenceCopyWithImpl<_IssueEvidence>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$IssueEvidenceToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _IssueEvidence&&(identical(other.id, id) || other.id == id)&&(identical(other.mentionId, mentionId) || other.mentionId == mentionId)&&(identical(other.relevanceScore, relevanceScore) || other.relevanceScore == relevanceScore)&&(identical(other.excerpt, excerpt) || other.excerpt == excerpt)&&(identical(other.createdAt, createdAt) || other.createdAt == createdAt));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,mentionId,relevanceScore,excerpt,createdAt);

@override
String toString() {
  return 'IssueEvidence(id: $id, mentionId: $mentionId, relevanceScore: $relevanceScore, excerpt: $excerpt, createdAt: $createdAt)';
}


}

/// @nodoc
abstract mixin class _$IssueEvidenceCopyWith<$Res> implements $IssueEvidenceCopyWith<$Res> {
  factory _$IssueEvidenceCopyWith(_IssueEvidence value, $Res Function(_IssueEvidence) _then) = __$IssueEvidenceCopyWithImpl;
@override @useResult
$Res call({
 String id,@JsonKey(name: 'mention_id') String mentionId,@JsonKey(name: 'relevance_score') double relevanceScore, String? excerpt,@JsonKey(name: 'created_at') DateTime createdAt
});




}
/// @nodoc
class __$IssueEvidenceCopyWithImpl<$Res>
    implements _$IssueEvidenceCopyWith<$Res> {
  __$IssueEvidenceCopyWithImpl(this._self, this._then);

  final _IssueEvidence _self;
  final $Res Function(_IssueEvidence) _then;

/// Create a copy of IssueEvidence
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? mentionId = null,Object? relevanceScore = null,Object? excerpt = freezed,Object? createdAt = null,}) {
  return _then(_IssueEvidence(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,mentionId: null == mentionId ? _self.mentionId : mentionId // ignore: cast_nullable_to_non_nullable
as String,relevanceScore: null == relevanceScore ? _self.relevanceScore : relevanceScore // ignore: cast_nullable_to_non_nullable
as double,excerpt: freezed == excerpt ? _self.excerpt : excerpt // ignore: cast_nullable_to_non_nullable
as String?,createdAt: null == createdAt ? _self.createdAt : createdAt // ignore: cast_nullable_to_non_nullable
as DateTime,
  ));
}


}


/// @nodoc
mixin _$CustomerIssue {

 String get id;@JsonKey(name: 'business_id') String get businessId; String get category; String get subtopic; String get severity; String get status;@JsonKey(name: 'mention_count') int get mentionCount;@JsonKey(name: 'platforms_breakdown') Map<String, int> get platformsBreakdown;@JsonKey(name: 'sentiment_breakdown') Map<String, int> get sentimentBreakdown;@JsonKey(name: 'first_seen_at') DateTime get firstSeenAt;@JsonKey(name: 'last_seen_at') DateTime get lastSeenAt; List<IssueEvidence> get evidence;
/// Create a copy of CustomerIssue
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$CustomerIssueCopyWith<CustomerIssue> get copyWith => _$CustomerIssueCopyWithImpl<CustomerIssue>(this as CustomerIssue, _$identity);

  /// Serializes this CustomerIssue to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is CustomerIssue&&(identical(other.id, id) || other.id == id)&&(identical(other.businessId, businessId) || other.businessId == businessId)&&(identical(other.category, category) || other.category == category)&&(identical(other.subtopic, subtopic) || other.subtopic == subtopic)&&(identical(other.severity, severity) || other.severity == severity)&&(identical(other.status, status) || other.status == status)&&(identical(other.mentionCount, mentionCount) || other.mentionCount == mentionCount)&&const DeepCollectionEquality().equals(other.platformsBreakdown, platformsBreakdown)&&const DeepCollectionEquality().equals(other.sentimentBreakdown, sentimentBreakdown)&&(identical(other.firstSeenAt, firstSeenAt) || other.firstSeenAt == firstSeenAt)&&(identical(other.lastSeenAt, lastSeenAt) || other.lastSeenAt == lastSeenAt)&&const DeepCollectionEquality().equals(other.evidence, evidence));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,businessId,category,subtopic,severity,status,mentionCount,const DeepCollectionEquality().hash(platformsBreakdown),const DeepCollectionEquality().hash(sentimentBreakdown),firstSeenAt,lastSeenAt,const DeepCollectionEquality().hash(evidence));

@override
String toString() {
  return 'CustomerIssue(id: $id, businessId: $businessId, category: $category, subtopic: $subtopic, severity: $severity, status: $status, mentionCount: $mentionCount, platformsBreakdown: $platformsBreakdown, sentimentBreakdown: $sentimentBreakdown, firstSeenAt: $firstSeenAt, lastSeenAt: $lastSeenAt, evidence: $evidence)';
}


}

/// @nodoc
abstract mixin class $CustomerIssueCopyWith<$Res>  {
  factory $CustomerIssueCopyWith(CustomerIssue value, $Res Function(CustomerIssue) _then) = _$CustomerIssueCopyWithImpl;
@useResult
$Res call({
 String id,@JsonKey(name: 'business_id') String businessId, String category, String subtopic, String severity, String status,@JsonKey(name: 'mention_count') int mentionCount,@JsonKey(name: 'platforms_breakdown') Map<String, int> platformsBreakdown,@JsonKey(name: 'sentiment_breakdown') Map<String, int> sentimentBreakdown,@JsonKey(name: 'first_seen_at') DateTime firstSeenAt,@JsonKey(name: 'last_seen_at') DateTime lastSeenAt, List<IssueEvidence> evidence
});




}
/// @nodoc
class _$CustomerIssueCopyWithImpl<$Res>
    implements $CustomerIssueCopyWith<$Res> {
  _$CustomerIssueCopyWithImpl(this._self, this._then);

  final CustomerIssue _self;
  final $Res Function(CustomerIssue) _then;

/// Create a copy of CustomerIssue
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? businessId = null,Object? category = null,Object? subtopic = null,Object? severity = null,Object? status = null,Object? mentionCount = null,Object? platformsBreakdown = null,Object? sentimentBreakdown = null,Object? firstSeenAt = null,Object? lastSeenAt = null,Object? evidence = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,businessId: null == businessId ? _self.businessId : businessId // ignore: cast_nullable_to_non_nullable
as String,category: null == category ? _self.category : category // ignore: cast_nullable_to_non_nullable
as String,subtopic: null == subtopic ? _self.subtopic : subtopic // ignore: cast_nullable_to_non_nullable
as String,severity: null == severity ? _self.severity : severity // ignore: cast_nullable_to_non_nullable
as String,status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,mentionCount: null == mentionCount ? _self.mentionCount : mentionCount // ignore: cast_nullable_to_non_nullable
as int,platformsBreakdown: null == platformsBreakdown ? _self.platformsBreakdown : platformsBreakdown // ignore: cast_nullable_to_non_nullable
as Map<String, int>,sentimentBreakdown: null == sentimentBreakdown ? _self.sentimentBreakdown : sentimentBreakdown // ignore: cast_nullable_to_non_nullable
as Map<String, int>,firstSeenAt: null == firstSeenAt ? _self.firstSeenAt : firstSeenAt // ignore: cast_nullable_to_non_nullable
as DateTime,lastSeenAt: null == lastSeenAt ? _self.lastSeenAt : lastSeenAt // ignore: cast_nullable_to_non_nullable
as DateTime,evidence: null == evidence ? _self.evidence : evidence // ignore: cast_nullable_to_non_nullable
as List<IssueEvidence>,
  ));
}

}


/// Adds pattern-matching-related methods to [CustomerIssue].
extension CustomerIssuePatterns on CustomerIssue {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _CustomerIssue value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _CustomerIssue() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _CustomerIssue value)  $default,){
final _that = this;
switch (_that) {
case _CustomerIssue():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _CustomerIssue value)?  $default,){
final _that = this;
switch (_that) {
case _CustomerIssue() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'business_id')  String businessId,  String category,  String subtopic,  String severity,  String status, @JsonKey(name: 'mention_count')  int mentionCount, @JsonKey(name: 'platforms_breakdown')  Map<String, int> platformsBreakdown, @JsonKey(name: 'sentiment_breakdown')  Map<String, int> sentimentBreakdown, @JsonKey(name: 'first_seen_at')  DateTime firstSeenAt, @JsonKey(name: 'last_seen_at')  DateTime lastSeenAt,  List<IssueEvidence> evidence)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _CustomerIssue() when $default != null:
return $default(_that.id,_that.businessId,_that.category,_that.subtopic,_that.severity,_that.status,_that.mentionCount,_that.platformsBreakdown,_that.sentimentBreakdown,_that.firstSeenAt,_that.lastSeenAt,_that.evidence);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'business_id')  String businessId,  String category,  String subtopic,  String severity,  String status, @JsonKey(name: 'mention_count')  int mentionCount, @JsonKey(name: 'platforms_breakdown')  Map<String, int> platformsBreakdown, @JsonKey(name: 'sentiment_breakdown')  Map<String, int> sentimentBreakdown, @JsonKey(name: 'first_seen_at')  DateTime firstSeenAt, @JsonKey(name: 'last_seen_at')  DateTime lastSeenAt,  List<IssueEvidence> evidence)  $default,) {final _that = this;
switch (_that) {
case _CustomerIssue():
return $default(_that.id,_that.businessId,_that.category,_that.subtopic,_that.severity,_that.status,_that.mentionCount,_that.platformsBreakdown,_that.sentimentBreakdown,_that.firstSeenAt,_that.lastSeenAt,_that.evidence);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id, @JsonKey(name: 'business_id')  String businessId,  String category,  String subtopic,  String severity,  String status, @JsonKey(name: 'mention_count')  int mentionCount, @JsonKey(name: 'platforms_breakdown')  Map<String, int> platformsBreakdown, @JsonKey(name: 'sentiment_breakdown')  Map<String, int> sentimentBreakdown, @JsonKey(name: 'first_seen_at')  DateTime firstSeenAt, @JsonKey(name: 'last_seen_at')  DateTime lastSeenAt,  List<IssueEvidence> evidence)?  $default,) {final _that = this;
switch (_that) {
case _CustomerIssue() when $default != null:
return $default(_that.id,_that.businessId,_that.category,_that.subtopic,_that.severity,_that.status,_that.mentionCount,_that.platformsBreakdown,_that.sentimentBreakdown,_that.firstSeenAt,_that.lastSeenAt,_that.evidence);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _CustomerIssue implements CustomerIssue {
  const _CustomerIssue({required this.id, @JsonKey(name: 'business_id') required this.businessId, required this.category, required this.subtopic, this.severity = 'medium', this.status = 'emerging', @JsonKey(name: 'mention_count') this.mentionCount = 0, @JsonKey(name: 'platforms_breakdown') this.platformsBreakdown = const {}, @JsonKey(name: 'sentiment_breakdown') this.sentimentBreakdown = const {}, @JsonKey(name: 'first_seen_at') required this.firstSeenAt, @JsonKey(name: 'last_seen_at') required this.lastSeenAt, this.evidence = const []});
  factory _CustomerIssue.fromJson(Map<String, dynamic> json) => _$CustomerIssueFromJson(json);

@override final  String id;
@override@JsonKey(name: 'business_id') final  String businessId;
@override final  String category;
@override final  String subtopic;
@override@JsonKey() final  String severity;
@override@JsonKey() final  String status;
@override@JsonKey(name: 'mention_count') final  int mentionCount;
@override@JsonKey(name: 'platforms_breakdown') final  Map<String, int> platformsBreakdown;
@override@JsonKey(name: 'sentiment_breakdown') final  Map<String, int> sentimentBreakdown;
@override@JsonKey(name: 'first_seen_at') final  DateTime firstSeenAt;
@override@JsonKey(name: 'last_seen_at') final  DateTime lastSeenAt;
@override@JsonKey() final  List<IssueEvidence> evidence;

/// Create a copy of CustomerIssue
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$CustomerIssueCopyWith<_CustomerIssue> get copyWith => __$CustomerIssueCopyWithImpl<_CustomerIssue>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$CustomerIssueToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _CustomerIssue&&(identical(other.id, id) || other.id == id)&&(identical(other.businessId, businessId) || other.businessId == businessId)&&(identical(other.category, category) || other.category == category)&&(identical(other.subtopic, subtopic) || other.subtopic == subtopic)&&(identical(other.severity, severity) || other.severity == severity)&&(identical(other.status, status) || other.status == status)&&(identical(other.mentionCount, mentionCount) || other.mentionCount == mentionCount)&&const DeepCollectionEquality().equals(other.platformsBreakdown, platformsBreakdown)&&const DeepCollectionEquality().equals(other.sentimentBreakdown, sentimentBreakdown)&&(identical(other.firstSeenAt, firstSeenAt) || other.firstSeenAt == firstSeenAt)&&(identical(other.lastSeenAt, lastSeenAt) || other.lastSeenAt == lastSeenAt)&&const DeepCollectionEquality().equals(other.evidence, evidence));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,businessId,category,subtopic,severity,status,mentionCount,const DeepCollectionEquality().hash(platformsBreakdown),const DeepCollectionEquality().hash(sentimentBreakdown),firstSeenAt,lastSeenAt,const DeepCollectionEquality().hash(evidence));

@override
String toString() {
  return 'CustomerIssue(id: $id, businessId: $businessId, category: $category, subtopic: $subtopic, severity: $severity, status: $status, mentionCount: $mentionCount, platformsBreakdown: $platformsBreakdown, sentimentBreakdown: $sentimentBreakdown, firstSeenAt: $firstSeenAt, lastSeenAt: $lastSeenAt, evidence: $evidence)';
}


}

/// @nodoc
abstract mixin class _$CustomerIssueCopyWith<$Res> implements $CustomerIssueCopyWith<$Res> {
  factory _$CustomerIssueCopyWith(_CustomerIssue value, $Res Function(_CustomerIssue) _then) = __$CustomerIssueCopyWithImpl;
@override @useResult
$Res call({
 String id,@JsonKey(name: 'business_id') String businessId, String category, String subtopic, String severity, String status,@JsonKey(name: 'mention_count') int mentionCount,@JsonKey(name: 'platforms_breakdown') Map<String, int> platformsBreakdown,@JsonKey(name: 'sentiment_breakdown') Map<String, int> sentimentBreakdown,@JsonKey(name: 'first_seen_at') DateTime firstSeenAt,@JsonKey(name: 'last_seen_at') DateTime lastSeenAt, List<IssueEvidence> evidence
});




}
/// @nodoc
class __$CustomerIssueCopyWithImpl<$Res>
    implements _$CustomerIssueCopyWith<$Res> {
  __$CustomerIssueCopyWithImpl(this._self, this._then);

  final _CustomerIssue _self;
  final $Res Function(_CustomerIssue) _then;

/// Create a copy of CustomerIssue
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? businessId = null,Object? category = null,Object? subtopic = null,Object? severity = null,Object? status = null,Object? mentionCount = null,Object? platformsBreakdown = null,Object? sentimentBreakdown = null,Object? firstSeenAt = null,Object? lastSeenAt = null,Object? evidence = null,}) {
  return _then(_CustomerIssue(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,businessId: null == businessId ? _self.businessId : businessId // ignore: cast_nullable_to_non_nullable
as String,category: null == category ? _self.category : category // ignore: cast_nullable_to_non_nullable
as String,subtopic: null == subtopic ? _self.subtopic : subtopic // ignore: cast_nullable_to_non_nullable
as String,severity: null == severity ? _self.severity : severity // ignore: cast_nullable_to_non_nullable
as String,status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,mentionCount: null == mentionCount ? _self.mentionCount : mentionCount // ignore: cast_nullable_to_non_nullable
as int,platformsBreakdown: null == platformsBreakdown ? _self.platformsBreakdown : platformsBreakdown // ignore: cast_nullable_to_non_nullable
as Map<String, int>,sentimentBreakdown: null == sentimentBreakdown ? _self.sentimentBreakdown : sentimentBreakdown // ignore: cast_nullable_to_non_nullable
as Map<String, int>,firstSeenAt: null == firstSeenAt ? _self.firstSeenAt : firstSeenAt // ignore: cast_nullable_to_non_nullable
as DateTime,lastSeenAt: null == lastSeenAt ? _self.lastSeenAt : lastSeenAt // ignore: cast_nullable_to_non_nullable
as DateTime,evidence: null == evidence ? _self.evidence : evidence // ignore: cast_nullable_to_non_nullable
as List<IssueEvidence>,
  ));
}


}

// dart format on
