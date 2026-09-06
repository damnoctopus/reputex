import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/network/api_client_interface.dart';
import '../../../../core/network/api_provider.dart';
import '../../domain/models/sentiment_analytics.dart';

final sentimentRepositoryProvider = Provider<SentimentRepository>((ref) {
  final api = ref.watch(apiServiceProvider);
  return SentimentRepository(apiService: api);
});

class SentimentRepository {
  SentimentRepository({required IApiService apiService}) : _api = apiService;

  final IApiService _api;

  Future<SentimentAnalytics> getSentimentAnalytics() =>
      _api.getSentimentAnalytics();
}
