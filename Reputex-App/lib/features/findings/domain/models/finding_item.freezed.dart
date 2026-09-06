// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'finding_item.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$FindingEvidenceItem {

 String get id;@JsonKey(name: 'finding_id') String get findingId;@JsonKey(name: 'mention_id') String get mentionId;@JsonKey(name: 'evidence_type') String get evidenceType; String? get snippet;@JsonKey(name: 'relevance_score') double get relevanceScore;@JsonKey(name: 'created_at') DateTime get createdAt;
/// Create a copy of FindingEvidenceItem
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$FindingEvidenceItemCopyWith<FindingEvidenceItem> get copyWith => _$FindingEvidenceItemCopyWithImpl<FindingEvidenceItem>(this as FindingEvidenceItem, _$identity);

  /// Serializes this FindingEvidenceItem to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is FindingEvidenceItem&&(identical(other.id, id) || other.id == id)&&(identical(other.findingId, findingId) || other.findingId == findingId)&&(identical(other.mentionId, mentionId) || other.mentionId == mentionId)&&(identical(other.evidenceType, evidenceType) || other.evidenceType == evidenceType)&&(identical(other.snippet, snippet) || other.snippet == snippet)&&(identical(other.relevanceScore, relevanceScore) || other.relevanceScore == relevanceScore)&&(identical(other.createdAt, createdAt) || other.createdAt == createdAt));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,findingId,mentionId,evidenceType,snippet,relevanceScore,createdAt);

@override
String toString() {
  return 'FindingEvidenceItem(id: $id, findingId: $findingId, mentionId: $mentionId, evidenceType: $evidenceType, snippet: $snippet, relevanceScore: $relevanceScore, createdAt: $createdAt)';
}


}

/// @nodoc
abstract mixin class $FindingEvidenceItemCopyWith<$Res>  {
  factory $FindingEvidenceItemCopyWith(FindingEvidenceItem value, $Res Function(FindingEvidenceItem) _then) = _$FindingEvidenceItemCopyWithImpl;
@useResult
$Res call({
 String id,@JsonKey(name: 'finding_id') String findingId,@JsonKey(name: 'mention_id') String mentionId,@JsonKey(name: 'evidence_type') String evidenceType, String? snippet,@JsonKey(name: 'relevance_score') double relevanceScore,@JsonKey(name: 'created_at') DateTime createdAt
});




}
/// @nodoc
class _$FindingEvidenceItemCopyWithImpl<$Res>
    implements $FindingEvidenceItemCopyWith<$Res> {
  _$FindingEvidenceItemCopyWithImpl(this._self, this._then);

  final FindingEvidenceItem _self;
  final $Res Function(FindingEvidenceItem) _then;

/// Create a copy of FindingEvidenceItem
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? findingId = null,Object? mentionId = null,Object? evidenceType = null,Object? snippet = freezed,Object? relevanceScore = null,Object? createdAt = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,findingId: null == findingId ? _self.findingId : findingId // ignore: cast_nullable_to_non_nullable
as String,mentionId: null == mentionId ? _self.mentionId : mentionId // ignore: cast_nullable_to_non_nullable
as String,evidenceType: null == evidenceType ? _self.evidenceType : evidenceType // ignore: cast_nullable_to_non_nullable
as String,snippet: freezed == snippet ? _self.snippet : snippet // ignore: cast_nullable_to_non_nullable
as String?,relevanceScore: null == relevanceScore ? _self.relevanceScore : relevanceScore // ignore: cast_nullable_to_non_nullable
as double,createdAt: null == createdAt ? _self.createdAt : createdAt // ignore: cast_nullable_to_non_nullable
as DateTime,
  ));
}

}


