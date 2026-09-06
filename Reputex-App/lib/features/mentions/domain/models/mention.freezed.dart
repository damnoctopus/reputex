// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'mention.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$Mention {

 String get id; String get platform; String get author; String get content; String get sentiment;@JsonKey(name: 'sentiment_score') double get sentimentScore;@JsonKey(name: 'is_fake') bool get isFake;@JsonKey(name: 'fraud_confidence') double? get fraudConfidence; String? get url; DateTime get timestamp; MentionEngagement get engagement; double? get rating;@JsonKey(name: 'response_status') String get responseStatus;@JsonKey(name: 'response_text') String? get responseText;@JsonKey(name: 'author_avatar') String? get authorAvatar;
/// Create a copy of Mention
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$MentionCopyWith<Mention> get copyWith => _$MentionCopyWithImpl<Mention>(this as Mention, _$identity);

  /// Serializes this Mention to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is Mention&&(identical(other.id, id) || other.id == id)&&(identical(other.platform, platform) || other.platform == platform)&&(identical(other.author, author) || other.author == author)&&(identical(other.content, content) || other.content == content)&&(identical(other.sentiment, sentiment) || other.sentiment == sentiment)&&(identical(other.sentimentScore, sentimentScore) || other.sentimentScore == sentimentScore)&&(identical(other.isFake, isFake) || other.isFake == isFake)&&(identical(other.fraudConfidence, fraudConfidence) || other.fraudConfidence == fraudConfidence)&&(identical(other.url, url) || other.url == url)&&(identical(other.timestamp, timestamp) || other.timestamp == timestamp)&&(identical(other.engagement, engagement) || other.engagement == engagement)&&(identical(other.rating, rating) || other.rating == rating)&&(identical(other.responseStatus, responseStatus) || other.responseStatus == responseStatus)&&(identical(other.responseText, responseText) || other.responseText == responseText)&&(identical(other.authorAvatar, authorAvatar) || other.authorAvatar == authorAvatar));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,platform,author,content,sentiment,sentimentScore,isFake,fraudConfidence,url,timestamp,engagement,rating,responseStatus,responseText,authorAvatar);

@override
String toString() {
  return 'Mention(id: $id, platform: $platform, author: $author, content: $content, sentiment: $sentiment, sentimentScore: $sentimentScore, isFake: $isFake, fraudConfidence: $fraudConfidence, url: $url, timestamp: $timestamp, engagement: $engagement, rating: $rating, responseStatus: $responseStatus, responseText: $responseText, authorAvatar: $authorAvatar)';
}


}

/// @nodoc
abstract mixin class $MentionCopyWith<$Res>  {
  factory $MentionCopyWith(Mention value, $Res Function(Mention) _then) = _$MentionCopyWithImpl;
@useResult
$Res call({
 String id, String platform, String author, String content, String sentiment,@JsonKey(name: 'sentiment_score') double sentimentScore,@JsonKey(name: 'is_fake') bool isFake,@JsonKey(name: 'fraud_confidence') double? fraudConfidence, String? url, DateTime timestamp, MentionEngagement engagement, double? rating,@JsonKey(name: 'response_status') String responseStatus,@JsonKey(name: 'response_text') String? responseText,@JsonKey(name: 'author_avatar') String? authorAvatar
});


$MentionEngagementCopyWith<$Res> get engagement;

}
/// @nodoc
class _$MentionCopyWithImpl<$Res>
    implements $MentionCopyWith<$Res> {
  _$MentionCopyWithImpl(this._self, this._then);

  final Mention _self;
  final $Res Function(Mention) _then;

/// Create a copy of Mention
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? platform = null,Object? author = null,Object? content = null,Object? sentiment = null,Object? sentimentScore = null,Object? isFake = null,Object? fraudConfidence = freezed,Object? url = freezed,Object? timestamp = null,Object? engagement = null,Object? rating = freezed,Object? responseStatus = null,Object? responseText = freezed,Object? authorAvatar = freezed,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,platform: null == platform ? _self.platform : platform // ignore: cast_nullable_to_non_nullable
as String,author: null == author ? _self.author : author // ignore: cast_nullable_to_non_nullable
as String,content: null == content ? _self.content : content // ignore: cast_nullable_to_non_nullable
as String,sentiment: null == sentiment ? _self.sentiment : sentiment // ignore: cast_nullable_to_non_nullable
as String,sentimentScore: null == sentimentScore ? _self.sentimentScore : sentimentScore // ignore: cast_nullable_to_non_nullable
as double,isFake: null == isFake ? _self.isFake : isFake // ignore: cast_nullable_to_non_nullable
as bool,fraudConfidence: freezed == fraudConfidence ? _self.fraudConfidence : fraudConfidence // ignore: cast_nullable_to_non_nullable
as double?,url: freezed == url ? _self.url : url // ignore: cast_nullable_to_non_nullable
as String?,timestamp: null == timestamp ? _self.timestamp : timestamp // ignore: cast_nullable_to_non_nullable
as DateTime,engagement: null == engagement ? _self.engagement : engagement // ignore: cast_nullable_to_non_nullable
as MentionEngagement,rating: freezed == rating ? _self.rating : rating // ignore: cast_nullable_to_non_nullable
as double?,responseStatus: null == responseStatus ? _self.responseStatus : responseStatus // ignore: cast_nullable_to_non_nullable
as String,responseText: freezed == responseText ? _self.responseText : responseText // ignore: cast_nullable_to_non_nullable
as String?,authorAvatar: freezed == authorAvatar ? _self.authorAvatar : authorAvatar // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}
/// Create a copy of Mention
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$MentionEngagementCopyWith<$Res> get engagement {
  
  return $MentionEngagementCopyWith<$Res>(_self.engagement, (value) {
    return _then(_self.copyWith(engagement: value));
  });
}
}


