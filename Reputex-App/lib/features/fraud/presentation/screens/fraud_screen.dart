import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/theme.dart';
import '../../../../core/widgets/empty_state_widget.dart';
import '../../../../core/widgets/error_widget.dart';
import '../../../../core/widgets/loading_indicator.dart';
import '../providers/fraud_provider.dart';

/// Fake review detection screen with risk-categorized list.
class FraudScreen extends ConsumerWidget {
  const FraudScreen({super.key});

  static Color _riskColor(String risk) {
    switch (risk.toLowerCase()) {
      case 'critical':
        return AppColors.riskCritical;
      case 'high':
        return AppColors.riskHigh;
      case 'medium':
        return AppColors.riskMedium;
      case 'low':
        return AppColors.riskLow;
      default:
        return AppColors.neutral;
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final fraudAsync = ref.watch(fraudReviewsProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Suspicious Reviews')),
      body: fraudAsync.when(
        loading: () => const Center(child: AppLoadingIndicator()),
        error: (error, _) => AppErrorWidget(
          message: error.toString(),
          onRetry: () => ref.refresh(fraudReviewsProvider),
        ),
        data: (fraudResults) {
          if (fraudResults.isEmpty) {
            return const EmptyStateWidget(
              icon: Icons.verified_user_outlined,
              message: 'No Suspicious Reviews',
              subtitle: 'All scanned reviews appear authentic and genuine.',
            );
          }

          return ListView(
            padding: const EdgeInsets.all(AppSpacing.xl),
            children: [
              // ── Summary ──
              Container(
                padding: const EdgeInsets.all(AppSpacing.base),
                decoration: BoxDecoration(
                  color: AppColors.suspicious.withValues(alpha: 0.08),
                  borderRadius: BorderRadius.circular(AppRadius.lg),
                  border: Border.all(
                    color: AppColors.suspicious.withValues(alpha: 0.2),
                  ),
                ),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(AppSpacing.md),
                      decoration: BoxDecoration(
                        color: AppColors.suspicious.withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(AppRadius.md),
                      ),
                      child: const Icon(
                        Icons.policy_rounded,
                        color: AppColors.suspicious,
                        size: 28,
                      ),
                    ),
                    const SizedBox(width: AppSpacing.base),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            '${fraudResults.length} Suspicious ${fraudResults.length == 1 ? 'Review' : 'Reviews'}',
                            style: Theme.of(context).textTheme.titleMedium
                                ?.copyWith(fontWeight: FontWeight.w600),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            'Detected across monitored platforms',
                            style: Theme.of(context).textTheme.bodySmall,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: AppSpacing.xl),

              // ── Fraud Cards ──
              ...fraudResults.map((fraud) {
                final color = _riskColor(fraud.riskLevel);

                return Material(
                  color: AppColors.cardDark,
                  borderRadius: BorderRadius.circular(AppRadius.lg),
                  child: InkWell(
                    onTap: () => context.push('/mentions/${fraud.mentionId}'),
                    borderRadius: BorderRadius.circular(AppRadius.lg),
                    child: Container(
                      margin: const EdgeInsets.only(bottom: AppSpacing.md),
                      padding: const EdgeInsets.all(AppSpacing.base),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(AppRadius.lg),
                        border: Border.all(color: color.withValues(alpha: 0.3)),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: AppSpacing.md,
                                  vertical: AppSpacing.xs,
                                ),
                                decoration: BoxDecoration(
                                  color: color.withValues(alpha: 0.15),
                                  borderRadius: BorderRadius.circular(
                                    AppRadius.full,
                                  ),
                                ),
                                child: Text(
                                  fraud.riskLevel.toUpperCase(),
                                  style: TextStyle(
                                    color: color,
                                    fontSize: 12,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ),
                              const Spacer(),
                              Text(
                                'Fraud: ${(fraud.confidence * 100).toStringAsFixed(0)}%',
                                style: TextStyle(
                                  color: color,
                                  fontWeight: FontWeight.w600,
                                  fontSize: 14,
                                ),
                              ),
                            ],
                          ),
                          if (fraud.reviewContent != null) ...[
                            const SizedBox(height: AppSpacing.md),
                            Text(
                              '"${fraud.reviewContent}"',
                              style: Theme.of(context).textTheme.bodyMedium
                                  ?.copyWith(
                                    fontStyle: FontStyle.italic,
                                    color: AppColors.textPrimaryDark,
                                  ),
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ],
                          const SizedBox(height: AppSpacing.md),
                          Wrap(
                            spacing: AppSpacing.sm,
                            runSpacing: AppSpacing.xs,
                            children: fraud.reasons.map((r) {
                              return Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: AppSpacing.sm,
                                  vertical: 2,
                                ),
                                decoration: BoxDecoration(
                                  color: AppColors.cardDarkElevated,
                                  borderRadius: BorderRadius.circular(
                                    AppRadius.sm,
                                  ),
                                ),
                                child: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Icon(
                                      Icons.check_circle_outline,
                                      size: 12,
                                      color: color,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      r,
                                      style: const TextStyle(
                                        fontSize: 11,
                                        color: AppColors.textSecondaryDark,
                                      ),
                                    ),
                                  ],
                                ),
                              );
                            }).toList(),
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              }),
            ],
          );
        },
      ),
    );
  }
}
