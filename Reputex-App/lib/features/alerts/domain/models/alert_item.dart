import 'package:freezed_annotation/freezed_annotation.dart';

part 'alert_item.freezed.dart';
part 'alert_item.g.dart';

@freezed
abstract class AlertItem with _$AlertItem {
  const factory AlertItem({
    required String id,
    required String type,
    required String title,
    required String message,
    @Default('medium') String severity,
    required DateTime timestamp,
    @JsonKey(name: 'is_read') @Default(false) bool isRead,
    @JsonKey(name: 'reference_id') String? referenceId,
    @JsonKey(name: 'reference_type') String? referenceType,
  }) = _AlertItem;

  factory AlertItem.fromJson(Map<String, dynamic> json) =>
      _$AlertItemFromJson(json);
}