/// Adds pattern-matching-related methods to [FindingEvidenceItem].
extension FindingEvidenceItemPatterns on FindingEvidenceItem {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _FindingEvidenceItem value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _FindingEvidenceItem() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _FindingEvidenceItem value)  $default,){
final _that = this;
switch (_that) {
case _FindingEvidenceItem():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _FindingEvidenceItem value)?  $default,){
final _that = this;
switch (_that) {
case _FindingEvidenceItem() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'finding_id')  String findingId, @JsonKey(name: 'mention_id')  String mentionId, @JsonKey(name: 'evidence_type')  String evidenceType,  String? snippet, @JsonKey(name: 'relevance_score')  double relevanceScore, @JsonKey(name: 'created_at')  DateTime createdAt)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _FindingEvidenceItem() when $default != null:
return $default(_that.id,_that.findingId,_that.mentionId,_that.evidenceType,_that.snippet,_that.relevanceScore,_that.createdAt);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'finding_id')  String findingId, @JsonKey(name: 'mention_id')  String mentionId, @JsonKey(name: 'evidence_type')  String evidenceType,  String? snippet, @JsonKey(name: 'relevance_score')  double relevanceScore, @JsonKey(name: 'created_at')  DateTime createdAt)  $default,) {final _that = this;
switch (_that) {
case _FindingEvidenceItem():
return $default(_that.id,_that.findingId,_that.mentionId,_that.evidenceType,_that.snippet,_that.relevanceScore,_that.createdAt);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id, @JsonKey(name: 'finding_id')  String findingId, @JsonKey(name: 'mention_id')  String mentionId, @JsonKey(name: 'evidence_type')  String evidenceType,  String? snippet, @JsonKey(name: 'relevance_score')  double relevanceScore, @JsonKey(name: 'created_at')  DateTime createdAt)?  $default,) {final _that = this;
switch (_that) {
case _FindingEvidenceItem() when $default != null:
return $default(_that.id,_that.findingId,_that.mentionId,_that.evidenceType,_that.snippet,_that.relevanceScore,_that.createdAt);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _FindingEvidenceItem implements FindingEvidenceItem {
  const _FindingEvidenceItem({required this.id, @JsonKey(name: 'finding_id') required this.findingId, @JsonKey(name: 'mention_id') required this.mentionId, @JsonKey(name: 'evidence_type') this.evidenceType = 'review', this.snippet, @JsonKey(name: 'relevance_score') this.relevanceScore = 1.0, @JsonKey(name: 'created_at') required this.createdAt});
  factory _FindingEvidenceItem.fromJson(Map<String, dynamic> json) => _$FindingEvidenceItemFromJson(json);

@override final  String id;
@override@JsonKey(name: 'finding_id') final  String findingId;
@override@JsonKey(name: 'mention_id') final  String mentionId;
@override@JsonKey(name: 'evidence_type') final  String evidenceType;
@override final  String? snippet;
@override@JsonKey(name: 'relevance_score') final  double relevanceScore;
@override@JsonKey(name: 'created_at') final  DateTime createdAt;

/// Create a copy of FindingEvidenceItem
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$FindingEvidenceItemCopyWith<_FindingEvidenceItem> get copyWith => __$FindingEvidenceItemCopyWithImpl<_FindingEvidenceItem>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$FindingEvidenceItemToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _FindingEvidenceItem&&(identical(other.id, id) || other.id == id)&&(identical(other.findingId, findingId) || other.findingId == findingId)&&(identical(other.mentionId, mentionId) || other.mentionId == mentionId)&&(identical(other.evidenceType, evidenceType) || other.evidenceType == evidenceType)&&(identical(other.snippet, snippet) || other.snippet == snippet)&&(identical(other.relevanceScore, relevanceScore) || other.relevanceScore == relevanceScore)&&(identical(other.createdAt, createdAt) || other.createdAt == createdAt));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,findingId,mentionId,evidenceType,snippet,relevanceScore,createdAt);

@override
String toString() {
  return 'FindingEvidenceItem(id: $id, findingId: $findingId, mentionId: $mentionId, evidenceType: $evidenceType, snippet: $snippet, relevanceScore: $relevanceScore, createdAt: $createdAt)';
}


}

