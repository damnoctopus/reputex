import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/crisis_repository.dart';
import '../../domain/models/crisis_event.dart';

final crisisEventsProvider = FutureProvider<List<CrisisEvent>>((ref) async {
  final repo = ref.watch(crisisRepositoryProvider);
  return repo.getCrisisEvents();
});

final activeCrisisProvider = FutureProvider<CrisisEvent?>((ref) async {
  final repo = ref.watch(crisisRepositoryProvider);
  return repo.getActiveCrisis();
});

final crisisDetailProvider = FutureProvider.family<CrisisEvent, String>((
  ref,
  id,
) async {
  final repo = ref.watch(crisisRepositoryProvider);
  return repo.getCrisisById(id);
});
