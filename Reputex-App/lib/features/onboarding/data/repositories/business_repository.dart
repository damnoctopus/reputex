import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/network/api_client_interface.dart';
import '../../../../core/network/api_provider.dart';
import '../../domain/models/brand_keyword.dart';
import '../../domain/models/business.dart';

final businessRepositoryProvider = Provider<BusinessRepository>((ref) {
  final api = ref.watch(apiServiceProvider);
  return BusinessRepository(apiService: api);
});

class BusinessRepository {
  BusinessRepository({required IApiService apiService}) : _api = apiService;

  final IApiService _api;

  Future<Business?> getBusiness() => _api.getBusiness();

  Future<Business> setupBusiness({
    required String name,
    required String category,
    String? website,
    String? location,
    String? phone,
    required List<String> keywords,
    required List<String> platforms,
  }) {
    return _api.setupBusiness(
      name: name,
      category: category,
      website: website,
      location: location,
      phone: phone,
      keywords: keywords,
      platforms: platforms,
    );
  }

  Future<List<BrandKeyword>> getKeywords() => _api.getKeywords();

  Future<BrandKeyword> addKeyword({
    required String keyword,
    String category = 'brand',
  }) {
    return _api.addKeyword(keyword: keyword, category: category);
  }

  Future<void> deleteKeyword(String id) => _api.deleteKeyword(id);
}
