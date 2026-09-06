import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/alerts_repository.dart';
import '../../domain/models/alert_item.dart';

class AlertsNotifier extends StateNotifier<AsyncValue<List<AlertItem>>> {
  AlertsNotifier({required this.repository})
    : super(const AsyncValue.loading()) {
    fetchAlerts();
  }

  final AlertsRepository repository;

  Future<void> fetchAlerts() async {
    state = const AsyncValue.loading();
    try {
      final alerts = await repository.getAlerts();
      state = AsyncValue.data(alerts);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> markAsRead(String id) async {
    final currentList = state.valueOrNull;
    if (currentList != null) {
      final updated = currentList.map((a) {
        if (a.id == id) {
          return a.copyWith(isRead: true);
        }
        return a;
      }).toList();
      state = AsyncValue.data(updated);
    }
    await repository.markAlertAsRead(id);
  }
}

final alertsProvider =
    StateNotifierProvider<AlertsNotifier, AsyncValue<List<AlertItem>>>((ref) {
      final repo = ref.watch(alertsRepositoryProvider);
      return AlertsNotifier(repository: repo);
    });
