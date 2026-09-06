// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'response_draft.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$ResponseDraft {

 String get id;@JsonKey(name: 'mention_id') String get mentionId;@JsonKey(name: 'original_review') String get originalReview;@JsonKey(name: 'generated_response') String get generatedResponse; String get tone; String get status;@JsonKey(name: 'created_at') DateTime get createdAt;@JsonKey(name: 'approved_at') DateTime? get approvedAt;@JsonKey(name: 'dispatched_at') DateTime? get dispatchedAt;
/// Create a copy of ResponseDraft
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$ResponseDraftCopyWith<ResponseDraft> get copyWith => _$ResponseDraftCopyWithImpl<ResponseDraft>(this as ResponseDraft, _$identity);

  /// Serializes this ResponseDraft to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is ResponseDraft&&(identical(other.id, id) || other.id == id)&&(identical(other.mentionId, mentionId) || other.mentionId == mentionId)&&(identical(other.originalReview, originalReview) || other.originalReview == originalReview)&&(identical(other.generatedResponse, generatedResponse) || other.generatedResponse == generatedResponse)&&(identical(other.tone, tone) || other.tone == tone)&&(identical(other.status, status) || other.status == status)&&(identical(other.createdAt, createdAt) || other.createdAt == createdAt)&&(identical(other.approvedAt, approvedAt) || other.approvedAt == approvedAt)&&(identical(other.dispatchedAt, dispatchedAt) || other.dispatchedAt == dispatchedAt));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,mentionId,originalReview,generatedResponse,tone,status,createdAt,approvedAt,dispatchedAt);

@override
String toString() {
  return 'ResponseDraft(id: $id, mentionId: $mentionId, originalReview: $originalReview, generatedResponse: $generatedResponse, tone: $tone, status: $status, createdAt: $createdAt, approvedAt: $approvedAt, dispatchedAt: $dispatchedAt)';
}


}

/// @nodoc
abstract mixin class $ResponseDraftCopyWith<$Res>  {
  factory $ResponseDraftCopyWith(ResponseDraft value, $Res Function(ResponseDraft) _then) = _$ResponseDraftCopyWithImpl;
@useResult
$Res call({
 String id,@JsonKey(name: 'mention_id') String mentionId,@JsonKey(name: 'original_review') String originalReview,@JsonKey(name: 'generated_response') String generatedResponse, String tone, String status,@JsonKey(name: 'created_at') DateTime createdAt,@JsonKey(name: 'approved_at') DateTime? approvedAt,@JsonKey(name: 'dispatched_at') DateTime? dispatchedAt
});




}
/// @nodoc
class _$ResponseDraftCopyWithImpl<$Res>
    implements $ResponseDraftCopyWith<$Res> {
  _$ResponseDraftCopyWithImpl(this._self, this._then);

  final ResponseDraft _self;
  final $Res Function(ResponseDraft) _then;

/// Create a copy of ResponseDraft
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? mentionId = null,Object? originalReview = null,Object? generatedResponse = null,Object? tone = null,Object? status = null,Object? createdAt = null,Object? approvedAt = freezed,Object? dispatchedAt = freezed,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,mentionId: null == mentionId ? _self.mentionId : mentionId // ignore: cast_nullable_to_non_nullable
as String,originalReview: null == originalReview ? _self.originalReview : originalReview // ignore: cast_nullable_to_non_nullable
as String,generatedResponse: null == generatedResponse ? _self.generatedResponse : generatedResponse // ignore: cast_nullable_to_non_nullable
as String,tone: null == tone ? _self.tone : tone // ignore: cast_nullable_to_non_nullable
as String,status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,createdAt: null == createdAt ? _self.createdAt : createdAt // ignore: cast_nullable_to_non_nullable
as DateTime,approvedAt: freezed == approvedAt ? _self.approvedAt : approvedAt // ignore: cast_nullable_to_non_nullable
as DateTime?,dispatchedAt: freezed == dispatchedAt ? _self.dispatchedAt : dispatchedAt // ignore: cast_nullable_to_non_nullable
as DateTime?,
  ));
}

}


