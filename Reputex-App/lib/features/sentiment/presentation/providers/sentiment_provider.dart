import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/sentiment_repository.dart';
import '../../domain/models/sentiment_analytics.dart';

final sentimentAnalyticsProvider = FutureProvider<SentimentAnalytics>((
  ref,
) async {
  final repo = ref.watch(sentimentRepositoryProvider);
  return repo.getSentimentAnalytics();
});
