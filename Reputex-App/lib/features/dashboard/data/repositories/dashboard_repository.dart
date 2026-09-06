import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/network/api_client_interface.dart';
import '../../../../core/network/api_provider.dart';
import '../../domain/models/dashboard_summary.dart';
import '../../domain/models/platform_statistics.dart';
import '../../domain/models/reputation_score.dart';
import '../../domain/models/sentiment_distribution.dart';
import '../../domain/models/sentiment_trend.dart';

final dashboardRepositoryProvider = Provider<DashboardRepository>((ref) {
  final api = ref.watch(apiServiceProvider);
  return DashboardRepository(apiService: api);
});

class DashboardRepository {
  DashboardRepository({required IApiService apiService}) : _api = apiService;

  final IApiService _api;

  Future<DashboardSummary> getDashboardSummary() => _api.getDashboardSummary();

  Future<ReputationScore> getReputationScore() => _api.getReputationScore();

  Future<SentimentDistribution> getSentimentDistribution() =>
      _api.getSentimentDistribution();

  Future<List<SentimentTrend>> getSentimentTrends({int days = 7}) =>
      _api.getSentimentTrends(days: days);

  Future<List<PlatformStatistics>> getPlatformStatistics() =>
      _api.getPlatformStatistics();
}
