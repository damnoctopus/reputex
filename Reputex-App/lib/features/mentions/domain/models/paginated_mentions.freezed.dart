// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'paginated_mentions.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$PaginatedMentions {

 List<Mention> get items;@JsonKey(name: 'total_count') int get totalCount; int get page;@JsonKey(name: 'total_pages') int get totalPages;@JsonKey(name: 'has_more') bool get hasMore;
/// Create a copy of PaginatedMentions
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$PaginatedMentionsCopyWith<PaginatedMentions> get copyWith => _$PaginatedMentionsCopyWithImpl<PaginatedMentions>(this as PaginatedMentions, _$identity);

  /// Serializes this PaginatedMentions to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is PaginatedMentions&&const DeepCollectionEquality().equals(other.items, items)&&(identical(other.totalCount, totalCount) || other.totalCount == totalCount)&&(identical(other.page, page) || other.page == page)&&(identical(other.totalPages, totalPages) || other.totalPages == totalPages)&&(identical(other.hasMore, hasMore) || other.hasMore == hasMore));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,const DeepCollectionEquality().hash(items),totalCount,page,totalPages,hasMore);

@override
String toString() {
  return 'PaginatedMentions(items: $items, totalCount: $totalCount, page: $page, totalPages: $totalPages, hasMore: $hasMore)';
}


}

/// @nodoc
abstract mixin class $PaginatedMentionsCopyWith<$Res>  {
  factory $PaginatedMentionsCopyWith(PaginatedMentions value, $Res Function(PaginatedMentions) _then) = _$PaginatedMentionsCopyWithImpl;
@useResult
$Res call({
 List<Mention> items,@JsonKey(name: 'total_count') int totalCount, int page,@JsonKey(name: 'total_pages') int totalPages,@JsonKey(name: 'has_more') bool hasMore
});




}
/// @nodoc
class _$PaginatedMentionsCopyWithImpl<$Res>
    implements $PaginatedMentionsCopyWith<$Res> {
  _$PaginatedMentionsCopyWithImpl(this._self, this._then);

  final PaginatedMentions _self;
  final $Res Function(PaginatedMentions) _then;

/// Create a copy of PaginatedMentions
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? items = null,Object? totalCount = null,Object? page = null,Object? totalPages = null,Object? hasMore = null,}) {
  return _then(_self.copyWith(
items: null == items ? _self.items : items // ignore: cast_nullable_to_non_nullable
as List<Mention>,totalCount: null == totalCount ? _self.totalCount : totalCount // ignore: cast_nullable_to_non_nullable
as int,page: null == page ? _self.page : page // ignore: cast_nullable_to_non_nullable
as int,totalPages: null == totalPages ? _self.totalPages : totalPages // ignore: cast_nullable_to_non_nullable
as int,hasMore: null == hasMore ? _self.hasMore : hasMore // ignore: cast_nullable_to_non_nullable
as bool,
  ));
}

}


/// Adds pattern-matching-related methods to [PaginatedMentions].
extension PaginatedMentionsPatterns on PaginatedMentions {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _PaginatedMentions value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _PaginatedMentions() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _PaginatedMentions value)  $default,){
final _that = this;
switch (_that) {
case _PaginatedMentions():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _PaginatedMentions value)?  $default,){
final _that = this;
switch (_that) {
case _PaginatedMentions() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( List<Mention> items, @JsonKey(name: 'total_count')  int totalCount,  int page, @JsonKey(name: 'total_pages')  int totalPages, @JsonKey(name: 'has_more')  bool hasMore)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _PaginatedMentions() when $default != null:
return $default(_that.items,_that.totalCount,_that.page,_that.totalPages,_that.hasMore);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( List<Mention> items, @JsonKey(name: 'total_count')  int totalCount,  int page, @JsonKey(name: 'total_pages')  int totalPages, @JsonKey(name: 'has_more')  bool hasMore)  $default,) {final _that = this;
switch (_that) {
case _PaginatedMentions():
return $default(_that.items,_that.totalCount,_that.page,_that.totalPages,_that.hasMore);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( List<Mention> items, @JsonKey(name: 'total_count')  int totalCount,  int page, @JsonKey(name: 'total_pages')  int totalPages, @JsonKey(name: 'has_more')  bool hasMore)?  $default,) {final _that = this;
switch (_that) {
case _PaginatedMentions() when $default != null:
return $default(_that.items,_that.totalCount,_that.page,_that.totalPages,_that.hasMore);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _PaginatedMentions implements PaginatedMentions {
  const _PaginatedMentions({required this.items, @JsonKey(name: 'total_count') required this.totalCount, this.page = 1, @JsonKey(name: 'total_pages') this.totalPages = 1, @JsonKey(name: 'has_more') this.hasMore = false});
  factory _PaginatedMentions.fromJson(Map<String, dynamic> json) => _$PaginatedMentionsFromJson(json);

@override final  List<Mention> items;
@override@JsonKey(name: 'total_count') final  int totalCount;
@override@JsonKey() final  int page;
@override@JsonKey(name: 'total_pages') final  int totalPages;
@override@JsonKey(name: 'has_more') final  bool hasMore;

/// Create a copy of PaginatedMentions
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$PaginatedMentionsCopyWith<_PaginatedMentions> get copyWith => __$PaginatedMentionsCopyWithImpl<_PaginatedMentions>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$PaginatedMentionsToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _PaginatedMentions&&const DeepCollectionEquality().equals(other.items, items)&&(identical(other.totalCount, totalCount) || other.totalCount == totalCount)&&(identical(other.page, page) || other.page == page)&&(identical(other.totalPages, totalPages) || other.totalPages == totalPages)&&(identical(other.hasMore, hasMore) || other.hasMore == hasMore));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,const DeepCollectionEquality().hash(items),totalCount,page,totalPages,hasMore);

@override
String toString() {
  return 'PaginatedMentions(items: $items, totalCount: $totalCount, page: $page, totalPages: $totalPages, hasMore: $hasMore)';
}


}

/// @nodoc
abstract mixin class _$PaginatedMentionsCopyWith<$Res> implements $PaginatedMentionsCopyWith<$Res> {
  factory _$PaginatedMentionsCopyWith(_PaginatedMentions value, $Res Function(_PaginatedMentions) _then) = __$PaginatedMentionsCopyWithImpl;
@override @useResult
$Res call({
 List<Mention> items,@JsonKey(name: 'total_count') int totalCount, int page,@JsonKey(name: 'total_pages') int totalPages,@JsonKey(name: 'has_more') bool hasMore
});




}
/// @nodoc
class __$PaginatedMentionsCopyWithImpl<$Res>
    implements _$PaginatedMentionsCopyWith<$Res> {
  __$PaginatedMentionsCopyWithImpl(this._self, this._then);

  final _PaginatedMentions _self;
  final $Res Function(_PaginatedMentions) _then;

/// Create a copy of PaginatedMentions
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? items = null,Object? totalCount = null,Object? page = null,Object? totalPages = null,Object? hasMore = null,}) {
  return _then(_PaginatedMentions(
items: null == items ? _self.items : items // ignore: cast_nullable_to_non_nullable
as List<Mention>,totalCount: null == totalCount ? _self.totalCount : totalCount // ignore: cast_nullable_to_non_nullable
as int,page: null == page ? _self.page : page // ignore: cast_nullable_to_non_nullable
as int,totalPages: null == totalPages ? _self.totalPages : totalPages // ignore: cast_nullable_to_non_nullable
as int,hasMore: null == hasMore ? _self.hasMore : hasMore // ignore: cast_nullable_to_non_nullable
as bool,
  ));
}


}

// dart format on
