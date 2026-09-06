import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/responses_repository.dart';
import '../../domain/models/response_draft.dart';

class AiResponseNotifier extends StateNotifier<AsyncValue<ResponseDraft?>> {
  AiResponseNotifier({
    required this.repository,
    required this.mentionId,
  }) : super(const AsyncValue.data(null));

  final ResponsesRepository repository;
  final String mentionId;

  Future<void> generate({
    required String tone,
    String? customInstructions,
  }) async {
    state = const AsyncValue.loading();
    try {
      final draft = await repository.generateResponse(
        mentionId: mentionId,
        tone: tone,
        customInstructions: customInstructions,
      );
      state = AsyncValue.data(draft);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<bool> approve({required String text}) async {
    final current = state.valueOrNull;
    if (current == null) return false;

    state = const AsyncValue.loading();
    try {
      final approved = await repository.approveResponse(
        id: current.id,
        responseText: text,
      );
      state = AsyncValue.data(approved);
      return true;
    } catch (e, st) {
      state = AsyncValue.error(e, st);
      return false;
    }
  }

  Future<bool> dispatch() async {
    final current = state.valueOrNull;
    if (current == null) return false;

    state = const AsyncValue.loading();
    try {
      final dispatched = await repository.dispatchResponse(current.id);
      state = AsyncValue.data(dispatched);
      return true;
    } catch (e, st) {
      state = AsyncValue.error(e, st);
      return false;
    }
  }
}

final aiResponseProvider =
    StateNotifierProvider.family<
      AiResponseNotifier,
      AsyncValue<ResponseDraft?>,
      String
    >((ref, mentionId) {
      final repo = ref.watch(responsesRepositoryProvider);
      return AiResponseNotifier(repository: repo, mentionId: mentionId);
    });
