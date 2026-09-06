import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/dashboard_repository.dart';
import '../../domain/models/dashboard_summary.dart';

class DashboardNotifier extends StateNotifier<AsyncValue<DashboardSummary>> {
  DashboardNotifier({required this.repository})
    : super(const AsyncValue.loading()) {
    fetchDashboard();
  }

  final DashboardRepository repository;

  Future<void> fetchDashboard() async {
    state = const AsyncValue.loading();
    try {
      final summary = await repository.getDashboardSummary();
      state = AsyncValue.data(summary);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> refresh() async {
    try {
      final summary = await repository.getDashboardSummary();
      state = AsyncValue.data(summary);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
}

final dashboardProvider =
    StateNotifierProvider<DashboardNotifier, AsyncValue<DashboardSummary>>((
      ref,
    ) {
      final repo = ref.watch(dashboardRepositoryProvider);
      return DashboardNotifier(repository: repo);
    });
