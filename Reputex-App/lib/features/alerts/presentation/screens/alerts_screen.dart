import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';

import '../../../../app/theme.dart';
import '../../../../core/widgets/empty_state_widget.dart';
import '../../../../core/widgets/error_widget.dart';
import '../../../../core/widgets/loading_indicator.dart';
import '../providers/alerts_provider.dart';

/// Alerts screen showing notifications, spikes, and crisis events.
class AlertsScreen extends ConsumerWidget {
  const AlertsScreen({super.key});

  static IconData _iconForType(String type) {
    switch (type.toLowerCase()) {
      case 'crisis':
        return Icons.crisis_alert_rounded;
      case 'fraud':
        return Icons.policy_rounded;
      case 'negative_spike':
        return Icons.warning_amber_rounded;
      case 'mention':
        return Icons.comment_rounded;
      default:
        return Icons.notifications_outlined;
    }
  }

  static Color _colorForType(String type) {
    switch (type.toLowerCase()) {
      case 'crisis':
        return AppColors.crisisRed;
      case 'fraud':
        return AppColors.suspicious;
      case 'negative_spike':
        return AppColors.accentWarning;
      case 'mention':
        return AppColors.primary;
      default:
        return AppColors.neutral;
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final alertsAsync = ref.watch(alertsProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Alerts')),
      body: alertsAsync.when(
        loading: () => const Center(child: AppLoadingIndicator()),
        error: (error, _) => AppErrorWidget(
          message: error.toString(),
          onRetry: () => ref.read(alertsProvider.notifier).fetchAlerts(),
        ),
        data: (alerts) {
          if (alerts.isEmpty) {
            return const EmptyStateWidget(
              message: 'No alerts yet',
              subtitle:
                  'You will be notified when something needs your attention',
              icon: Icons.notifications_none_rounded,
            );
          }

          final dateFormat = DateFormat('MMM d, hh:mm a');

          return RefreshIndicator(
            onRefresh: () => ref.read(alertsProvider.notifier).fetchAlerts(),
            child: ListView.separated(
              padding: const EdgeInsets.all(AppSpacing.xl),
              itemCount: alerts.length,
              separatorBuilder: (_, _) =>
                  const SizedBox(height: AppSpacing.sm),
              itemBuilder: (context, index) {
                final alert = alerts[index];
                final type = alert.type;
                final isRead = alert.isRead;
                final typeColor = _colorForType(type);

                return Material(
                  color: isRead
                      ? AppColors.cardDark
                      : AppColors.cardDarkElevated,
                  borderRadius: BorderRadius.circular(AppRadius.lg),
                  child: InkWell(
                    onTap: () {
                      if (!isRead) {
                        ref.read(alertsProvider.notifier).markAsRead(alert.id);
                      }
                      if (alert.referenceType == 'crisis' &&
                          alert.referenceId != null) {
                        context.push('/crisis/${alert.referenceId}');
                      } else if (alert.referenceType == 'mention' &&
                          alert.referenceId != null) {
                        context.push('/mentions/${alert.referenceId}');
                      }
                    },
                    borderRadius: BorderRadius.circular(AppRadius.lg),
                    child: Container(
                      padding: const EdgeInsets.all(AppSpacing.base),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(AppRadius.lg),
                        border: Border.all(
                          color: isRead
                              ? AppColors.glassBorder
                              : typeColor.withValues(alpha: 0.3),
                        ),
                      ),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Container(
                            padding: const EdgeInsets.all(AppSpacing.sm),
                            decoration: BoxDecoration(
                              color: typeColor.withValues(alpha: 0.15),
                              borderRadius: BorderRadius.circular(AppRadius.sm),
                            ),
                            child: Icon(
                              _iconForType(type),
                              color: typeColor,
                              size: 20,
                            ),
                          ),
                          const SizedBox(width: AppSpacing.md),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  alert.title,
                                  style: Theme.of(context).textTheme.titleMedium
                                      ?.copyWith(
                                        fontWeight: isRead
                                            ? FontWeight.w500
                                            : FontWeight.w600,
                                      ),
                                ),
                                const SizedBox(height: AppSpacing.xs),
                                Text(
                                  alert.message,
                                  style: Theme.of(context).textTheme.bodySmall,
                                ),
                                const SizedBox(height: AppSpacing.xs),
                                Text(
                                  dateFormat.format(alert.timestamp),
                                  style: Theme.of(context).textTheme.bodySmall
                                      ?.copyWith(
                                        color: AppColors.textTertiaryDark,
                                        fontSize: 11,
                                      ),
                                ),
                              ],
                            ),
                          ),
                          if (!isRead)
                            Container(
                              width: 8,
                              height: 8,
                              margin: const EdgeInsets.only(top: 6),
                              decoration: BoxDecoration(
                                color: typeColor,
                                shape: BoxShape.circle,
                              ),
                            ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}
