import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/business_repository.dart';
import '../../domain/models/business.dart';

class BusinessStateNotifier extends StateNotifier<AsyncValue<Business?>> {
  BusinessStateNotifier({required this.repository})
    : super(const AsyncValue.loading()) {
    loadBusiness();
  }

  final BusinessRepository repository;

  Future<void> loadBusiness() async {
    state = const AsyncValue.loading();
    try {
      final business = await repository.getBusiness();
      state = AsyncValue.data(business);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<bool> setupBusiness({
    required String name,
    required String category,
    String? website,
    String? location,
    String? phone,
    required List<String> keywords,
    required List<String> platforms,
  }) async {
    state = const AsyncValue.loading();
    try {
      final business = await repository.setupBusiness(
        name: name,
        category: category,
        website: website,
        location: location,
        phone: phone,
        keywords: keywords,
        platforms: platforms,
      );
      state = AsyncValue.data(business);
      return true;
    } catch (e, st) {
      state = AsyncValue.error(e, st);
      return false;
    }
  }
}

final businessProvider =
    StateNotifierProvider<BusinessStateNotifier, AsyncValue<Business?>>((ref) {
      final repo = ref.watch(businessRepositoryProvider);
      return BusinessStateNotifier(repository: repo);
    });
