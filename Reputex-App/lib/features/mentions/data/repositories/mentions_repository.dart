import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/network/api_client_interface.dart';
import '../../../../core/network/api_provider.dart';
import '../../domain/models/mention.dart';
import '../../domain/models/mentions_filter.dart';
import '../../domain/models/paginated_mentions.dart';

final mentionsRepositoryProvider = Provider<MentionsRepository>((ref) {
  final api = ref.watch(apiServiceProvider);
  return MentionsRepository(apiService: api);
});

class MentionsRepository {
  MentionsRepository({required IApiService apiService}) : _api = apiService;

  final IApiService _api;

  Future<PaginatedMentions> getMentions({
    MentionsFilter filter = const MentionsFilter(),
  }) {
    return _api.getMentions(filter: filter);
  }

  Future<Mention> getMentionById(String id) => _api.getMentionById(id);
}