/// Adds pattern-matching-related methods to [Mention].
extension MentionPatterns on Mention {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _Mention value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _Mention() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _Mention value)  $default,){
final _that = this;
switch (_that) {
case _Mention():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _Mention value)?  $default,){
final _that = this;
switch (_that) {
case _Mention() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String platform,  String author,  String content,  String sentiment, @JsonKey(name: 'sentiment_score')  double sentimentScore, @JsonKey(name: 'is_fake')  bool isFake, @JsonKey(name: 'fraud_confidence')  double? fraudConfidence,  String? url,  DateTime timestamp,  MentionEngagement engagement,  double? rating, @JsonKey(name: 'response_status')  String responseStatus, @JsonKey(name: 'response_text')  String? responseText, @JsonKey(name: 'author_avatar')  String? authorAvatar)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _Mention() when $default != null:
return $default(_that.id,_that.platform,_that.author,_that.content,_that.sentiment,_that.sentimentScore,_that.isFake,_that.fraudConfidence,_that.url,_that.timestamp,_that.engagement,_that.rating,_that.responseStatus,_that.responseText,_that.authorAvatar);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String platform,  String author,  String content,  String sentiment, @JsonKey(name: 'sentiment_score')  double sentimentScore, @JsonKey(name: 'is_fake')  bool isFake, @JsonKey(name: 'fraud_confidence')  double? fraudConfidence,  String? url,  DateTime timestamp,  MentionEngagement engagement,  double? rating, @JsonKey(name: 'response_status')  String responseStatus, @JsonKey(name: 'response_text')  String? responseText, @JsonKey(name: 'author_avatar')  String? authorAvatar)  $default,) {final _that = this;
switch (_that) {
case _Mention():
return $default(_that.id,_that.platform,_that.author,_that.content,_that.sentiment,_that.sentimentScore,_that.isFake,_that.fraudConfidence,_that.url,_that.timestamp,_that.engagement,_that.rating,_that.responseStatus,_that.responseText,_that.authorAvatar);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String platform,  String author,  String content,  String sentiment, @JsonKey(name: 'sentiment_score')  double sentimentScore, @JsonKey(name: 'is_fake')  bool isFake, @JsonKey(name: 'fraud_confidence')  double? fraudConfidence,  String? url,  DateTime timestamp,  MentionEngagement engagement,  double? rating, @JsonKey(name: 'response_status')  String responseStatus, @JsonKey(name: 'response_text')  String? responseText, @JsonKey(name: 'author_avatar')  String? authorAvatar)?  $default,) {final _that = this;
switch (_that) {
case _Mention() when $default != null:
return $default(_that.id,_that.platform,_that.author,_that.content,_that.sentiment,_that.sentimentScore,_that.isFake,_that.fraudConfidence,_that.url,_that.timestamp,_that.engagement,_that.rating,_that.responseStatus,_that.responseText,_that.authorAvatar);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _Mention implements Mention {
  const _Mention({required this.id, required this.platform, required this.author, required this.content, required this.sentiment, @JsonKey(name: 'sentiment_score') this.sentimentScore = 0.0, @JsonKey(name: 'is_fake') this.isFake = false, @JsonKey(name: 'fraud_confidence') this.fraudConfidence, this.url, required this.timestamp, this.engagement = const MentionEngagement(), this.rating, @JsonKey(name: 'response_status') this.responseStatus = 'none', @JsonKey(name: 'response_text') this.responseText, @JsonKey(name: 'author_avatar') this.authorAvatar});
  factory _Mention.fromJson(Map<String, dynamic> json) => _$MentionFromJson(json);

@override final  String id;
@override final  String platform;
@override final  String author;
@override final  String content;
@override final  String sentiment;
@override@JsonKey(name: 'sentiment_score') final  double sentimentScore;
@override@JsonKey(name: 'is_fake') final  bool isFake;
@override@JsonKey(name: 'fraud_confidence') final  double? fraudConfidence;
@override final  String? url;
@override final  DateTime timestamp;
@override@JsonKey() final  MentionEngagement engagement;
@override final  double? rating;
@override@JsonKey(name: 'response_status') final  String responseStatus;
@override@JsonKey(name: 'response_text') final  String? responseText;
@override@JsonKey(name: 'author_avatar') final  String? authorAvatar;

/// Create a copy of Mention
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$MentionCopyWith<_Mention> get copyWith => __$MentionCopyWithImpl<_Mention>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$MentionToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _Mention&&(identical(other.id, id) || other.id == id)&&(identical(other.platform, platform) || other.platform == platform)&&(identical(other.author, author) || other.author == author)&&(identical(other.content, content) || other.content == content)&&(identical(other.sentiment, sentiment) || other.sentiment == sentiment)&&(identical(other.sentimentScore, sentimentScore) || other.sentimentScore == sentimentScore)&&(identical(other.isFake, isFake) || other.isFake == isFake)&&(identical(other.fraudConfidence, fraudConfidence) || other.fraudConfidence == fraudConfidence)&&(identical(other.url, url) || other.url == url)&&(identical(other.timestamp, timestamp) || other.timestamp == timestamp)&&(identical(other.engagement, engagement) || other.engagement == engagement)&&(identical(other.rating, rating) || other.rating == rating)&&(identical(other.responseStatus, responseStatus) || other.responseStatus == responseStatus)&&(identical(other.responseText, responseText) || other.responseText == responseText)&&(identical(other.authorAvatar, authorAvatar) || other.authorAvatar == authorAvatar));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,platform,author,content,sentiment,sentimentScore,isFake,fraudConfidence,url,timestamp,engagement,rating,responseStatus,responseText,authorAvatar);

@override
String toString() {
  return 'Mention(id: $id, platform: $platform, author: $author, content: $content, sentiment: $sentiment, sentimentScore: $sentimentScore, isFake: $isFake, fraudConfidence: $fraudConfidence, url: $url, timestamp: $timestamp, engagement: $engagement, rating: $rating, responseStatus: $responseStatus, responseText: $responseText, authorAvatar: $authorAvatar)';
}


}

