// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'brand_keyword.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$BrandKeyword {

 String get id; String get keyword; String get category;@JsonKey(name: 'is_active') bool get isActive;@JsonKey(name: 'business_id') String? get businessId;
/// Create a copy of BrandKeyword
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$BrandKeywordCopyWith<BrandKeyword> get copyWith => _$BrandKeywordCopyWithImpl<BrandKeyword>(this as BrandKeyword, _$identity);

  /// Serializes this BrandKeyword to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is BrandKeyword&&(identical(other.id, id) || other.id == id)&&(identical(other.keyword, keyword) || other.keyword == keyword)&&(identical(other.category, category) || other.category == category)&&(identical(other.isActive, isActive) || other.isActive == isActive)&&(identical(other.businessId, businessId) || other.businessId == businessId));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,keyword,category,isActive,businessId);

@override
String toString() {
  return 'BrandKeyword(id: $id, keyword: $keyword, category: $category, isActive: $isActive, businessId: $businessId)';
}


}

/// @nodoc
abstract mixin class $BrandKeywordCopyWith<$Res>  {
  factory $BrandKeywordCopyWith(BrandKeyword value, $Res Function(BrandKeyword) _then) = _$BrandKeywordCopyWithImpl;
@useResult
$Res call({
 String id, String keyword, String category,@JsonKey(name: 'is_active') bool isActive,@JsonKey(name: 'business_id') String? businessId
});




}
/// @nodoc
class _$BrandKeywordCopyWithImpl<$Res>
    implements $BrandKeywordCopyWith<$Res> {
  _$BrandKeywordCopyWithImpl(this._self, this._then);

  final BrandKeyword _self;
  final $Res Function(BrandKeyword) _then;

/// Create a copy of BrandKeyword
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? keyword = null,Object? category = null,Object? isActive = null,Object? businessId = freezed,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,keyword: null == keyword ? _self.keyword : keyword // ignore: cast_nullable_to_non_nullable
as String,category: null == category ? _self.category : category // ignore: cast_nullable_to_non_nullable
as String,isActive: null == isActive ? _self.isActive : isActive // ignore: cast_nullable_to_non_nullable
as bool,businessId: freezed == businessId ? _self.businessId : businessId // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}

}


/// Adds pattern-matching-related methods to [BrandKeyword].
extension BrandKeywordPatterns on BrandKeyword {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _BrandKeyword value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _BrandKeyword() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _BrandKeyword value)  $default,){
final _that = this;
switch (_that) {
case _BrandKeyword():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _BrandKeyword value)?  $default,){
final _that = this;
switch (_that) {
case _BrandKeyword() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String keyword,  String category, @JsonKey(name: 'is_active')  bool isActive, @JsonKey(name: 'business_id')  String? businessId)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _BrandKeyword() when $default != null:
return $default(_that.id,_that.keyword,_that.category,_that.isActive,_that.businessId);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String keyword,  String category, @JsonKey(name: 'is_active')  bool isActive, @JsonKey(name: 'business_id')  String? businessId)  $default,) {final _that = this;
switch (_that) {
case _BrandKeyword():
return $default(_that.id,_that.keyword,_that.category,_that.isActive,_that.businessId);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String keyword,  String category, @JsonKey(name: 'is_active')  bool isActive, @JsonKey(name: 'business_id')  String? businessId)?  $default,) {final _that = this;
switch (_that) {
case _BrandKeyword() when $default != null:
return $default(_that.id,_that.keyword,_that.category,_that.isActive,_that.businessId);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _BrandKeyword implements BrandKeyword {
  const _BrandKeyword({required this.id, required this.keyword, this.category = 'brand', @JsonKey(name: 'is_active') this.isActive = true, @JsonKey(name: 'business_id') this.businessId});
  factory _BrandKeyword.fromJson(Map<String, dynamic> json) => _$BrandKeywordFromJson(json);

@override final  String id;
@override final  String keyword;
@override@JsonKey() final  String category;
@override@JsonKey(name: 'is_active') final  bool isActive;
@override@JsonKey(name: 'business_id') final  String? businessId;

/// Create a copy of BrandKeyword
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$BrandKeywordCopyWith<_BrandKeyword> get copyWith => __$BrandKeywordCopyWithImpl<_BrandKeyword>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$BrandKeywordToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _BrandKeyword&&(identical(other.id, id) || other.id == id)&&(identical(other.keyword, keyword) || other.keyword == keyword)&&(identical(other.category, category) || other.category == category)&&(identical(other.isActive, isActive) || other.isActive == isActive)&&(identical(other.businessId, businessId) || other.businessId == businessId));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,keyword,category,isActive,businessId);

@override
String toString() {
  return 'BrandKeyword(id: $id, keyword: $keyword, category: $category, isActive: $isActive, businessId: $businessId)';
}


}

/// @nodoc
abstract mixin class _$BrandKeywordCopyWith<$Res> implements $BrandKeywordCopyWith<$Res> {
  factory _$BrandKeywordCopyWith(_BrandKeyword value, $Res Function(_BrandKeyword) _then) = __$BrandKeywordCopyWithImpl;
@override @useResult
$Res call({
 String id, String keyword, String category,@JsonKey(name: 'is_active') bool isActive,@JsonKey(name: 'business_id') String? businessId
});




}
/// @nodoc
class __$BrandKeywordCopyWithImpl<$Res>
    implements _$BrandKeywordCopyWith<$Res> {
  __$BrandKeywordCopyWithImpl(this._self, this._then);

  final _BrandKeyword _self;
  final $Res Function(_BrandKeyword) _then;

/// Create a copy of BrandKeyword
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? keyword = null,Object? category = null,Object? isActive = null,Object? businessId = freezed,}) {
  return _then(_BrandKeyword(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,keyword: null == keyword ? _self.keyword : keyword // ignore: cast_nullable_to_non_nullable
as String,category: null == category ? _self.category : category // ignore: cast_nullable_to_non_nullable
as String,isActive: null == isActive ? _self.isActive : isActive // ignore: cast_nullable_to_non_nullable
as bool,businessId: freezed == businessId ? _self.businessId : businessId // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}


}

// dart format on
