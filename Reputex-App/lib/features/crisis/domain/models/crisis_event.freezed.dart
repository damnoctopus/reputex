// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'crisis_event.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$CrisisEvent {

 String get id; String get title; String get severity; String get status;@JsonKey(name: 'trigger_reason') String get triggerReason; double get velocity;@JsonKey(name: 'negative_mentions_count') int get negativeMentionsCount;@JsonKey(name: 'affected_platforms') List<String> get affectedPlatforms;@JsonKey(name: 'started_at') DateTime get startedAt;@JsonKey(name: 'resolved_at') DateTime? get resolvedAt;@JsonKey(name: 'suggested_actions') List<String> get suggestedActions;@JsonKey(name: 'estimated_reach') int get estimatedReach;@JsonKey(name: 'peak_volume_per_hour') int get peakVolumePerHour;
/// Create a copy of CrisisEvent
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$CrisisEventCopyWith<CrisisEvent> get copyWith => _$CrisisEventCopyWithImpl<CrisisEvent>(this as CrisisEvent, _$identity);

  /// Serializes this CrisisEvent to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is CrisisEvent&&(identical(other.id, id) || other.id == id)&&(identical(other.title, title) || other.title == title)&&(identical(other.severity, severity) || other.severity == severity)&&(identical(other.status, status) || other.status == status)&&(identical(other.triggerReason, triggerReason) || other.triggerReason == triggerReason)&&(identical(other.velocity, velocity) || other.velocity == velocity)&&(identical(other.negativeMentionsCount, negativeMentionsCount) || other.negativeMentionsCount == negativeMentionsCount)&&const DeepCollectionEquality().equals(other.affectedPlatforms, affectedPlatforms)&&(identical(other.startedAt, startedAt) || other.startedAt == startedAt)&&(identical(other.resolvedAt, resolvedAt) || other.resolvedAt == resolvedAt)&&const DeepCollectionEquality().equals(other.suggestedActions, suggestedActions)&&(identical(other.estimatedReach, estimatedReach) || other.estimatedReach == estimatedReach)&&(identical(other.peakVolumePerHour, peakVolumePerHour) || other.peakVolumePerHour == peakVolumePerHour));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,title,severity,status,triggerReason,velocity,negativeMentionsCount,const DeepCollectionEquality().hash(affectedPlatforms),startedAt,resolvedAt,const DeepCollectionEquality().hash(suggestedActions),estimatedReach,peakVolumePerHour);

@override
String toString() {
  return 'CrisisEvent(id: $id, title: $title, severity: $severity, status: $status, triggerReason: $triggerReason, velocity: $velocity, negativeMentionsCount: $negativeMentionsCount, affectedPlatforms: $affectedPlatforms, startedAt: $startedAt, resolvedAt: $resolvedAt, suggestedActions: $suggestedActions, estimatedReach: $estimatedReach, peakVolumePerHour: $peakVolumePerHour)';
}


}

