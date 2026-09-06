// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'alert_item.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$AlertItem {

 String get id; String get type; String get title; String get message; String get severity; DateTime get timestamp;@JsonKey(name: 'is_read') bool get isRead;@JsonKey(name: 'reference_id') String? get referenceId;@JsonKey(name: 'reference_type') String? get referenceType;
/// Create a copy of AlertItem
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$AlertItemCopyWith<AlertItem> get copyWith => _$AlertItemCopyWithImpl<AlertItem>(this as AlertItem, _$identity);

  /// Serializes this AlertItem to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is AlertItem&&(identical(other.id, id) || other.id == id)&&(identical(other.type, type) || other.type == type)&&(identical(other.title, title) || other.title == title)&&(identical(other.message, message) || other.message == message)&&(identical(other.severity, severity) || other.severity == severity)&&(identical(other.timestamp, timestamp) || other.timestamp == timestamp)&&(identical(other.isRead, isRead) || other.isRead == isRead)&&(identical(other.referenceId, referenceId) || other.referenceId == referenceId)&&(identical(other.referenceType, referenceType) || other.referenceType == referenceType));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,type,title,message,severity,timestamp,isRead,referenceId,referenceType);

@override
String toString() {
  return 'AlertItem(id: $id, type: $type, title: $title, message: $message, severity: $severity, timestamp: $timestamp, isRead: $isRead, referenceId: $referenceId, referenceType: $referenceType)';
}


}

/// @nodoc
abstract mixin class $AlertItemCopyWith<$Res>  {
  factory $AlertItemCopyWith(AlertItem value, $Res Function(AlertItem) _then) = _$AlertItemCopyWithImpl;
@useResult
$Res call({
 String id, String type, String title, String message, String severity, DateTime timestamp,@JsonKey(name: 'is_read') bool isRead,@JsonKey(name: 'reference_id') String? referenceId,@JsonKey(name: 'reference_type') String? referenceType
});




}
/// @nodoc
class _$AlertItemCopyWithImpl<$Res>
    implements $AlertItemCopyWith<$Res> {
  _$AlertItemCopyWithImpl(this._self, this._then);

  final AlertItem _self;
  final $Res Function(AlertItem) _then;

/// Create a copy of AlertItem
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? type = null,Object? title = null,Object? message = null,Object? severity = null,Object? timestamp = null,Object? isRead = null,Object? referenceId = freezed,Object? referenceType = freezed,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,type: null == type ? _self.type : type // ignore: cast_nullable_to_non_nullable
as String,title: null == title ? _self.title : title // ignore: cast_nullable_to_non_nullable
as String,message: null == message ? _self.message : message // ignore: cast_nullable_to_non_nullable
as String,severity: null == severity ? _self.severity : severity // ignore: cast_nullable_to_non_nullable
as String,timestamp: null == timestamp ? _self.timestamp : timestamp // ignore: cast_nullable_to_non_nullable
as DateTime,isRead: null == isRead ? _self.isRead : isRead // ignore: cast_nullable_to_non_nullable
as bool,referenceId: freezed == referenceId ? _self.referenceId : referenceId // ignore: cast_nullable_to_non_nullable
as String?,referenceType: freezed == referenceType ? _self.referenceType : referenceType // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}

}


