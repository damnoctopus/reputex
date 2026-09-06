import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/network/api_client_interface.dart';
import '../../../../core/network/api_provider.dart';
import '../../domain/models/alert_item.dart';

final alertsRepositoryProvider = Provider<AlertsRepository>((ref) {
  final api = ref.watch(apiServiceProvider);
  return AlertsRepository(apiService: api);
});

class AlertsRepository {
  AlertsRepository({required IApiService apiService}) : _api = apiService;

  final IApiService _api;

  Future<List<AlertItem>> getAlerts() => _api.getAlerts();

  Future<void> markAlertAsRead(String id) => _api.markAlertAsRead(id);
}