/// @nodoc
abstract mixin class $CrisisEventCopyWith<$Res>  {
  factory $CrisisEventCopyWith(CrisisEvent value, $Res Function(CrisisEvent) _then) = _$CrisisEventCopyWithImpl;
@useResult
$Res call({
 String id, String title, String severity, String status,@JsonKey(name: 'trigger_reason') String triggerReason, double velocity,@JsonKey(name: 'negative_mentions_count') int negativeMentionsCount,@JsonKey(name: 'affected_platforms') List<String> affectedPlatforms,@JsonKey(name: 'started_at') DateTime startedAt,@JsonKey(name: 'resolved_at') DateTime? resolvedAt,@JsonKey(name: 'suggested_actions') List<String> suggestedActions,@JsonKey(name: 'estimated_reach') int estimatedReach,@JsonKey(name: 'peak_volume_per_hour') int peakVolumePerHour
});




}
/// @nodoc
class _$CrisisEventCopyWithImpl<$Res>
    implements $CrisisEventCopyWith<$Res> {
  _$CrisisEventCopyWithImpl(this._self, this._then);

  final CrisisEvent _self;
  final $Res Function(CrisisEvent) _then;

/// Create a copy of CrisisEvent
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? title = null,Object? severity = null,Object? status = null,Object? triggerReason = null,Object? velocity = null,Object? negativeMentionsCount = null,Object? affectedPlatforms = null,Object? startedAt = null,Object? resolvedAt = freezed,Object? suggestedActions = null,Object? estimatedReach = null,Object? peakVolumePerHour = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,title: null == title ? _self.title : title // ignore: cast_nullable_to_non_nullable
as String,severity: null == severity ? _self.severity : severity // ignore: cast_nullable_to_non_nullable
as String,status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,triggerReason: null == triggerReason ? _self.triggerReason : triggerReason // ignore: cast_nullable_to_non_nullable
as String,velocity: null == velocity ? _self.velocity : velocity // ignore: cast_nullable_to_non_nullable
as double,negativeMentionsCount: null == negativeMentionsCount ? _self.negativeMentionsCount : negativeMentionsCount // ignore: cast_nullable_to_non_nullable
as int,affectedPlatforms: null == affectedPlatforms ? _self.affectedPlatforms : affectedPlatforms // ignore: cast_nullable_to_non_nullable
as List<String>,startedAt: null == startedAt ? _self.startedAt : startedAt // ignore: cast_nullable_to_non_nullable
as DateTime,resolvedAt: freezed == resolvedAt ? _self.resolvedAt : resolvedAt // ignore: cast_nullable_to_non_nullable
as DateTime?,suggestedActions: null == suggestedActions ? _self.suggestedActions : suggestedActions // ignore: cast_nullable_to_non_nullable
as List<String>,estimatedReach: null == estimatedReach ? _self.estimatedReach : estimatedReach // ignore: cast_nullable_to_non_nullable
as int,peakVolumePerHour: null == peakVolumePerHour ? _self.peakVolumePerHour : peakVolumePerHour // ignore: cast_nullable_to_non_nullable
as int,
  ));
}

}


