// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'fraud_result.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$SuspiciousPattern {

@JsonKey(name: 'pattern_name') String get patternName; String get description; String get severity;
/// Create a copy of SuspiciousPattern
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$SuspiciousPatternCopyWith<SuspiciousPattern> get copyWith => _$SuspiciousPatternCopyWithImpl<SuspiciousPattern>(this as SuspiciousPattern, _$identity);

  /// Serializes this SuspiciousPattern to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is SuspiciousPattern&&(identical(other.patternName, patternName) || other.patternName == patternName)&&(identical(other.description, description) || other.description == description)&&(identical(other.severity, severity) || other.severity == severity));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,patternName,description,severity);

@override
String toString() {
  return 'SuspiciousPattern(patternName: $patternName, description: $description, severity: $severity)';
}


}

/// @nodoc
abstract mixin class $SuspiciousPatternCopyWith<$Res>  {
  factory $SuspiciousPatternCopyWith(SuspiciousPattern value, $Res Function(SuspiciousPattern) _then) = _$SuspiciousPatternCopyWithImpl;
@useResult
$Res call({
@JsonKey(name: 'pattern_name') String patternName, String description, String severity
});




}
/// @nodoc
class _$SuspiciousPatternCopyWithImpl<$Res>
    implements $SuspiciousPatternCopyWith<$Res> {
  _$SuspiciousPatternCopyWithImpl(this._self, this._then);

  final SuspiciousPattern _self;
  final $Res Function(SuspiciousPattern) _then;

/// Create a copy of SuspiciousPattern
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? patternName = null,Object? description = null,Object? severity = null,}) {
  return _then(_self.copyWith(
patternName: null == patternName ? _self.patternName : patternName // ignore: cast_nullable_to_non_nullable
as String,description: null == description ? _self.description : description // ignore: cast_nullable_to_non_nullable
as String,severity: null == severity ? _self.severity : severity // ignore: cast_nullable_to_non_nullable
as String,
  ));
}

}


