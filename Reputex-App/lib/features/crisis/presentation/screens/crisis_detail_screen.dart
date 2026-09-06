import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../../../app/theme.dart';
import '../../../../core/widgets/error_widget.dart';
import '../../../../core/widgets/loading_indicator.dart';
import '../providers/crisis_provider.dart';

/// Crisis detail screen showing timeline, metrics, and suggested mitigation actions.
class CrisisDetailScreen extends ConsumerWidget {
  const CrisisDetailScreen({super.key, required this.crisisId});

  final String crisisId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final crisisAsync = ref.watch(crisisDetailProvider(crisisId));

    return Scaffold(
      appBar: AppBar(title: const Text('Crisis Details')),
      body: crisisAsync.when(
        loading: () => const Center(child: AppLoadingIndicator()),
        error: (err, _) => AppErrorWidget(
          message: err.toString(),
          onRetry: () => ref.refresh(crisisDetailProvider(crisisId)),
        ),
        data: (crisis) {
          final isResolved = crisis.status == 'resolved';
          final statusColor = isResolved
              ? AppColors.positive
              : AppColors.crisisRed;
          final dateFormat = DateFormat('MMM d, yyyy HH:mm');

          return SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.xl),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Status banner
                Container(
                  padding: const EdgeInsets.all(AppSpacing.base),
                  decoration: BoxDecoration(
                    color: statusColor.withValues(alpha: 0.08),
                    borderRadius: BorderRadius.circular(AppRadius.lg),
                    border: Border.all(
                      color: statusColor.withValues(alpha: 0.3),
                    ),
                  ),
                  child: Row(
                    children: [
                      Container(
                        width: 10,
                        height: 10,
                        decoration: BoxDecoration(
                          color: statusColor,
                          shape: BoxShape.circle,
                        ),
                      ),
                      const SizedBox(width: AppSpacing.sm),
                      Text(
                        isResolved
                            ? 'Resolved Crisis'
                            : 'Active Crisis (${crisis.severity.toUpperCase()})',
                        style: Theme.of(context).textTheme.titleMedium
                            ?.copyWith(
                              color: statusColor,
                              fontWeight: FontWeight.w600,
                            ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: AppSpacing.lg),

                Text(
                  crisis.title,
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const SizedBox(height: AppSpacing.sm),
                Text(
                  crisis.triggerReason,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: AppColors.textSecondaryDark,
                    height: 1.5,
                  ),
                ),
                const SizedBox(height: AppSpacing.xl),

                // Metrics
                Text(
                  'Crisis Metrics',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: AppSpacing.base),
                _MetricTile(
                  label: 'Velocity',
                  value: '${crisis.velocity.toStringAsFixed(1)} mentions/hr',
                ),
                _MetricTile(
                  label: 'Negative Mentions',
                  value: '${crisis.negativeMentionsCount}',
                ),
                _MetricTile(
                  label: 'Estimated Reach',
                  value: '${crisis.estimatedReach} users',
                ),
                _MetricTile(
                  label: 'Affected Platforms',
                  value: crisis.affectedPlatforms.join(', '),
                ),
                _MetricTile(
                  label: 'Started',
                  value: dateFormat.format(crisis.startedAt),
                ),
                if (crisis.resolvedAt != null)
                  _MetricTile(
                    label: 'Resolved',
                    value: dateFormat.format(crisis.resolvedAt!),
                  ),

                const SizedBox(height: AppSpacing.xxl),

                // Mitigation Actions
                if (crisis.suggestedActions.isNotEmpty) ...[
                  Text(
                    'Suggested Mitigation Actions',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: AppSpacing.base),
                  ...crisis.suggestedActions.map((action) {
                    return Padding(
                      padding: const EdgeInsets.only(bottom: AppSpacing.sm),
                      child: Container(
                        padding: const EdgeInsets.all(AppSpacing.base),
                        decoration: BoxDecoration(
                          color: AppColors.cardDark,
                          borderRadius: BorderRadius.circular(AppRadius.md),
                          border: Border.all(color: AppColors.glassBorder),
                        ),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Icon(
                              Icons.lightbulb_outline_rounded,
                              color: AppColors.accentWarning,
                              size: 18,
                            ),
                            const SizedBox(width: AppSpacing.sm),
                            Expanded(
                              child: Text(
                                action,
                                style: Theme.of(context).textTheme.bodyMedium,
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  }),
                ],
              ],
            ),
          );
        },
      ),
    );
  }
}

class _MetricTile extends StatelessWidget {
  const _MetricTile({required this.label, required this.value});
  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppSpacing.md),
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.base),
        decoration: BoxDecoration(
          color: AppColors.cardDark,
          borderRadius: BorderRadius.circular(AppRadius.md),
          border: Border.all(color: AppColors.glassBorder),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: Theme.of(context).textTheme.bodyMedium),
            Text(
              value,
              style: Theme.of(context).textTheme.bodyLarge
                  ?.copyWith(fontWeight: FontWeight.w600),
            ),
          ],
        ),
      ),
    );
  }
}