/// Adds pattern-matching-related methods to [AlertItem].
extension AlertItemPatterns on AlertItem {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _AlertItem value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _AlertItem() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _AlertItem value)  $default,){
final _that = this;
switch (_that) {
case _AlertItem():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _AlertItem value)?  $default,){
final _that = this;
switch (_that) {
case _AlertItem() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String type,  String title,  String message,  String severity,  DateTime timestamp, @JsonKey(name: 'is_read')  bool isRead, @JsonKey(name: 'reference_id')  String? referenceId, @JsonKey(name: 'reference_type')  String? referenceType)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _AlertItem() when $default != null:
return $default(_that.id,_that.type,_that.title,_that.message,_that.severity,_that.timestamp,_that.isRead,_that.referenceId,_that.referenceType);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String type,  String title,  String message,  String severity,  DateTime timestamp, @JsonKey(name: 'is_read')  bool isRead, @JsonKey(name: 'reference_id')  String? referenceId, @JsonKey(name: 'reference_type')  String? referenceType)  $default,) {final _that = this;
switch (_that) {
case _AlertItem():
return $default(_that.id,_that.type,_that.title,_that.message,_that.severity,_that.timestamp,_that.isRead,_that.referenceId,_that.referenceType);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String type,  String title,  String message,  String severity,  DateTime timestamp, @JsonKey(name: 'is_read')  bool isRead, @JsonKey(name: 'reference_id')  String? referenceId, @JsonKey(name: 'reference_type')  String? referenceType)?  $default,) {final _that = this;
switch (_that) {
case _AlertItem() when $default != null:
return $default(_that.id,_that.type,_that.title,_that.message,_that.severity,_that.timestamp,_that.isRead,_that.referenceId,_that.referenceType);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _AlertItem implements AlertItem {
  const _AlertItem({required this.id, required this.type, required this.title, required this.message, this.severity = 'medium', required this.timestamp, @JsonKey(name: 'is_read') this.isRead = false, @JsonKey(name: 'reference_id') this.referenceId, @JsonKey(name: 'reference_type') this.referenceType});
  factory _AlertItem.fromJson(Map<String, dynamic> json) => _$AlertItemFromJson(json);

@override final  String id;
@override final  String type;
@override final  String title;
@override final  String message;
@override@JsonKey() final  String severity;
@override final  DateTime timestamp;
@override@JsonKey(name: 'is_read') final  bool isRead;
@override@JsonKey(name: 'reference_id') final  String? referenceId;
@override@JsonKey(name: 'reference_type') final  String? referenceType;

/// Create a copy of AlertItem
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$AlertItemCopyWith<_AlertItem> get copyWith => __$AlertItemCopyWithImpl<_AlertItem>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$AlertItemToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _AlertItem&&(identical(other.id, id) || other.id == id)&&(identical(other.type, type) || other.type == type)&&(identical(other.title, title) || other.title == title)&&(identical(other.message, message) || other.message == message)&&(identical(other.severity, severity) || other.severity == severity)&&(identical(other.timestamp, timestamp) || other.timestamp == timestamp)&&(identical(other.isRead, isRead) || other.isRead == isRead)&&(identical(other.referenceId, referenceId) || other.referenceId == referenceId)&&(identical(other.referenceType, referenceType) || other.referenceType == referenceType));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,type,title,message,severity,timestamp,isRead,referenceId,referenceType);

@override
String toString() {
  return 'AlertItem(id: $id, type: $type, title: $title, message: $message, severity: $severity, timestamp: $timestamp, isRead: $isRead, referenceId: $referenceId, referenceType: $referenceType)';
}


}

/// @nodoc
abstract mixin class _$AlertItemCopyWith<$Res> implements $AlertItemCopyWith<$Res> {
  factory _$AlertItemCopyWith(_AlertItem value, $Res Function(_AlertItem) _then) = __$AlertItemCopyWithImpl;
@override @useResult
$Res call({
 String id, String type, String title, String message, String severity, DateTime timestamp,@JsonKey(name: 'is_read') bool isRead,@JsonKey(name: 'reference_id') String? referenceId,@JsonKey(name: 'reference_type') String? referenceType
});




}
/// @nodoc
class __$AlertItemCopyWithImpl<$Res>
    implements _$AlertItemCopyWith<$Res> {
  __$AlertItemCopyWithImpl(this._self, this._then);

  final _AlertItem _self;
  final $Res Function(_AlertItem) _then;

/// Create a copy of AlertItem
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? type = null,Object? title = null,Object? message = null,Object? severity = null,Object? timestamp = null,Object? isRead = null,Object? referenceId = freezed,Object? referenceType = freezed,}) {
  return _then(_AlertItem(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,type: null == type ? _self.type : type // ignore: cast_nullable_to_non_nullable
as String,title: null == title ? _self.title : title // ignore: cast_nullable_to_non_nullable
as String,message: null == message ? _self.message : message // ignore: cast_nullable_to_non_nullable
as String,severity: null == severity ? _self.severity : severity // ignore: cast_nullable_to_non_nullable
as String,timestamp: null == timestamp ? _self.timestamp : timestamp // ignore: cast_nullable_to_non_nullable
as DateTime,isRead: null == isRead ? _self.isRead : isRead // ignore: cast_nullable_to_non_nullable
as bool,referenceId: freezed == referenceId ? _self.referenceId : referenceId // ignore: cast_nullable_to_non_nullable
as String?,referenceType: freezed == referenceType ? _self.referenceType : referenceType // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}


}

// dart format on
