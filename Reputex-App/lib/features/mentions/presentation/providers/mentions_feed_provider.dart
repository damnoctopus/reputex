import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/mentions_repository.dart';
import '../../domain/models/mention.dart';
import '../../domain/models/mentions_filter.dart';

class MentionsFeedState {
  const MentionsFeedState({
    this.filter = const MentionsFilter(),
    this.items = const [],
    this.isLoading = false,
    this.isLoadingMore = false,
    this.hasMore = false,
    this.totalCount = 0,
    this.errorMessage,
  });

  final MentionsFilter filter;
  final List<Mention> items;
  final bool isLoading;
  final bool isLoadingMore;
  final bool hasMore;
  final int totalCount;
  final String? errorMessage;

  MentionsFeedState copyWith({
    MentionsFilter? filter,
    List<Mention>? items,
    bool? isLoading,
    bool? isLoadingMore,
    bool? hasMore,
    int? totalCount,
    String? errorMessage,
    bool clearError = false,
  }) {
    return MentionsFeedState(
      filter: filter ?? this.filter,
      items: items ?? this.items,
      isLoading: isLoading ?? this.isLoading,
      isLoadingMore: isLoadingMore ?? this.isLoadingMore,
      hasMore: hasMore ?? this.hasMore,
      totalCount: totalCount ?? this.totalCount,
      errorMessage: clearError ? null : (errorMessage ?? this.errorMessage),
    );
  }
}

class MentionsFeedNotifier extends StateNotifier<MentionsFeedState> {
  MentionsFeedNotifier({required this.repository})
    : super(const MentionsFeedState()) {
    fetchMentions();
  }

  final MentionsRepository repository;

  Future<void> fetchMentions({MentionsFilter? newFilter}) async {
    final filterToUse = (newFilter ?? state.filter).copyWith(page: 1);
    state = state.copyWith(
      filter: filterToUse,
      isLoading: true,
      clearError: true,
    );

    try {
      final result = await repository.getMentions(filter: filterToUse);
      state = state.copyWith(
        items: result.items,
        isLoading: false,
        hasMore: result.hasMore,
        totalCount: result.totalCount,
      );
    } catch (e) {
      state = state.copyWith(isLoading: false, errorMessage: e.toString());
    }
  }

  Future<void> loadMore() async {
    if (state.isLoadingMore || !state.hasMore || state.isLoading) return;

    state = state.copyWith(isLoadingMore: true);
    final nextPage = state.filter.page + 1;
    final nextFilter = state.filter.copyWith(page: nextPage);

    try {
      final result = await repository.getMentions(filter: nextFilter);
      state = state.copyWith(
        filter: nextFilter,
        items: [...state.items, ...result.items],
        isLoadingMore: false,
        hasMore: result.hasMore,
        totalCount: result.totalCount,
      );
    } catch (e) {
      state = state.copyWith(isLoadingMore: false, errorMessage: e.toString());
    }
  }

  Future<void> refresh() async {
    await fetchMentions();
  }

  void setPlatform(String? platform) {
    fetchMentions(newFilter: state.filter.copyWith(platform: platform));
  }

  void setSentiment(String? sentiment) {
    fetchMentions(newFilter: state.filter.copyWith(sentiment: sentiment));
  }

  void setFakeOnly(bool? isFake) {
    fetchMentions(newFilter: state.filter.copyWith(isFake: isFake));
  }

  void setSearchQuery(String query) {
    fetchMentions(newFilter: state.filter.copyWith(searchQuery: query));
  }
}

final mentionsFeedProvider =
    StateNotifierProvider<MentionsFeedNotifier, MentionsFeedState>((ref) {
      final repo = ref.watch(mentionsRepositoryProvider);
      return MentionsFeedNotifier(repository: repo);
    });

final mentionDetailProvider = FutureProvider.family<Mention, String>((
  ref,
  id,
) async {
  final repo = ref.watch(mentionsRepositoryProvider);
  return repo.getMentionById(id);
});