/// @nodoc
abstract mixin class _$FindingEvidenceItemCopyWith<$Res> implements $FindingEvidenceItemCopyWith<$Res> {
  factory _$FindingEvidenceItemCopyWith(_FindingEvidenceItem value, $Res Function(_FindingEvidenceItem) _then) = __$FindingEvidenceItemCopyWithImpl;
@override @useResult
$Res call({
 String id,@JsonKey(name: 'finding_id') String findingId,@JsonKey(name: 'mention_id') String mentionId,@JsonKey(name: 'evidence_type') String evidenceType, String? snippet,@JsonKey(name: 'relevance_score') double relevanceScore,@JsonKey(name: 'created_at') DateTime createdAt
});




}
/// @nodoc
class __$FindingEvidenceItemCopyWithImpl<$Res>
    implements _$FindingEvidenceItemCopyWith<$Res> {
  __$FindingEvidenceItemCopyWithImpl(this._self, this._then);

  final _FindingEvidenceItem _self;
  final $Res Function(_FindingEvidenceItem) _then;

/// Create a copy of FindingEvidenceItem
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? findingId = null,Object? mentionId = null,Object? evidenceType = null,Object? snippet = freezed,Object? relevanceScore = null,Object? createdAt = null,}) {
  return _then(_FindingEvidenceItem(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,findingId: null == findingId ? _self.findingId : findingId // ignore: cast_nullable_to_non_nullable
as String,mentionId: null == mentionId ? _self.mentionId : mentionId // ignore: cast_nullable_to_non_nullable
as String,evidenceType: null == evidenceType ? _self.evidenceType : evidenceType // ignore: cast_nullable_to_non_nullable
as String,snippet: freezed == snippet ? _self.snippet : snippet // ignore: cast_nullable_to_non_nullable
as String?,relevanceScore: null == relevanceScore ? _self.relevanceScore : relevanceScore // ignore: cast_nullable_to_non_nullable
as double,createdAt: null == createdAt ? _self.createdAt : createdAt // ignore: cast_nullable_to_non_nullable
as DateTime,
  ));
}


}


/// @nodoc
mixin _$FindingItem {

 String get id;@JsonKey(name: 'business_id') String get businessId;@JsonKey(name: 'finding_type') String get findingType; String get severity; double get confidence; double get score; String get title; String get description;@JsonKey(name: 'detected_at') DateTime get detectedAt;@JsonKey(name: 'first_seen_at') DateTime get firstSeenAt;@JsonKey(name: 'last_seen_at') DateTime get lastSeenAt;@JsonKey(name: 'metadata_json') Map<String, dynamic> get metadataJson; List<FindingEvidenceItem> get evidence;
/// Create a copy of FindingItem
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$FindingItemCopyWith<FindingItem> get copyWith => _$FindingItemCopyWithImpl<FindingItem>(this as FindingItem, _$identity);

  /// Serializes this FindingItem to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is FindingItem&&(identical(other.id, id) || other.id == id)&&(identical(other.businessId, businessId) || other.businessId == businessId)&&(identical(other.findingType, findingType) || other.findingType == findingType)&&(identical(other.severity, severity) || other.severity == severity)&&(identical(other.confidence, confidence) || other.confidence == confidence)&&(identical(other.score, score) || other.score == score)&&(identical(other.title, title) || other.title == title)&&(identical(other.description, description) || other.description == description)&&(identical(other.detectedAt, detectedAt) || other.detectedAt == detectedAt)&&(identical(other.firstSeenAt, firstSeenAt) || other.firstSeenAt == firstSeenAt)&&(identical(other.lastSeenAt, lastSeenAt) || other.lastSeenAt == lastSeenAt)&&const DeepCollectionEquality().equals(other.metadataJson, metadataJson)&&const DeepCollectionEquality().equals(other.evidence, evidence));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,businessId,findingType,severity,confidence,score,title,description,detectedAt,firstSeenAt,lastSeenAt,const DeepCollectionEquality().hash(metadataJson),const DeepCollectionEquality().hash(evidence));

@override
String toString() {
  return 'FindingItem(id: $id, businessId: $businessId, findingType: $findingType, severity: $severity, confidence: $confidence, score: $score, title: $title, description: $description, detectedAt: $detectedAt, firstSeenAt: $firstSeenAt, lastSeenAt: $lastSeenAt, metadataJson: $metadataJson, evidence: $evidence)';
}


}

