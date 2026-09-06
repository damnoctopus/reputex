import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/network/api_client_interface.dart';
import '../../../../core/network/api_provider.dart';
import '../../domain/models/crisis_event.dart';

final crisisRepositoryProvider = Provider<CrisisRepository>((ref) {
  final api = ref.watch(apiServiceProvider);
  return CrisisRepository(apiService: api);
});

class CrisisRepository {
  CrisisRepository({required IApiService apiService}) : _api = apiService;

  final IApiService _api;

  Future<List<CrisisEvent>> getCrisisEvents() => _api.getCrisisEvents();

  Future<CrisisEvent?> getActiveCrisis() => _api.getActiveCrisis();

  Future<CrisisEvent> getCrisisById(String id) => _api.getCrisisById(id);
}
