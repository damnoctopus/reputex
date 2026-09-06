import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';

import '../../../../app/theme.dart';
import '../../../../core/widgets/error_widget.dart';
import '../../../../core/widgets/loading_indicator.dart';
import '../../domain/models/crisis_event.dart';
import '../providers/crisis_provider.dart';

/// Crisis monitoring screen showing active and historical crises.
class CrisisScreen extends ConsumerWidget {
  const CrisisScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final activeCrisisAsync = ref.watch(activeCrisisProvider);
    final crisisEventsAsync = ref.watch(crisisEventsProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Crisis Monitor')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(AppSpacing.xl),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // ── Active Crisis ──
            activeCrisisAsync.when(
              loading: () => const ShimmerCard(height: 220),
              error: (err, _) => AppErrorWidget(
                message: err.toString(),
                onRetry: () => ref.refresh(activeCrisisProvider),
              ),
              data: (activeCrisis) {
                if (activeCrisis == null) {
                  return Container(
                    padding: const EdgeInsets.all(AppSpacing.xl),
                    decoration: BoxDecoration(
                      color: AppColors.positive.withValues(alpha: 0.08),
                      borderRadius: BorderRadius.circular(AppRadius.xl),
                      border: Border.all(
                        color: AppColors.positive.withValues(alpha: 0.3),
                      ),
                    ),
                    child: Row(
                      children: [
                        const Icon(
                          Icons.check_circle_outline_rounded,
                          color: AppColors.positive,
                          size: 32,
                        ),
                        const SizedBox(width: AppSpacing.base),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'No Active Crises',
                                style: Theme.of(context).textTheme.titleMedium
                                    ?.copyWith(
                                      fontWeight: FontWeight.w600,
                                      color: AppColors.positive,
                                    ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                'Mention velocity and sentiment thresholds are stable.',
                                style: Theme.of(context).textTheme.bodySmall,
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  );
                }

                return _ActiveCrisisCard(
                  crisis: activeCrisis,
                  onTap: () => context.push('/crisis/${activeCrisis.id}'),
                );
              },
            ),
            const SizedBox(height: AppSpacing.xxl),

            // ── History ──
            Text(
              'Crisis History',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: AppSpacing.base),

            crisisEventsAsync.when(
              loading: () => const Column(
                children: [
                  ShimmerCard(height: 90),
                  SizedBox(height: AppSpacing.md),
                  ShimmerCard(height: 90),
                ],
              ),
              error: (err, _) => Text(
                'Could not load history: $err',
                style: const TextStyle(color: AppColors.error),
              ),
              data: (events) {
                final resolvedEvents = events
                    .where((e) => e.status != 'active')
                    .toList();

                if (resolvedEvents.isEmpty) {
                  return Text(
                    'No past resolved crisis events recorded.',
                    style: Theme.of(context).textTheme.bodySmall,
                  );
                }

                final dateFormat = DateFormat('MMM d, HH:mm');

                return Column(
                  children: resolvedEvents.map((event) {
                    return Padding(
                      padding: const EdgeInsets.only(bottom: AppSpacing.md),
                      child: _HistoryCrisisCard(
                        title: event.title,
                        startedAt: dateFormat.format(event.startedAt),
                        resolvedAt: event.resolvedAt != null
                            ? dateFormat.format(event.resolvedAt!)
                            : 'N/A',
                        peakVelocity: '${event.velocity.toStringAsFixed(1)}/hr',
                        onTap: () => context.push('/crisis/${event.id}'),
                      ),
                    );
                  }).toList(),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}

class _ActiveCrisisCard extends StatefulWidget {
  const _ActiveCrisisCard({required this.crisis, required this.onTap});

  final CrisisEvent crisis;
  final VoidCallback onTap;

  @override
  State<_ActiveCrisisCard> createState() => _ActiveCrisisCardState();
}

class _ActiveCrisisCardState extends State<_ActiveCrisisCard>
    with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      duration: const Duration(milliseconds: 2000),
      vsync: this,
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final crisis = widget.crisis;

    return AnimatedBuilder(
      animation: _pulseController,
      builder: (context, child) {
        final pulseValue = 0.15 + (_pulseController.value * 0.15);

        return Material(
          color: Colors.transparent,
          child: InkWell(
            onTap: widget.onTap,
            borderRadius: BorderRadius.circular(AppRadius.xl),
            child: Container(
              padding: const EdgeInsets.all(AppSpacing.xl),
              decoration: BoxDecoration(
                color: AppColors.crisisRed.withValues(alpha: 0.08),
                borderRadius: BorderRadius.circular(AppRadius.xl),
                border: Border.all(
                  color: AppColors.crisisRed.withValues(
                    alpha: pulseValue + 0.2,
                  ),
                  width: 1.5,
                ),
                boxShadow: [
                  BoxShadow(
                    color: AppColors.crisisRed.withValues(
                      alpha: pulseValue * 0.3,
                    ),
                    blurRadius: 20,
                    spreadRadius: 2,
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        width: 12,
                        height: 12,
                        decoration: BoxDecoration(
                          color: AppColors.crisisRed,
                          shape: BoxShape.circle,
                          boxShadow: [
                            BoxShadow(
                              color: AppColors.crisisRed.withValues(alpha: 0.5),
                              blurRadius: 8,
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: AppSpacing.sm),
                      Text(
                        'ACTIVE CRISIS (${crisis.severity.toUpperCase()})',
                        style: Theme.of(context).textTheme.labelLarge?.copyWith(
                          color: AppColors.crisisRed,
                          letterSpacing: 1.2,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: AppSpacing.md),
                  Text(
                    crisis.title,
                    style: Theme.of(context).textTheme.titleMedium
                        ?.copyWith(fontWeight: FontWeight.w700),
                  ),
                  const SizedBox(height: AppSpacing.sm),
                  Text(
                    crisis.triggerReason,
                    style: Theme.of(context).textTheme.bodySmall
                        ?.copyWith(color: AppColors.textSecondaryDark),
                  ),
                  const SizedBox(height: AppSpacing.xl),
                  _CrisisMetric(
                    label: 'Velocity',
                    value: '+${crisis.velocity.toStringAsFixed(1)} mentions/hr',
                  ),
                  const SizedBox(height: AppSpacing.md),
                  _CrisisMetric(
                    label: 'Negative Mentions',
                    value: '${crisis.negativeMentionsCount}',
                  ),
                  const SizedBox(height: AppSpacing.md),
                  _CrisisMetric(
                    label: 'Platforms',
                    value: crisis.affectedPlatforms.join(', '),
                  ),
                  const SizedBox(height: AppSpacing.xl),
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton(
                      onPressed: widget.onTap,
                      style: OutlinedButton.styleFrom(
                        side: const BorderSide(color: AppColors.crisisRed),
                        foregroundColor: AppColors.crisisRed,
                      ),
                      child: const Text('View Crisis Details'),
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}

class _CrisisMetric extends StatelessWidget {
  const _CrisisMetric({required this.label, required this.value});
  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: Theme.of(context).textTheme.bodyMedium),
        Text(
          value,
          style: Theme.of(context).textTheme.bodyLarge
              ?.copyWith(fontWeight: FontWeight.w600),
        ),
      ],
    );
  }
}

class _HistoryCrisisCard extends StatelessWidget {
  const _HistoryCrisisCard({
    required this.title,
    required this.startedAt,
    required this.resolvedAt,
    required this.peakVelocity,
    required this.onTap,
  });

  final String title;
  final String startedAt;
  final String resolvedAt;
  final String peakVelocity;
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
              const Row(
                children: [
                  Icon(
                    Icons.check_circle_outline,
                    color: AppColors.positive,
                    size: 18,
                  ),
                  SizedBox(width: AppSpacing.sm),
                  Text(
                    'Resolved',
                    style: TextStyle(
                      color: AppColors.positive,
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: AppSpacing.sm),
              Text(title, style: Theme.of(context).textTheme.titleMedium),
              const SizedBox(height: AppSpacing.md),
              Row(
                children: [
                  _MiniMetric(label: 'Velocity', value: peakVelocity),
                  const SizedBox(width: AppSpacing.xl),
                  _MiniMetric(label: 'Started', value: startedAt),
                  const SizedBox(width: AppSpacing.xl),
                  _MiniMetric(label: 'Resolved', value: resolvedAt),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _MiniMetric extends StatelessWidget {
  const _MiniMetric({required this.label, required this.value});
  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: Theme.of(context).textTheme.bodySmall),
        const SizedBox(height: 2),
        Text(
          value,
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
            fontWeight: FontWeight.w500,
            color: AppColors.textPrimaryDark,
          ),
        ),
      ],
    );
  }
}