/// @nodoc
abstract mixin class $FindingItemCopyWith<$Res>  {
  factory $FindingItemCopyWith(FindingItem value, $Res Function(FindingItem) _then) = _$FindingItemCopyWithImpl;
@useResult
$Res call({
 String id,@JsonKey(name: 'business_id') String businessId,@JsonKey(name: 'finding_type') String findingType, String severity, double confidence, double score, String title, String description,@JsonKey(name: 'detected_at') DateTime detectedAt,@JsonKey(name: 'first_seen_at') DateTime firstSeenAt,@JsonKey(name: 'last_seen_at') DateTime lastSeenAt,@JsonKey(name: 'metadata_json') Map<String, dynamic> metadataJson, List<FindingEvidenceItem> evidence
});




}
/// @nodoc
class _$FindingItemCopyWithImpl<$Res>
    implements $FindingItemCopyWith<$Res> {
  _$FindingItemCopyWithImpl(this._self, this._then);

  final FindingItem _self;
  final $Res Function(FindingItem) _then;

/// Create a copy of FindingItem
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? businessId = null,Object? findingType = null,Object? severity = null,Object? confidence = null,Object? score = null,Object? title = null,Object? description = null,Object? detectedAt = null,Object? firstSeenAt = null,Object? lastSeenAt = null,Object? metadataJson = null,Object? evidence = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,businessId: null == businessId ? _self.businessId : businessId // ignore: cast_nullable_to_non_nullable
as String,findingType: null == findingType ? _self.findingType : findingType // ignore: cast_nullable_to_non_nullable
as String,severity: null == severity ? _self.severity : severity // ignore: cast_nullable_to_non_nullable
as String,confidence: null == confidence ? _self.confidence : confidence // ignore: cast_nullable_to_non_nullable
as double,score: null == score ? _self.score : score // ignore: cast_nullable_to_non_nullable
as double,title: null == title ? _self.title : title // ignore: cast_nullable_to_non_nullable
as String,description: null == description ? _self.description : description // ignore: cast_nullable_to_non_nullable
as String,detectedAt: null == detectedAt ? _self.detectedAt : detectedAt // ignore: cast_nullable_to_non_nullable
as DateTime,firstSeenAt: null == firstSeenAt ? _self.firstSeenAt : firstSeenAt // ignore: cast_nullable_to_non_nullable
as DateTime,lastSeenAt: null == lastSeenAt ? _self.lastSeenAt : lastSeenAt // ignore: cast_nullable_to_non_nullable
as DateTime,metadataJson: null == metadataJson ? _self.metadataJson : metadataJson // ignore: cast_nullable_to_non_nullable
as Map<String, dynamic>,evidence: null == evidence ? _self.evidence : evidence // ignore: cast_nullable_to_non_nullable
as List<FindingEvidenceItem>,
  ));
}

}


