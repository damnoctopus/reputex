import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/fraud_repository.dart';
import '../../domain/models/fraud_result.dart';

final fraudReviewsProvider = FutureProvider<List<FraudResult>>((ref) async {
  final repo = ref.watch(fraudRepositoryProvider);
  return repo.getFraudReviews();
});

final fraudAnalysisProvider = FutureProvider.family<FraudResult, String>((
  ref,
  mentionId,
) async {
  final repo = ref.watch(fraudRepositoryProvider);
  return repo.getFraudAnalysis(mentionId);
});
