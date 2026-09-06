// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'mention_engagement.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$MentionEngagement {

 int get likes; int get shares; int get comments;
/// Create a copy of MentionEngagement
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$MentionEngagementCopyWith<MentionEngagement> get copyWith => _$MentionEngagementCopyWithImpl<MentionEngagement>(this as MentionEngagement, _$identity);

  /// Serializes this MentionEngagement to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is MentionEngagement&&(identical(other.likes, likes) || other.likes == likes)&&(identical(other.shares, shares) || other.shares == shares)&&(identical(other.comments, comments) || other.comments == comments));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,likes,shares,comments);

@override
String toString() {
  return 'MentionEngagement(likes: $likes, shares: $shares, comments: $comments)';
}


}

/// @nodoc
abstract mixin class $MentionEngagementCopyWith<$Res>  {
  factory $MentionEngagementCopyWith(MentionEngagement value, $Res Function(MentionEngagement) _then) = _$MentionEngagementCopyWithImpl;
@useResult
$Res call({
 int likes, int shares, int comments
});




}
/// @nodoc
class _$MentionEngagementCopyWithImpl<$Res>
    implements $MentionEngagementCopyWith<$Res> {
  _$MentionEngagementCopyWithImpl(this._self, this._then);

  final MentionEngagement _self;
  final $Res Function(MentionEngagement) _then;

/// Create a copy of MentionEngagement
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? likes = null,Object? shares = null,Object? comments = null,}) {
  return _then(_self.copyWith(
likes: null == likes ? _self.likes : likes // ignore: cast_nullable_to_non_nullable
as int,shares: null == shares ? _self.shares : shares // ignore: cast_nullable_to_non_nullable
as int,comments: null == comments ? _self.comments : comments // ignore: cast_nullable_to_non_nullable
as int,
  ));
}

}


/// Adds pattern-matching-related methods to [MentionEngagement].
extension MentionEngagementPatterns on MentionEngagement {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _MentionEngagement value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _MentionEngagement() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _MentionEngagement value)  $default,){
final _that = this;
switch (_that) {
case _MentionEngagement():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _MentionEngagement value)?  $default,){
final _that = this;
switch (_that) {
case _MentionEngagement() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( int likes,  int shares,  int comments)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _MentionEngagement() when $default != null:
return $default(_that.likes,_that.shares,_that.comments);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( int likes,  int shares,  int comments)  $default,) {final _that = this;
switch (_that) {
case _MentionEngagement():
return $default(_that.likes,_that.shares,_that.comments);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( int likes,  int shares,  int comments)?  $default,) {final _that = this;
switch (_that) {
case _MentionEngagement() when $default != null:
return $default(_that.likes,_that.shares,_that.comments);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _MentionEngagement implements MentionEngagement {
  const _MentionEngagement({this.likes = 0, this.shares = 0, this.comments = 0});
  factory _MentionEngagement.fromJson(Map<String, dynamic> json) => _$MentionEngagementFromJson(json);

@override@JsonKey() final  int likes;
@override@JsonKey() final  int shares;
@override@JsonKey() final  int comments;

/// Create a copy of MentionEngagement
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$MentionEngagementCopyWith<_MentionEngagement> get copyWith => __$MentionEngagementCopyWithImpl<_MentionEngagement>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$MentionEngagementToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _MentionEngagement&&(identical(other.likes, likes) || other.likes == likes)&&(identical(other.shares, shares) || other.shares == shares)&&(identical(other.comments, comments) || other.comments == comments));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,likes,shares,comments);

@override
String toString() {
  return 'MentionEngagement(likes: $likes, shares: $shares, comments: $comments)';
}


}

/// @nodoc
abstract mixin class _$MentionEngagementCopyWith<$Res> implements $MentionEngagementCopyWith<$Res> {
  factory _$MentionEngagementCopyWith(_MentionEngagement value, $Res Function(_MentionEngagement) _then) = __$MentionEngagementCopyWithImpl;
@override @useResult
$Res call({
 int likes, int shares, int comments
});




}
/// @nodoc
class __$MentionEngagementCopyWithImpl<$Res>
    implements _$MentionEngagementCopyWith<$Res> {
  __$MentionEngagementCopyWithImpl(this._self, this._then);

  final _MentionEngagement _self;
  final $Res Function(_MentionEngagement) _then;

/// Create a copy of MentionEngagement
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? likes = null,Object? shares = null,Object? comments = null,}) {
  return _then(_MentionEngagement(
likes: null == likes ? _self.likes : likes // ignore: cast_nullable_to_non_nullable
as int,shares: null == shares ? _self.shares : shares // ignore: cast_nullable_to_non_nullable
as int,comments: null == comments ? _self.comments : comments // ignore: cast_nullable_to_non_nullable
as int,
  ));
}


}

// dart format on
