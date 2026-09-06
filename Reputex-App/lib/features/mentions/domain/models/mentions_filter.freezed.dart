// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'mentions_filter.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$MentionsFilter {

 String? get platform; String? get sentiment;@JsonKey(name: 'is_fake') bool? get isFake;@JsonKey(name: 'search_query') String? get searchQuery; int get page; int get limit;@JsonKey(name: 'sort_by') String get sortBy;
/// Create a copy of MentionsFilter
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$MentionsFilterCopyWith<MentionsFilter> get copyWith => _$MentionsFilterCopyWithImpl<MentionsFilter>(this as MentionsFilter, _$identity);

  /// Serializes this MentionsFilter to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is MentionsFilter&&(identical(other.platform, platform) || other.platform == platform)&&(identical(other.sentiment, sentiment) || other.sentiment == sentiment)&&(identical(other.isFake, isFake) || other.isFake == isFake)&&(identical(other.searchQuery, searchQuery) || other.searchQuery == searchQuery)&&(identical(other.page, page) || other.page == page)&&(identical(other.limit, limit) || other.limit == limit)&&(identical(other.sortBy, sortBy) || other.sortBy == sortBy));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,platform,sentiment,isFake,searchQuery,page,limit,sortBy);

@override
String toString() {
  return 'MentionsFilter(platform: $platform, sentiment: $sentiment, isFake: $isFake, searchQuery: $searchQuery, page: $page, limit: $limit, sortBy: $sortBy)';
}


}

/// @nodoc
abstract mixin class $MentionsFilterCopyWith<$Res>  {
  factory $MentionsFilterCopyWith(MentionsFilter value, $Res Function(MentionsFilter) _then) = _$MentionsFilterCopyWithImpl;
@useResult
$Res call({
 String? platform, String? sentiment,@JsonKey(name: 'is_fake') bool? isFake,@JsonKey(name: 'search_query') String? searchQuery, int page, int limit,@JsonKey(name: 'sort_by') String sortBy
});




}
/// @nodoc
class _$MentionsFilterCopyWithImpl<$Res>
    implements $MentionsFilterCopyWith<$Res> {
  _$MentionsFilterCopyWithImpl(this._self, this._then);

  final MentionsFilter _self;
  final $Res Function(MentionsFilter) _then;

/// Create a copy of MentionsFilter
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? platform = freezed,Object? sentiment = freezed,Object? isFake = freezed,Object? searchQuery = freezed,Object? page = null,Object? limit = null,Object? sortBy = null,}) {
  return _then(_self.copyWith(
platform: freezed == platform ? _self.platform : platform // ignore: cast_nullable_to_non_nullable
as String?,sentiment: freezed == sentiment ? _self.sentiment : sentiment // ignore: cast_nullable_to_non_nullable
as String?,isFake: freezed == isFake ? _self.isFake : isFake // ignore: cast_nullable_to_non_nullable
as bool?,searchQuery: freezed == searchQuery ? _self.searchQuery : searchQuery // ignore: cast_nullable_to_non_nullable
as String?,page: null == page ? _self.page : page // ignore: cast_nullable_to_non_nullable
as int,limit: null == limit ? _self.limit : limit // ignore: cast_nullable_to_non_nullable
as int,sortBy: null == sortBy ? _self.sortBy : sortBy // ignore: cast_nullable_to_non_nullable
as String,
  ));
}

}