/// @nodoc
abstract mixin class _$MentionCopyWith<$Res> implements $MentionCopyWith<$Res> {
  factory _$MentionCopyWith(_Mention value, $Res Function(_Mention) _then) = __$MentionCopyWithImpl;
@override @useResult
$Res call({
 String id, String platform, String author, String content, String sentiment,@JsonKey(name: 'sentiment_score') double sentimentScore,@JsonKey(name: 'is_fake') bool isFake,@JsonKey(name: 'fraud_confidence') double? fraudConfidence, String? url, DateTime timestamp, MentionEngagement engagement, double? rating,@JsonKey(name: 'response_status') String responseStatus,@JsonKey(name: 'response_text') String? responseText,@JsonKey(name: 'author_avatar') String? authorAvatar
});


@override $MentionEngagementCopyWith<$Res> get engagement;

}
/// @nodoc
class __$MentionCopyWithImpl<$Res>
    implements _$MentionCopyWith<$Res> {
  __$MentionCopyWithImpl(this._self, this._then);

  final _Mention _self;
  final $Res Function(_Mention) _then;

/// Create a copy of Mention
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? platform = null,Object? author = null,Object? content = null,Object? sentiment = null,Object? sentimentScore = null,Object? isFake = null,Object? fraudConfidence = freezed,Object? url = freezed,Object? timestamp = null,Object? engagement = null,Object? rating = freezed,Object? responseStatus = null,Object? responseText = freezed,Object? authorAvatar = freezed,}) {
  return _then(_Mention(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,platform: null == platform ? _self.platform : platform // ignore: cast_nullable_to_non_nullable
as String,author: null == author ? _self.author : author // ignore: cast_nullable_to_non_nullable
as String,content: null == content ? _self.content : content // ignore: cast_nullable_to_non_nullable
as String,sentiment: null == sentiment ? _self.sentiment : sentiment // ignore: cast_nullable_to_non_nullable
as String,sentimentScore: null == sentimentScore ? _self.sentimentScore : sentimentScore // ignore: cast_nullable_to_non_nullable
as double,isFake: null == isFake ? _self.isFake : isFake // ignore: cast_nullable_to_non_nullable
as bool,fraudConfidence: freezed == fraudConfidence ? _self.fraudConfidence : fraudConfidence // ignore: cast_nullable_to_non_nullable
as double?,url: freezed == url ? _self.url : url // ignore: cast_nullable_to_non_nullable
as String?,timestamp: null == timestamp ? _self.timestamp : timestamp // ignore: cast_nullable_to_non_nullable
as DateTime,engagement: null == engagement ? _self.engagement : engagement // ignore: cast_nullable_to_non_nullable
as MentionEngagement,rating: freezed == rating ? _self.rating : rating // ignore: cast_nullable_to_non_nullable
as double?,responseStatus: null == responseStatus ? _self.responseStatus : responseStatus // ignore: cast_nullable_to_non_nullable
as String,responseText: freezed == responseText ? _self.responseText : responseText // ignore: cast_nullable_to_non_nullable
as String?,authorAvatar: freezed == authorAvatar ? _self.authorAvatar : authorAvatar // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}

/// Create a copy of Mention
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$MentionEngagementCopyWith<$Res> get engagement {
  
  return $MentionEngagementCopyWith<$Res>(_self.engagement, (value) {
    return _then(_self.copyWith(engagement: value));
  });
}
}

// dart format on
