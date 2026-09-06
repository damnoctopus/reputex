import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/network/api_client_interface.dart';
import '../../../../core/network/api_provider.dart';
import '../../domain/models/fraud_result.dart';

final fraudRepositoryProvider = Provider<FraudRepository>((ref) {
  final api = ref.watch(apiServiceProvider);
  return FraudRepository(apiService: api);
});

class FraudRepository {
  FraudRepository({required IApiService apiService}) : _api = apiService;

  final IApiService _api;

  Future<List<FraudResult>> getFraudReviews() => _api.getFraudReviews();

  Future<FraudResult> getFraudAnalysis(String mentionId) =>
      _api.getFraudAnalysis(mentionId);
}
