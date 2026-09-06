import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/theme.dart';
import '../../../../core/widgets/empty_state_widget.dart';
import '../../../../core/widgets/error_widget.dart';
import '../../../../core/widgets/loading_indicator.dart';
import '../../../../core/widgets/platform_icon.dart';
import '../../../../core/widgets/sentiment_badge.dart';
import '../../domain/models/mention.dart';
import '../providers/mentions_feed_provider.dart';

/// Mentions feed screen with filters, pagination, and shared state widgets.
class MentionsScreen extends ConsumerStatefulWidget {
  const MentionsScreen({super.key});

  @override
  ConsumerState<MentionsScreen> createState() => _MentionsScreenState();
}

class _MentionsScreenState extends ConsumerState<MentionsScreen> {
  final _scrollController = ScrollController();
  String _selectedFilter = 'All';

  static const _filters = ['All', 'Positive', 'Neutral', 'Negative', 'Fake'];

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
  }

  void _onScroll() {
    if (_scrollController.position.pixels >=
        _scrollController.position.maxScrollExtent - 200) {
      ref.read(mentionsFeedProvider.notifier).loadMore();
    }
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _onFilterSelected(String filter) {
    setState(() => _selectedFilter = filter);
    final notifier = ref.read(mentionsFeedProvider.notifier);

    if (filter == 'All') {
      notifier.setSentiment(null);
      notifier.setFakeOnly(null);
    } else if (filter == 'Fake') {
      notifier.setSentiment(null);
      notifier.setFakeOnly(true);
    } else {
      notifier.setFakeOnly(null);
      notifier.setSentiment(filter.toLowerCase());
    }
  }

  @override
  Widget build(BuildContext context) {
    final feedState = ref.watch(mentionsFeedProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Reviews & Mentions')),
      body: Column(
        children: [
          // ── Filter Chips ──
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.xl,
              vertical: AppSpacing.sm,
            ),
            child: Row(
              children: _filters.map((filter) {
                final isSelected = filter == _selectedFilter;
                return Padding(
                  padding: const EdgeInsets.only(right: AppSpacing.sm),
                  child: FilterChip(
                    label: Text(filter),
                    selected: isSelected,
                    onSelected: (_) => _onFilterSelected(filter),
                    selectedColor: AppColors.primary.withValues(alpha: 0.2),
                    checkmarkColor: AppColors.primary,
                    labelStyle: TextStyle(
                      color: isSelected
                          ? AppColors.primary
                          : AppColors.textSecondaryDark,
                      fontWeight: isSelected
                          ? FontWeight.w600
                          : FontWeight.normal,
                    ),
                  ),
                );
              }).toList(),
            ),
          ),

          // ── Mention List ──
          Expanded(
            child: Builder(
              builder: (context) {
                if (feedState.isLoading && feedState.items.isEmpty) {
                  return const Padding(
                    padding: EdgeInsets.all(AppSpacing.xl),
                    child: Column(
                      children: [
                        ShimmerCard(height: 120),
                        SizedBox(height: AppSpacing.md),
                        ShimmerCard(height: 120),
                        SizedBox(height: AppSpacing.md),
                        ShimmerCard(height: 120),
                      ],
                    ),
                  );
                }

                if (feedState.errorMessage != null && feedState.items.isEmpty) {
                  return AppErrorWidget(
                    message: feedState.errorMessage!,
                    onRetry: () =>
                        ref.read(mentionsFeedProvider.notifier).refresh(),
                  );
                }

                if (feedState.items.isEmpty) {
                  return EmptyStateWidget(
                    icon: Icons.reviews_outlined,
                    message: 'No mentions found',
                    subtitle: 'No reviews or mentions match the current filter selection.',
                    action: ElevatedButton(
                      onPressed: () => _onFilterSelected('All'),
                      child: const Text('Reset Filters'),
                    ),
                  );
                }

                return RefreshIndicator(
                  onRefresh: () =>
                      ref.read(mentionsFeedProvider.notifier).refresh(),
                  child: ListView.separated(
                    controller: _scrollController,
                    physics: const AlwaysScrollableScrollPhysics(),
                    padding: const EdgeInsets.all(AppSpacing.xl),
                    itemCount:
                        feedState.items.length +
                        (feedState.isLoadingMore ? 1 : 0),
                    separatorBuilder: (_, _) =>
                        const SizedBox(height: AppSpacing.md),
                    itemBuilder: (context, index) {
                      if (index == feedState.items.length) {
                        return const Center(
                          child: Padding(
                            padding: EdgeInsets.all(AppSpacing.base),
                            child: SizedBox(
                              width: 24,
                              height: 24,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            ),
                          ),
                        );
                      }

                      final mention = feedState.items[index];
                      return _MentionCard(
                        mention: mention,
                        onTap: () => context.push('/mentions/${mention.id}'),
                      );
                    },
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _MentionCard extends StatelessWidget {
  const _MentionCard({required this.mention, required this.onTap});

  final Mention mention;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: AppColors.cardDark,
      borderRadius: BorderRadius.circular(AppRadius.lg),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        child: Container(
          padding: const EdgeInsets.all(AppSpacing.base),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(AppRadius.lg),
            border: Border.all(color: AppColors.glassBorder),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  PlatformIcon(platform: mention.platform, showLabel: true),
                  const Spacer(),
                  if (mention.isFake)
                    Padding(
                      padding: const EdgeInsets.only(right: AppSpacing.sm),
                      child: Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: AppSpacing.sm,
                          vertical: 2,
                        ),
                        decoration: BoxDecoration(
                          color: AppColors.suspicious.withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(AppRadius.full),
                        ),
                        child: const Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(
                              Icons.warning_amber_rounded,
                              size: 12,
                              color: AppColors.suspicious,
                            ),
                            SizedBox(width: 4),
                            Text(
                              'Suspicious',
                              style: TextStyle(
                                color: AppColors.suspicious,
                                fontSize: 10,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  Text(
                    _formatTimeAgo(mention.timestamp),
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
              const SizedBox(height: AppSpacing.md),
              Text(
                '"${mention.content}"',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: AppColors.textPrimaryDark,
                  fontStyle: FontStyle.italic,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: AppSpacing.md),
              Row(
                children: [
                  SentimentBadge(
                    sentiment: mention.sentiment,
                    confidence: mention.sentimentScore.abs(),
                    compact: true,
                  ),
                  if (mention.responseStatus != 'none') ...[
                    const SizedBox(width: AppSpacing.sm),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: AppSpacing.sm,
                        vertical: 2,
                      ),
                      decoration: BoxDecoration(
                        color: AppColors.primary.withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(AppRadius.full),
                      ),
                      child: Text(
                        mention.responseStatus.toUpperCase(),
                        style: const TextStyle(
                          color: AppColors.primaryLight,
                          fontSize: 9,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ),
                  ],
                  const Spacer(),
                  const Icon(
                    Icons.chevron_right_rounded,
                    color: AppColors.textTertiaryDark,
                    size: 20,
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  static String _formatTimeAgo(DateTime timestamp) {
    final diff = DateTime.now().difference(timestamp);
    if (diff.inMinutes < 60) return '${diff.inMinutes}m ago';
    if (diff.inHours < 24) return '${diff.inHours}h ago';
    return '${diff.inDays}d ago';
  }
}