/// Adds pattern-matching-related methods to [FindingItem].
extension FindingItemPatterns on FindingItem {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _FindingItem value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _FindingItem() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _FindingItem value)  $default,){
final _that = this;
switch (_that) {
case _FindingItem():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _FindingItem value)?  $default,){
final _that = this;
switch (_that) {
case _FindingItem() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'business_id')  String businessId, @JsonKey(name: 'finding_type')  String findingType,  String severity,  double confidence,  double score,  String title,  String description, @JsonKey(name: 'detected_at')  DateTime detectedAt, @JsonKey(name: 'first_seen_at')  DateTime firstSeenAt, @JsonKey(name: 'last_seen_at')  DateTime lastSeenAt, @JsonKey(name: 'metadata_json')  Map<String, dynamic> metadataJson,  List<FindingEvidenceItem> evidence)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _FindingItem() when $default != null:
return $default(_that.id,_that.businessId,_that.findingType,_that.severity,_that.confidence,_that.score,_that.title,_that.description,_that.detectedAt,_that.firstSeenAt,_that.lastSeenAt,_that.metadataJson,_that.evidence);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'business_id')  String businessId, @JsonKey(name: 'finding_type')  String findingType,  String severity,  double confidence,  double score,  String title,  String description, @JsonKey(name: 'detected_at')  DateTime detectedAt, @JsonKey(name: 'first_seen_at')  DateTime firstSeenAt, @JsonKey(name: 'last_seen_at')  DateTime lastSeenAt, @JsonKey(name: 'metadata_json')  Map<String, dynamic> metadataJson,  List<FindingEvidenceItem> evidence)  $default,) {final _that = this;
switch (_that) {
case _FindingItem():
return $default(_that.id,_that.businessId,_that.findingType,_that.severity,_that.confidence,_that.score,_that.title,_that.description,_that.detectedAt,_that.firstSeenAt,_that.lastSeenAt,_that.metadataJson,_that.evidence);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id, @JsonKey(name: 'business_id')  String businessId, @JsonKey(name: 'finding_type')  String findingType,  String severity,  double confidence,  double score,  String title,  String description, @JsonKey(name: 'detected_at')  DateTime detectedAt, @JsonKey(name: 'first_seen_at')  DateTime firstSeenAt, @JsonKey(name: 'last_seen_at')  DateTime lastSeenAt, @JsonKey(name: 'metadata_json')  Map<String, dynamic> metadataJson,  List<FindingEvidenceItem> evidence)?  $default,) {final _that = this;
switch (_that) {
case _FindingItem() when $default != null:
return $default(_that.id,_that.businessId,_that.findingType,_that.severity,_that.confidence,_that.score,_that.title,_that.description,_that.detectedAt,_that.firstSeenAt,_that.lastSeenAt,_that.metadataJson,_that.evidence);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _FindingItem implements FindingItem {
  const _FindingItem({required this.id, @JsonKey(name: 'business_id') required this.businessId, @JsonKey(name: 'finding_type') required this.findingType, this.severity = 'medium', this.confidence = 0.8, this.score = 0.0, required this.title, required this.description, @JsonKey(name: 'detected_at') required this.detectedAt, @JsonKey(name: 'first_seen_at') required this.firstSeenAt, @JsonKey(name: 'last_seen_at') required this.lastSeenAt, @JsonKey(name: 'metadata_json') this.metadataJson = const {}, this.evidence = const []});
  factory _FindingItem.fromJson(Map<String, dynamic> json) => _$FindingItemFromJson(json);

@override final  String id;
@override@JsonKey(name: 'business_id') final  String businessId;
@override@JsonKey(name: 'finding_type') final  String findingType;
@override@JsonKey() final  String severity;
@override@JsonKey() final  double confidence;
@override@JsonKey() final  double score;
@override final  String title;
@override final  String description;
@override@JsonKey(name: 'detected_at') final  DateTime detectedAt;
@override@JsonKey(name: 'first_seen_at') final  DateTime firstSeenAt;
@override@JsonKey(name: 'last_seen_at') final  DateTime lastSeenAt;
@override@JsonKey(name: 'metadata_json') final  Map<String, dynamic> metadataJson;
@override@JsonKey() final  List<FindingEvidenceItem> evidence;

/// Create a copy of FindingItem
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$FindingItemCopyWith<_FindingItem> get copyWith => __$FindingItemCopyWithImpl<_FindingItem>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$FindingItemToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _FindingItem&&(identical(other.id, id) || other.id == id)&&(identical(other.businessId, businessId) || other.businessId == businessId)&&(identical(other.findingType, findingType) || other.findingType == findingType)&&(identical(other.severity, severity) || other.severity == severity)&&(identical(other.confidence, confidence) || other.confidence == confidence)&&(identical(other.score, score) || other.score == score)&&(identical(other.title, title) || other.title == title)&&(identical(other.description, description) || other.description == description)&&(identical(other.detectedAt, detectedAt) || other.detectedAt == detectedAt)&&(identical(other.firstSeenAt, firstSeenAt) || other.firstSeenAt == firstSeenAt)&&(identical(other.lastSeenAt, lastSeenAt) || other.lastSeenAt == lastSeenAt)&&const DeepCollectionEquality().equals(other.metadataJson, metadataJson)&&const DeepCollectionEquality().equals(other.evidence, evidence));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,businessId,findingType,severity,confidence,score,title,description,detectedAt,firstSeenAt,lastSeenAt,const DeepCollectionEquality().hash(metadataJson),const DeepCollectionEquality().hash(evidence));

@override
String toString() {
  return 'FindingItem(id: $id, businessId: $businessId, findingType: $findingType, severity: $severity, confidence: $confidence, score: $score, title: $title, description: $description, detectedAt: $detectedAt, firstSeenAt: $firstSeenAt, lastSeenAt: $lastSeenAt, metadataJson: $metadataJson, evidence: $evidence)';
}


}