/// Adds pattern-matching-related methods to [MentionsFilter].
extension MentionsFilterPatterns on MentionsFilter {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _MentionsFilter value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _MentionsFilter() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _MentionsFilter value)  $default,){
final _that = this;
switch (_that) {
case _MentionsFilter():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _MentionsFilter value)?  $default,){
final _that = this;
switch (_that) {
case _MentionsFilter() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String? platform,  String? sentiment, @JsonKey(name: 'is_fake')  bool? isFake, @JsonKey(name: 'search_query')  String? searchQuery,  int page,  int limit, @JsonKey(name: 'sort_by')  String sortBy)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _MentionsFilter() when $default != null:
return $default(_that.platform,_that.sentiment,_that.isFake,_that.searchQuery,_that.page,_that.limit,_that.sortBy);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String? platform,  String? sentiment, @JsonKey(name: 'is_fake')  bool? isFake, @JsonKey(name: 'search_query')  String? searchQuery,  int page,  int limit, @JsonKey(name: 'sort_by')  String sortBy)  $default,) {final _that = this;
switch (_that) {
case _MentionsFilter():
return $default(_that.platform,_that.sentiment,_that.isFake,_that.searchQuery,_that.page,_that.limit,_that.sortBy);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String? platform,  String? sentiment, @JsonKey(name: 'is_fake')  bool? isFake, @JsonKey(name: 'search_query')  String? searchQuery,  int page,  int limit, @JsonKey(name: 'sort_by')  String sortBy)?  $default,) {final _that = this;
switch (_that) {
case _MentionsFilter() when $default != null:
return $default(_that.platform,_that.sentiment,_that.isFake,_that.searchQuery,_that.page,_that.limit,_that.sortBy);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _MentionsFilter implements MentionsFilter {
  const _MentionsFilter({this.platform, this.sentiment, @JsonKey(name: 'is_fake') this.isFake, @JsonKey(name: 'search_query') this.searchQuery, this.page = 1, this.limit = 20, @JsonKey(name: 'sort_by') this.sortBy = 'newest'});
  factory _MentionsFilter.fromJson(Map<String, dynamic> json) => _$MentionsFilterFromJson(json);

@override final  String? platform;
@override final  String? sentiment;
@override@JsonKey(name: 'is_fake') final  bool? isFake;
@override@JsonKey(name: 'search_query') final  String? searchQuery;
@override@JsonKey() final  int page;
@override@JsonKey() final  int limit;
@override@JsonKey(name: 'sort_by') final  String sortBy;

/// Create a copy of MentionsFilter
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$MentionsFilterCopyWith<_MentionsFilter> get copyWith => __$MentionsFilterCopyWithImpl<_MentionsFilter>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$MentionsFilterToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _MentionsFilter&&(identical(other.platform, platform) || other.platform == platform)&&(identical(other.sentiment, sentiment) || other.sentiment == sentiment)&&(identical(other.isFake, isFake) || other.isFake == isFake)&&(identical(other.searchQuery, searchQuery) || other.searchQuery == searchQuery)&&(identical(other.page, page) || other.page == page)&&(identical(other.limit, limit) || other.limit == limit)&&(identical(other.sortBy, sortBy) || other.sortBy == sortBy));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,platform,sentiment,isFake,searchQuery,page,limit,sortBy);

@override
String toString() {
  return 'MentionsFilter(platform: $platform, sentiment: $sentiment, isFake: $isFake, searchQuery: $searchQuery, page: $page, limit: $limit, sortBy: $sortBy)';
}


}

/// @nodoc
abstract mixin class _$MentionsFilterCopyWith<$Res> implements $MentionsFilterCopyWith<$Res> {
  factory _$MentionsFilterCopyWith(_MentionsFilter value, $Res Function(_MentionsFilter) _then) = __$MentionsFilterCopyWithImpl;
@override @useResult
$Res call({
 String? platform, String? sentiment,@JsonKey(name: 'is_fake') bool? isFake,@JsonKey(name: 'search_query') String? searchQuery, int page, int limit,@JsonKey(name: 'sort_by') String sortBy
});




}
/// @nodoc
class __$MentionsFilterCopyWithImpl<$Res>
    implements _$MentionsFilterCopyWith<$Res> {
  __$MentionsFilterCopyWithImpl(this._self, this._then);

  final _MentionsFilter _self;
  final $Res Function(_MentionsFilter) _then;

/// Create a copy of MentionsFilter
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? platform = freezed,Object? sentiment = freezed,Object? isFake = freezed,Object? searchQuery = freezed,Object? page = null,Object? limit = null,Object? sortBy = null,}) {
  return _then(_MentionsFilter(
platform: freezed == platform ? _self.platform : platform // ignore: cast_nullable_to_non_nullable
as String?,sentiment: freezed == sentiment ? _self.sentiment : sentiment // ignore: cast_nullable_to_non_nullable
as String?,isFake: freezed == isFake ? _self.isFake : isFake // ignore: cast_nullable_to_non_nullable
as bool?,searchQuery: freezed == searchQuery ? _self.searchQuery : searchQuery // ignore: cast_nullable_to_non_nullable
as String?,page: null == page ? _self.page : page // ignore: cast_nullable_to_non_nullable
as int,limit: null == limit ? _self.limit : limit // ignore: cast_nullable_to_non_nullable
as int,sortBy: null == sortBy ? _self.sortBy : sortBy // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}

// dart format on