/// Adds pattern-matching-related methods to [CrisisEvent].
extension CrisisEventPatterns on CrisisEvent {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _CrisisEvent value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _CrisisEvent() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _CrisisEvent value)  $default,){
final _that = this;
switch (_that) {
case _CrisisEvent():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _CrisisEvent value)?  $default,){
final _that = this;
switch (_that) {
case _CrisisEvent() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String title,  String severity,  String status, @JsonKey(name: 'trigger_reason')  String triggerReason,  double velocity, @JsonKey(name: 'negative_mentions_count')  int negativeMentionsCount, @JsonKey(name: 'affected_platforms')  List<String> affectedPlatforms, @JsonKey(name: 'started_at')  DateTime startedAt, @JsonKey(name: 'resolved_at')  DateTime? resolvedAt, @JsonKey(name: 'suggested_actions')  List<String> suggestedActions, @JsonKey(name: 'estimated_reach')  int estimatedReach, @JsonKey(name: 'peak_volume_per_hour')  int peakVolumePerHour)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _CrisisEvent() when $default != null:
return $default(_that.id,_that.title,_that.severity,_that.status,_that.triggerReason,_that.velocity,_that.negativeMentionsCount,_that.affectedPlatforms,_that.startedAt,_that.resolvedAt,_that.suggestedActions,_that.estimatedReach,_that.peakVolumePerHour);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String title,  String severity,  String status, @JsonKey(name: 'trigger_reason')  String triggerReason,  double velocity, @JsonKey(name: 'negative_mentions_count')  int negativeMentionsCount, @JsonKey(name: 'affected_platforms')  List<String> affectedPlatforms, @JsonKey(name: 'started_at')  DateTime startedAt, @JsonKey(name: 'resolved_at')  DateTime? resolvedAt, @JsonKey(name: 'suggested_actions')  List<String> suggestedActions, @JsonKey(name: 'estimated_reach')  int estimatedReach, @JsonKey(name: 'peak_volume_per_hour')  int peakVolumePerHour)  $default,) {final _that = this;
switch (_that) {
case _CrisisEvent():
return $default(_that.id,_that.title,_that.severity,_that.status,_that.triggerReason,_that.velocity,_that.negativeMentionsCount,_that.affectedPlatforms,_that.startedAt,_that.resolvedAt,_that.suggestedActions,_that.estimatedReach,_that.peakVolumePerHour);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String title,  String severity,  String status, @JsonKey(name: 'trigger_reason')  String triggerReason,  double velocity, @JsonKey(name: 'negative_mentions_count')  int negativeMentionsCount, @JsonKey(name: 'affected_platforms')  List<String> affectedPlatforms, @JsonKey(name: 'started_at')  DateTime startedAt, @JsonKey(name: 'resolved_at')  DateTime? resolvedAt, @JsonKey(name: 'suggested_actions')  List<String> suggestedActions, @JsonKey(name: 'estimated_reach')  int estimatedReach, @JsonKey(name: 'peak_volume_per_hour')  int peakVolumePerHour)?  $default,) {final _that = this;
switch (_that) {
case _CrisisEvent() when $default != null:
return $default(_that.id,_that.title,_that.severity,_that.status,_that.triggerReason,_that.velocity,_that.negativeMentionsCount,_that.affectedPlatforms,_that.startedAt,_that.resolvedAt,_that.suggestedActions,_that.estimatedReach,_that.peakVolumePerHour);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _CrisisEvent implements CrisisEvent {
  const _CrisisEvent({required this.id, required this.title, required this.severity, this.status = 'active', @JsonKey(name: 'trigger_reason') required this.triggerReason, this.velocity = 0.0, @JsonKey(name: 'negative_mentions_count') this.negativeMentionsCount = 0, @JsonKey(name: 'affected_platforms') this.affectedPlatforms = const [], @JsonKey(name: 'started_at') required this.startedAt, @JsonKey(name: 'resolved_at') this.resolvedAt, @JsonKey(name: 'suggested_actions') this.suggestedActions = const [], @JsonKey(name: 'estimated_reach') this.estimatedReach = 0, @JsonKey(name: 'peak_volume_per_hour') this.peakVolumePerHour = 0});
  factory _CrisisEvent.fromJson(Map<String, dynamic> json) => _$CrisisEventFromJson(json);

@override final  String id;
@override final  String title;
@override final  String severity;
@override@JsonKey() final  String status;
@override@JsonKey(name: 'trigger_reason') final  String triggerReason;
@override@JsonKey() final  double velocity;
@override@JsonKey(name: 'negative_mentions_count') final  int negativeMentionsCount;
@override@JsonKey(name: 'affected_platforms') final  List<String> affectedPlatforms;
@override@JsonKey(name: 'started_at') final  DateTime startedAt;
@override@JsonKey(name: 'resolved_at') final  DateTime? resolvedAt;
@override@JsonKey(name: 'suggested_actions') final  List<String> suggestedActions;
@override@JsonKey(name: 'estimated_reach') final  int estimatedReach;
@override@JsonKey(name: 'peak_volume_per_hour') final  int peakVolumePerHour;

/// Create a copy of CrisisEvent
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$CrisisEventCopyWith<_CrisisEvent> get copyWith => __$CrisisEventCopyWithImpl<_CrisisEvent>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$CrisisEventToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _CrisisEvent&&(identical(other.id, id) || other.id == id)&&(identical(other.title, title) || other.title == title)&&(identical(other.severity, severity) || other.severity == severity)&&(identical(other.status, status) || other.status == status)&&(identical(other.triggerReason, triggerReason) || other.triggerReason == triggerReason)&&(identical(other.velocity, velocity) || other.velocity == velocity)&&(identical(other.negativeMentionsCount, negativeMentionsCount) || other.negativeMentionsCount == negativeMentionsCount)&&const DeepCollectionEquality().equals(other.affectedPlatforms, affectedPlatforms)&&(identical(other.startedAt, startedAt) || other.startedAt == startedAt)&&(identical(other.resolvedAt, resolvedAt) || other.resolvedAt == resolvedAt)&&const DeepCollectionEquality().equals(other.suggestedActions, suggestedActions)&&(identical(other.estimatedReach, estimatedReach) || other.estimatedReach == estimatedReach)&&(identical(other.peakVolumePerHour, peakVolumePerHour) || other.peakVolumePerHour == peakVolumePerHour));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,title,severity,status,triggerReason,velocity,negativeMentionsCount,const DeepCollectionEquality().hash(affectedPlatforms),startedAt,resolvedAt,const DeepCollectionEquality().hash(suggestedActions),estimatedReach,peakVolumePerHour);

@override
String toString() {
  return 'CrisisEvent(id: $id, title: $title, severity: $severity, status: $status, triggerReason: $triggerReason, velocity: $velocity, negativeMentionsCount: $negativeMentionsCount, affectedPlatforms: $affectedPlatforms, startedAt: $startedAt, resolvedAt: $resolvedAt, suggestedActions: $suggestedActions, estimatedReach: $estimatedReach, peakVolumePerHour: $peakVolumePerHour)';
}


}