/// @nodoc
abstract mixin class _$FindingItemCopyWith<$Res> implements $FindingItemCopyWith<$Res> {
  factory _$FindingItemCopyWith(_FindingItem value, $Res Function(_FindingItem) _then) = __$FindingItemCopyWithImpl;
@override @useResult
$Res call({
 String id,@JsonKey(name: 'business_id') String businessId,@JsonKey(name: 'finding_type') String findingType, String severity, double confidence, double score, String title, String description,@JsonKey(name: 'detected_at') DateTime detectedAt,@JsonKey(name: 'first_seen_at') DateTime firstSeenAt,@JsonKey(name: 'last_seen_at') DateTime lastSeenAt,@JsonKey(name: 'metadata_json') Map<String, dynamic> metadataJson, List<FindingEvidenceItem> evidence
});




}
/// @nodoc
class __$FindingItemCopyWithImpl<$Res>
    implements _$FindingItemCopyWith<$Res> {
  __$FindingItemCopyWithImpl(this._self, this._then);

  final _FindingItem _self;
  final $Res Function(_FindingItem) _then;

/// Create a copy of FindingItem
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? businessId = null,Object? findingType = null,Object? severity = null,Object? confidence = null,Object? score = null,Object? title = null,Object? description = null,Object? detectedAt = null,Object? firstSeenAt = null,Object? lastSeenAt = null,Object? metadataJson = null,Object? evidence = null,}) {
  return _then(_FindingItem(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,businessId: null == businessId ? _self.businessId : businessId // ignore: cast_nullable_to_non_nullable
as String,findingType: null == findingType ? _self.findingType : findingType // ignore: cast_nullable_to_non_nullable
as String,severity: null == severity ? _self.severity : severity // ignore: cast_nullable_to_non_nullable
as String,confidence: null == confidence ? _self.confidence : confidence // ignore: cast_nullable_to_non_nullable
as double,score: null == score ? _self.score : score // ignore: cast_nullable_to_non_nullable
as double,title: null == title ? _self.title : title // ignore: cast_nullable_to_non_nullable
as String,description: null == description ? _self.description : description // ignore: cast_nullable_to_non_nullable
as String,detectedAt: null == detectedAt ? _self.detectedAt : detectedAt // ignore: cast_nullable_to_non_nullable
as DateTime,firstSeenAt: null == firstSeenAt ? _self.firstSeenAt : firstSeenAt // ignore: cast_nullable_to_non_nullable
as DateTime,lastSeenAt: null == lastSeenAt ? _self.lastSeenAt : lastSeenAt // ignore: cast_nullable_to_non_nullable
as DateTime,metadataJson: null == metadataJson ? _self.metadataJson : metadataJson // ignore: cast_nullable_to_non_nullable
as Map<String, dynamic>,evidence: null == evidence ? _self.evidence : evidence // ignore: cast_nullable_to_non_nullable
as List<FindingEvidenceItem>,
  ));
}


}

// dart format on
