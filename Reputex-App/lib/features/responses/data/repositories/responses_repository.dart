import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/network/api_client_interface.dart';
import '../../../../core/network/api_provider.dart';
import '../../domain/models/response_draft.dart';

final responsesRepositoryProvider = Provider<ResponsesRepository>((ref) {
  final api = ref.watch(apiServiceProvider);
  return ResponsesRepository(apiService: api);
});

class ResponsesRepository {
  ResponsesRepository({required IApiService apiService}) : _api = apiService;

  final IApiService _api;

  Future<ResponseDraft> generateResponse({
    required String mentionId,
    required String tone,
    String? customInstructions,
  }) {
    return _api.generateResponse(
      mentionId: mentionId,
      tone: tone,
      customInstructions: customInstructions,
    );
  }

  Future<List<ResponseDraft>> getResponses() => _api.getResponses();

  Future<ResponseDraft> getResponseById(String id) => _api.getResponseById(id);

  Future<ResponseDraft> approveResponse({
    required String id,
    required String responseText,
  }) {
    return _api.approveResponse(id: id, responseText: responseText);
  }

  Future<ResponseDraft> dispatchResponse(String id) =>
      _api.dispatchResponse(id);
}