/// Adds pattern-matching-related methods to [ResponseDraft].
extension ResponseDraftPatterns on ResponseDraft {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _ResponseDraft value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _ResponseDraft() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _ResponseDraft value)  $default,){
final _that = this;
switch (_that) {
case _ResponseDraft():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _ResponseDraft value)?  $default,){
final _that = this;
switch (_that) {
case _ResponseDraft() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'mention_id')  String mentionId, @JsonKey(name: 'original_review')  String originalReview, @JsonKey(name: 'generated_response')  String generatedResponse,  String tone,  String status, @JsonKey(name: 'created_at')  DateTime createdAt, @JsonKey(name: 'approved_at')  DateTime? approvedAt, @JsonKey(name: 'dispatched_at')  DateTime? dispatchedAt)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _ResponseDraft() when $default != null:
return $default(_that.id,_that.mentionId,_that.originalReview,_that.generatedResponse,_that.tone,_that.status,_that.createdAt,_that.approvedAt,_that.dispatchedAt);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'mention_id')  String mentionId, @JsonKey(name: 'original_review')  String originalReview, @JsonKey(name: 'generated_response')  String generatedResponse,  String tone,  String status, @JsonKey(name: 'created_at')  DateTime createdAt, @JsonKey(name: 'approved_at')  DateTime? approvedAt, @JsonKey(name: 'dispatched_at')  DateTime? dispatchedAt)  $default,) {final _that = this;
switch (_that) {
case _ResponseDraft():
return $default(_that.id,_that.mentionId,_that.originalReview,_that.generatedResponse,_that.tone,_that.status,_that.createdAt,_that.approvedAt,_that.dispatchedAt);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id, @JsonKey(name: 'mention_id')  String mentionId, @JsonKey(name: 'original_review')  String originalReview, @JsonKey(name: 'generated_response')  String generatedResponse,  String tone,  String status, @JsonKey(name: 'created_at')  DateTime createdAt, @JsonKey(name: 'approved_at')  DateTime? approvedAt, @JsonKey(name: 'dispatched_at')  DateTime? dispatchedAt)?  $default,) {final _that = this;
switch (_that) {
case _ResponseDraft() when $default != null:
return $default(_that.id,_that.mentionId,_that.originalReview,_that.generatedResponse,_that.tone,_that.status,_that.createdAt,_that.approvedAt,_that.dispatchedAt);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _ResponseDraft implements ResponseDraft {
  const _ResponseDraft({required this.id, @JsonKey(name: 'mention_id') required this.mentionId, @JsonKey(name: 'original_review') required this.originalReview, @JsonKey(name: 'generated_response') required this.generatedResponse, this.tone = 'empathetic', this.status = 'drafted', @JsonKey(name: 'created_at') required this.createdAt, @JsonKey(name: 'approved_at') this.approvedAt, @JsonKey(name: 'dispatched_at') this.dispatchedAt});
  factory _ResponseDraft.fromJson(Map<String, dynamic> json) => _$ResponseDraftFromJson(json);

@override final  String id;
@override@JsonKey(name: 'mention_id') final  String mentionId;
@override@JsonKey(name: 'original_review') final  String originalReview;
@override@JsonKey(name: 'generated_response') final  String generatedResponse;
@override@JsonKey() final  String tone;
@override@JsonKey() final  String status;
@override@JsonKey(name: 'created_at') final  DateTime createdAt;
@override@JsonKey(name: 'approved_at') final  DateTime? approvedAt;
@override@JsonKey(name: 'dispatched_at') final  DateTime? dispatchedAt;

/// Create a copy of ResponseDraft
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$ResponseDraftCopyWith<_ResponseDraft> get copyWith => __$ResponseDraftCopyWithImpl<_ResponseDraft>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$ResponseDraftToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _ResponseDraft&&(identical(other.id, id) || other.id == id)&&(identical(other.mentionId, mentionId) || other.mentionId == mentionId)&&(identical(other.originalReview, originalReview) || other.originalReview == originalReview)&&(identical(other.generatedResponse, generatedResponse) || other.generatedResponse == generatedResponse)&&(identical(other.tone, tone) || other.tone == tone)&&(identical(other.status, status) || other.status == status)&&(identical(other.createdAt, createdAt) || other.createdAt == createdAt)&&(identical(other.approvedAt, approvedAt) || other.approvedAt == approvedAt)&&(identical(other.dispatchedAt, dispatchedAt) || other.dispatchedAt == dispatchedAt));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,mentionId,originalReview,generatedResponse,tone,status,createdAt,approvedAt,dispatchedAt);

@override
String toString() {
  return 'ResponseDraft(id: $id, mentionId: $mentionId, originalReview: $originalReview, generatedResponse: $generatedResponse, tone: $tone, status: $status, createdAt: $createdAt, approvedAt: $approvedAt, dispatchedAt: $dispatchedAt)';
}


}

/// @nodoc
abstract mixin class _$ResponseDraftCopyWith<$Res> implements $ResponseDraftCopyWith<$Res> {
  factory _$ResponseDraftCopyWith(_ResponseDraft value, $Res Function(_ResponseDraft) _then) = __$ResponseDraftCopyWithImpl;
@override @useResult
$Res call({
 String id,@JsonKey(name: 'mention_id') String mentionId,@JsonKey(name: 'original_review') String originalReview,@JsonKey(name: 'generated_response') String generatedResponse, String tone, String status,@JsonKey(name: 'created_at') DateTime createdAt,@JsonKey(name: 'approved_at') DateTime? approvedAt,@JsonKey(name: 'dispatched_at') DateTime? dispatchedAt
});




}
/// @nodoc
class __$ResponseDraftCopyWithImpl<$Res>
    implements _$ResponseDraftCopyWith<$Res> {
  __$ResponseDraftCopyWithImpl(this._self, this._then);

  final _ResponseDraft _self;
  final $Res Function(_ResponseDraft) _then;

/// Create a copy of ResponseDraft
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? mentionId = null,Object? originalReview = null,Object? generatedResponse = null,Object? tone = null,Object? status = null,Object? createdAt = null,Object? approvedAt = freezed,Object? dispatchedAt = freezed,}) {
  return _then(_ResponseDraft(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,mentionId: null == mentionId ? _self.mentionId : mentionId // ignore: cast_nullable_to_non_nullable
as String,originalReview: null == originalReview ? _self.originalReview : originalReview // ignore: cast_nullable_to_non_nullable
as String,generatedResponse: null == generatedResponse ? _self.generatedResponse : generatedResponse // ignore: cast_nullable_to_non_nullable
as String,tone: null == tone ? _self.tone : tone // ignore: cast_nullable_to_non_nullable
as String,status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,createdAt: null == createdAt ? _self.createdAt : createdAt // ignore: cast_nullable_to_non_nullable
as DateTime,approvedAt: freezed == approvedAt ? _self.approvedAt : approvedAt // ignore: cast_nullable_to_non_nullable
as DateTime?,dispatchedAt: freezed == dispatchedAt ? _self.dispatchedAt : dispatchedAt // ignore: cast_nullable_to_non_nullable
as DateTime?,
  ));
}


}

// dart format on