/// @nodoc
abstract mixin class _$CrisisEventCopyWith<$Res> implements $CrisisEventCopyWith<$Res> {
  factory _$CrisisEventCopyWith(_CrisisEvent value, $Res Function(_CrisisEvent) _then) = __$CrisisEventCopyWithImpl;
@override @useResult
$Res call({
 String id, String title, String severity, String status,@JsonKey(name: 'trigger_reason') String triggerReason, double velocity,@JsonKey(name: 'negative_mentions_count') int negativeMentionsCount,@JsonKey(name: 'affected_platforms') List<String> affectedPlatforms,@JsonKey(name: 'started_at') DateTime startedAt,@JsonKey(name: 'resolved_at') DateTime? resolvedAt,@JsonKey(name: 'suggested_actions') List<String> suggestedActions,@JsonKey(name: 'estimated_reach') int estimatedReach,@JsonKey(name: 'peak_volume_per_hour') int peakVolumePerHour
});




}
/// @nodoc
class __$CrisisEventCopyWithImpl<$Res>
    implements _$CrisisEventCopyWith<$Res> {
  __$CrisisEventCopyWithImpl(this._self, this._then);

  final _CrisisEvent _self;
  final $Res Function(_CrisisEvent) _then;

/// Create a copy of CrisisEvent
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? title = null,Object? severity = null,Object? status = null,Object? triggerReason = null,Object? velocity = null,Object? negativeMentionsCount = null,Object? affectedPlatforms = null,Object? startedAt = null,Object? resolvedAt = freezed,Object? suggestedActions = null,Object? estimatedReach = null,Object? peakVolumePerHour = null,}) {
  return _then(_CrisisEvent(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,title: null == title ? _self.title : title // ignore: cast_nullable_to_non_nullable
as String,severity: null == severity ? _self.severity : severity // ignore: cast_nullable_to_non_nullable
as String,status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,triggerReason: null == triggerReason ? _self.triggerReason : triggerReason // ignore: cast_nullable_to_non_nullable
as String,velocity: null == velocity ? _self.velocity : velocity // ignore: cast_nullable_to_non_nullable
as double,negativeMentionsCount: null == negativeMentionsCount ? _self.negativeMentionsCount : negativeMentionsCount // ignore: cast_nullable_to_non_nullable
as int,affectedPlatforms: null == affectedPlatforms ? _self.affectedPlatforms : affectedPlatforms // ignore: cast_nullable_to_non_nullable
as List<String>,startedAt: null == startedAt ? _self.startedAt : startedAt // ignore: cast_nullable_to_non_nullable
as DateTime,resolvedAt: freezed == resolvedAt ? _self.resolvedAt : resolvedAt // ignore: cast_nullable_to_non_nullable
as DateTime?,suggestedActions: null == suggestedActions ? _self.suggestedActions : suggestedActions // ignore: cast_nullable_to_non_nullable
as List<String>,estimatedReach: null == estimatedReach ? _self.estimatedReach : estimatedReach // ignore: cast_nullable_to_non_nullable
as int,peakVolumePerHour: null == peakVolumePerHour ? _self.peakVolumePerHour : peakVolumePerHour // ignore: cast_nullable_to_non_nullable
as int,
  ));
}


}

// dart format on