/// Adds pattern-matching-related methods to [SuspiciousPattern].
extension SuspiciousPatternPatterns on SuspiciousPattern {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _SuspiciousPattern value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _SuspiciousPattern() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _SuspiciousPattern value)  $default,){
final _that = this;
switch (_that) {
case _SuspiciousPattern():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _SuspiciousPattern value)?  $default,){
final _that = this;
switch (_that) {
case _SuspiciousPattern() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function(@JsonKey(name: 'pattern_name')  String patternName,  String description,  String severity)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _SuspiciousPattern() when $default != null:
return $default(_that.patternName,_that.description,_that.severity);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function(@JsonKey(name: 'pattern_name')  String patternName,  String description,  String severity)  $default,) {final _that = this;
switch (_that) {
case _SuspiciousPattern():
return $default(_that.patternName,_that.description,_that.severity);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function(@JsonKey(name: 'pattern_name')  String patternName,  String description,  String severity)?  $default,) {final _that = this;
switch (_that) {
case _SuspiciousPattern() when $default != null:
return $default(_that.patternName,_that.description,_that.severity);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _SuspiciousPattern implements SuspiciousPattern {
  const _SuspiciousPattern({@JsonKey(name: 'pattern_name') required this.patternName, required this.description, this.severity = 'medium'});
  factory _SuspiciousPattern.fromJson(Map<String, dynamic> json) => _$SuspiciousPatternFromJson(json);

@override@JsonKey(name: 'pattern_name') final  String patternName;
@override final  String description;
@override@JsonKey() final  String severity;

/// Create a copy of SuspiciousPattern
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$SuspiciousPatternCopyWith<_SuspiciousPattern> get copyWith => __$SuspiciousPatternCopyWithImpl<_SuspiciousPattern>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$SuspiciousPatternToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _SuspiciousPattern&&(identical(other.patternName, patternName) || other.patternName == patternName)&&(identical(other.description, description) || other.description == description)&&(identical(other.severity, severity) || other.severity == severity));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,patternName,description,severity);

@override
String toString() {
  return 'SuspiciousPattern(patternName: $patternName, description: $description, severity: $severity)';
}


}

/// @nodoc
abstract mixin class _$SuspiciousPatternCopyWith<$Res> implements $SuspiciousPatternCopyWith<$Res> {
  factory _$SuspiciousPatternCopyWith(_SuspiciousPattern value, $Res Function(_SuspiciousPattern) _then) = __$SuspiciousPatternCopyWithImpl;
@override @useResult
$Res call({
@JsonKey(name: 'pattern_name') String patternName, String description, String severity
});




}
/// @nodoc
class __$SuspiciousPatternCopyWithImpl<$Res>
    implements _$SuspiciousPatternCopyWith<$Res> {
  __$SuspiciousPatternCopyWithImpl(this._self, this._then);

  final _SuspiciousPattern _self;
  final $Res Function(_SuspiciousPattern) _then;

/// Create a copy of SuspiciousPattern
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? patternName = null,Object? description = null,Object? severity = null,}) {
  return _then(_SuspiciousPattern(
patternName: null == patternName ? _self.patternName : patternName // ignore: cast_nullable_to_non_nullable
as String,description: null == description ? _self.description : description // ignore: cast_nullable_to_non_nullable
as String,severity: null == severity ? _self.severity : severity // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}


/// @nodoc
mixin _$FraudResult {

@JsonKey(name: 'mention_id') String get mentionId;@JsonKey(name: 'is_fraudulent') bool get isFraudulent; double get confidence;@JsonKey(name: 'risk_level') String get riskLevel; List<String> get reasons; List<SuspiciousPattern> get patterns;@JsonKey(name: 'review_content') String? get reviewContent; String? get author; String? get platform; DateTime? get timestamp;
/// Create a copy of FraudResult
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$FraudResultCopyWith<FraudResult> get copyWith => _$FraudResultCopyWithImpl<FraudResult>(this as FraudResult, _$identity);

  /// Serializes this FraudResult to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is FraudResult&&(identical(other.mentionId, mentionId) || other.mentionId == mentionId)&&(identical(other.isFraudulent, isFraudulent) || other.isFraudulent == isFraudulent)&&(identical(other.confidence, confidence) || other.confidence == confidence)&&(identical(other.riskLevel, riskLevel) || other.riskLevel == riskLevel)&&const DeepCollectionEquality().equals(other.reasons, reasons)&&const DeepCollectionEquality().equals(other.patterns, patterns)&&(identical(other.reviewContent, reviewContent) || other.reviewContent == reviewContent)&&(identical(other.author, author) || other.author == author)&&(identical(other.platform, platform) || other.platform == platform)&&(identical(other.timestamp, timestamp) || other.timestamp == timestamp));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,mentionId,isFraudulent,confidence,riskLevel,const DeepCollectionEquality().hash(reasons),const DeepCollectionEquality().hash(patterns),reviewContent,author,platform,timestamp);

@override
String toString() {
  return 'FraudResult(mentionId: $mentionId, isFraudulent: $isFraudulent, confidence: $confidence, riskLevel: $riskLevel, reasons: $reasons, patterns: $patterns, reviewContent: $reviewContent, author: $author, platform: $platform, timestamp: $timestamp)';
}


}

/// @nodoc
abstract mixin class $FraudResultCopyWith<$Res>  {
  factory $FraudResultCopyWith(FraudResult value, $Res Function(FraudResult) _then) = _$FraudResultCopyWithImpl;
@useResult
$Res call({
@JsonKey(name: 'mention_id') String mentionId,@JsonKey(name: 'is_fraudulent') bool isFraudulent, double confidence,@JsonKey(name: 'risk_level') String riskLevel, List<String> reasons, List<SuspiciousPattern> patterns,@JsonKey(name: 'review_content') String? reviewContent, String? author, String? platform, DateTime? timestamp
});




}
/// @nodoc
class _$FraudResultCopyWithImpl<$Res>
    implements $FraudResultCopyWith<$Res> {
  _$FraudResultCopyWithImpl(this._self, this._then);

  final FraudResult _self;
  final $Res Function(FraudResult) _then;

/// Create a copy of FraudResult
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? mentionId = null,Object? isFraudulent = null,Object? confidence = null,Object? riskLevel = null,Object? reasons = null,Object? patterns = null,Object? reviewContent = freezed,Object? author = freezed,Object? platform = freezed,Object? timestamp = freezed,}) {
  return _then(_self.copyWith(
mentionId: null == mentionId ? _self.mentionId : mentionId // ignore: cast_nullable_to_non_nullable
as String,isFraudulent: null == isFraudulent ? _self.isFraudulent : isFraudulent // ignore: cast_nullable_to_non_nullable
as bool,confidence: null == confidence ? _self.confidence : confidence // ignore: cast_nullable_to_non_nullable
as double,riskLevel: null == riskLevel ? _self.riskLevel : riskLevel // ignore: cast_nullable_to_non_nullable
as String,reasons: null == reasons ? _self.reasons : reasons // ignore: cast_nullable_to_non_nullable
as List<String>,patterns: null == patterns ? _self.patterns : patterns // ignore: cast_nullable_to_non_nullable
as List<SuspiciousPattern>,reviewContent: freezed == reviewContent ? _self.reviewContent : reviewContent // ignore: cast_nullable_to_non_nullable
as String?,author: freezed == author ? _self.author : author // ignore: cast_nullable_to_non_nullable
as String?,platform: freezed == platform ? _self.platform : platform // ignore: cast_nullable_to_non_nullable
as String?,timestamp: freezed == timestamp ? _self.timestamp : timestamp // ignore: cast_nullable_to_non_nullable
as DateTime?,
  ));
}

}


/// Adds pattern-matching-related methods to [FraudResult].
extension FraudResultPatterns on FraudResult {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _FraudResult value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _FraudResult() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _FraudResult value)  $default,){
final _that = this;
switch (_that) {
case _FraudResult():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _FraudResult value)?  $default,){
final _that = this;
switch (_that) {
case _FraudResult() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function(@JsonKey(name: 'mention_id')  String mentionId, @JsonKey(name: 'is_fraudulent')  bool isFraudulent,  double confidence, @JsonKey(name: 'risk_level')  String riskLevel,  List<String> reasons,  List<SuspiciousPattern> patterns, @JsonKey(name: 'review_content')  String? reviewContent,  String? author,  String? platform,  DateTime? timestamp)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _FraudResult() when $default != null:
return $default(_that.mentionId,_that.isFraudulent,_that.confidence,_that.riskLevel,_that.reasons,_that.patterns,_that.reviewContent,_that.author,_that.platform,_that.timestamp);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function(@JsonKey(name: 'mention_id')  String mentionId, @JsonKey(name: 'is_fraudulent')  bool isFraudulent,  double confidence, @JsonKey(name: 'risk_level')  String riskLevel,  List<String> reasons,  List<SuspiciousPattern> patterns, @JsonKey(name: 'review_content')  String? reviewContent,  String? author,  String? platform,  DateTime? timestamp)  $default,) {final _that = this;
switch (_that) {
case _FraudResult():
return $default(_that.mentionId,_that.isFraudulent,_that.confidence,_that.riskLevel,_that.reasons,_that.patterns,_that.reviewContent,_that.author,_that.platform,_that.timestamp);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function(@JsonKey(name: 'mention_id')  String mentionId, @JsonKey(name: 'is_fraudulent')  bool isFraudulent,  double confidence, @JsonKey(name: 'risk_level')  String riskLevel,  List<String> reasons,  List<SuspiciousPattern> patterns, @JsonKey(name: 'review_content')  String? reviewContent,  String? author,  String? platform,  DateTime? timestamp)?  $default,) {final _that = this;
switch (_that) {
case _FraudResult() when $default != null:
return $default(_that.mentionId,_that.isFraudulent,_that.confidence,_that.riskLevel,_that.reasons,_that.patterns,_that.reviewContent,_that.author,_that.platform,_that.timestamp);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _FraudResult implements FraudResult {
  const _FraudResult({@JsonKey(name: 'mention_id') required this.mentionId, @JsonKey(name: 'is_fraudulent') required this.isFraudulent, required this.confidence, @JsonKey(name: 'risk_level') required this.riskLevel, this.reasons = const [], this.patterns = const [], @JsonKey(name: 'review_content') this.reviewContent, this.author, this.platform, this.timestamp});
  factory _FraudResult.fromJson(Map<String, dynamic> json) => _$FraudResultFromJson(json);

@override@JsonKey(name: 'mention_id') final  String mentionId;
@override@JsonKey(name: 'is_fraudulent') final  bool isFraudulent;
@override final  double confidence;
@override@JsonKey(name: 'risk_level') final  String riskLevel;
@override@JsonKey() final  List<String> reasons;
@override@JsonKey() final  List<SuspiciousPattern> patterns;
@override@JsonKey(name: 'review_content') final  String? reviewContent;
@override final  String? author;
@override final  String? platform;
@override final  DateTime? timestamp;

/// Create a copy of FraudResult
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$FraudResultCopyWith<_FraudResult> get copyWith => __$FraudResultCopyWithImpl<_FraudResult>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$FraudResultToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _FraudResult&&(identical(other.mentionId, mentionId) || other.mentionId == mentionId)&&(identical(other.isFraudulent, isFraudulent) || other.isFraudulent == isFraudulent)&&(identical(other.confidence, confidence) || other.confidence == confidence)&&(identical(other.riskLevel, riskLevel) || other.riskLevel == riskLevel)&&const DeepCollectionEquality().equals(other.reasons, reasons)&&const DeepCollectionEquality().equals(other.patterns, patterns)&&(identical(other.reviewContent, reviewContent) || other.reviewContent == reviewContent)&&(identical(other.author, author) || other.author == author)&&(identical(other.platform, platform) || other.platform == platform)&&(identical(other.timestamp, timestamp) || other.timestamp == timestamp));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,mentionId,isFraudulent,confidence,riskLevel,const DeepCollectionEquality().hash(reasons),const DeepCollectionEquality().hash(patterns),reviewContent,author,platform,timestamp);

@override
String toString() {
  return 'FraudResult(mentionId: $mentionId, isFraudulent: $isFraudulent, confidence: $confidence, riskLevel: $riskLevel, reasons: $reasons, patterns: $patterns, reviewContent: $reviewContent, author: $author, platform: $platform, timestamp: $timestamp)';
}


}

/// @nodoc
abstract mixin class _$FraudResultCopyWith<$Res> implements $FraudResultCopyWith<$Res> {
  factory _$FraudResultCopyWith(_FraudResult value, $Res Function(_FraudResult) _then) = __$FraudResultCopyWithImpl;
@override @useResult
$Res call({
@JsonKey(name: 'mention_id') String mentionId,@JsonKey(name: 'is_fraudulent') bool isFraudulent, double confidence,@JsonKey(name: 'risk_level') String riskLevel, List<String> reasons, List<SuspiciousPattern> patterns,@JsonKey(name: 'review_content') String? reviewContent, String? author, String? platform, DateTime? timestamp
});




}
/// @nodoc
class __$FraudResultCopyWithImpl<$Res>
    implements _$FraudResultCopyWith<$Res> {
  __$FraudResultCopyWithImpl(this._self, this._then);

  final _FraudResult _self;
  final $Res Function(_FraudResult) _then;

/// Create a copy of FraudResult
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? mentionId = null,Object? isFraudulent = null,Object? confidence = null,Object? riskLevel = null,Object? reasons = null,Object? patterns = null,Object? reviewContent = freezed,Object? author = freezed,Object? platform = freezed,Object? timestamp = freezed,}) {
  return _then(_FraudResult(
mentionId: null == mentionId ? _self.mentionId : mentionId // ignore: cast_nullable_to_non_nullable
as String,isFraudulent: null == isFraudulent ? _self.isFraudulent : isFraudulent // ignore: cast_nullable_to_non_nullable
as bool,confidence: null == confidence ? _self.confidence : confidence // ignore: cast_nullable_to_non_nullable
as double,riskLevel: null == riskLevel ? _self.riskLevel : riskLevel // ignore: cast_nullable_to_non_nullable
as String,reasons: null == reasons ? _self.reasons : reasons // ignore: cast_nullable_to_non_nullable
as List<String>,patterns: null == patterns ? _self.patterns : patterns // ignore: cast_nullable_to_non_nullable
as List<SuspiciousPattern>,reviewContent: freezed == reviewContent ? _self.reviewContent : reviewContent // ignore: cast_nullable_to_non_nullable
as String?,author: freezed == author ? _self.author : author // ignore: cast_nullable_to_non_nullable
as String?,platform: freezed == platform ? _self.platform : platform // ignore: cast_nullable_to_non_nullable
as String?,timestamp: freezed == timestamp ? _self.timestamp : timestamp // ignore: cast_nullable_to_non_nullable
as DateTime?,
  ));
}


}

// dart format on
