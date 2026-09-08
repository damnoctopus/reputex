import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/theme.dart';
import '../../../../core/network/api_provider.dart';
import '../../../../core/widgets/error_widget.dart';
import '../../../../core/widgets/loading_indicator.dart';
import '../../../../core/widgets/platform_icon.dart';
import '../../../../core/widgets/score_gauge.dart';
import '../../../../core/widgets/sentiment_badge.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../../onboarding/presentation/providers/business_provider.dart';
import '../providers/dashboard_provider.dart';

/// Main dashboard screen — consumes [dashboardProvider] and [authProvider].
class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);
    final businessState = ref.watch(businessProvider);
    final dashboardAsync = ref.watch(dashboardProvider);
    final userName = authState.user?.fullName ?? 'Business Owner';
    final businessName = businessState.valueOrNull?.name ?? 'My Business';

    return Scaffold(
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: () => ref.read(dashboardProvider.notifier).refresh(),
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: const EdgeInsets.all(AppSpacing.xl),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // ── Greeting & Scan Action ──
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Good Morning, $userName',
                            style: Theme.of(context).textTheme.headlineMedium,
                          ),
                          const SizedBox(height: AppSpacing.xs),
                          Text(
                            businessName,
                            style: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.copyWith(color: AppColors.primary),
                          ),
                        ],
                      ),
                    ),
                    const _ScanButton(),
                  ],
                ),
                const SizedBox(height: AppSpacing.xl),

                dashboardAsync.when(
                  loading: () => const Column(
                    children: [
                      ShimmerCard(height: 220),
                      SizedBox(height: AppSpacing.xl),
                      Row(
                        children: [
                          Expanded(child: ShimmerCard(height: 100)),
                          SizedBox(width: AppSpacing.md),
                          Expanded(child: ShimmerCard(height: 100)),
                        ],
                      ),
                      SizedBox(height: AppSpacing.md),
                      Row(
                        children: [
                          Expanded(child: ShimmerCard(height: 100)),
                          SizedBox(width: AppSpacing.md),
                          Expanded(child: ShimmerCard(height: 100)),
                        ],
                      ),
                    ],
                  ),
                  error: (error, _) => AppErrorWidget(
                    message: error.toString(),
                    onRetry: () =>
                        ref.read(dashboardProvider.notifier).fetchDashboard(),
                  ),
                  data: (summary) {
                    final dist = summary.sentimentDistribution;
                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // ── Reputation Score ──
                        Center(
                          child: Container(
                            padding: const EdgeInsets.all(AppSpacing.xl),
                            decoration: BoxDecoration(
                              color: AppColors.cardDark,
                              borderRadius: BorderRadius.circular(AppRadius.xl),
                              border: Border.all(color: AppColors.glassBorder),
                            ),
                            child: Column(
                              children: [
                                Text(
                                  'Reputation Score',
                                  style: Theme.of(context)
                                      .textTheme
                                      .titleMedium,
                                ),
                                const SizedBox(height: AppSpacing.base),
                                ScoreGauge(
                                  score: summary
                                      .reputationScore
                                      .currentScore
                                      .round(),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: AppSpacing.xl),

                        // ── Sentiment Distribution ──
                        Row(
                          children: [
                            Expanded(
                              child: _StatCard(
                                label: 'Positive',
                                value: '${dist.positivePercentage.round()}%',
                                color: AppColors.positive,
                                icon: Icons.trending_up_rounded,
                              ),
                            ),
                            const SizedBox(width: AppSpacing.md),
                            Expanded(
                              child: _StatCard(
                                label: 'Negative',
                                value: '${dist.negativePercentage.round()}%',
                                color: AppColors.negative,
                                icon: Icons.trending_down_rounded,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: AppSpacing.md),
                        Row(
                          children: [
                            Expanded(
                              child: _StatCard(
                                label: 'Neutral',
                                value: '${dist.neutralPercentage.round()}%',
                                color: AppColors.neutral,
                                icon: Icons.trending_flat_rounded,
                              ),
                            ),
                            const SizedBox(width: AppSpacing.md),
                            Expanded(
                              child: _StatCard(
                                label: 'Suspicious',
                                value: '${summary.fraudAlertsCount}',
                                color: AppColors.suspicious,
                                icon: Icons.warning_amber_rounded,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: AppSpacing.xl),

                        // ── Quick Actions ──
                        Row(
                          children: [
                            Expanded(
                              child: _ActionChip(
                                label: 'Analytics',
                                icon: Icons.analytics_outlined,
                                onTap: () => context.push('/analytics'),
                              ),
                            ),
                            const SizedBox(width: AppSpacing.sm),
                            Expanded(
                              child: _ActionChip(
                                label: 'Fraud',
                                icon: Icons.policy_outlined,
                                onTap: () => context.push('/fraud'),
                              ),
                            ),
                            const SizedBox(width: AppSpacing.sm),
                            Expanded(
                              child: _ActionChip(
                                label: 'Crisis',
                                icon: Icons.crisis_alert_outlined,
                                onTap: () => context.push('/crisis'),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: AppSpacing.xl),

                        // ── Crisis Early Warning Banner ──
                        if (summary.crisisRiskLevel != 'Normal') ...[
                          _CrisisRiskBanner(level: summary.crisisRiskLevel),
                          const SizedBox(height: AppSpacing.lg),
                        ],

                        // ── Review Manipulation Risk Banner ──
                        if (summary.suspiciousReviewsCount > 0) ...[
                          _ManipulationRiskBanner(
                            suspiciousCount: summary.suspiciousReviewsCount,
                            clusterCount: summary.activeClustersCount,
                          ),
                          const SizedBox(height: AppSpacing.lg),
                        ],

                        // ── Top Customer Issues ──
                        if (summary.topIssues.isNotEmpty) ...[
                          _TopIssuesSection(issues: summary.topIssues),
                          const SizedBox(height: AppSpacing.xl),
                        ],

                        // ── Recent Mentions ──
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              'Recent Mentions',
                              style: Theme.of(context).textTheme.titleLarge,
                            ),
                            TextButton(
                              onPressed: () => context.go('/mentions'),
                              child: const Text('View All'),
                            ),
                          ],
                        ),
                        const SizedBox(height: AppSpacing.md),
                        ...summary.recentMentions.map((mention) {
                          return Padding(
                            padding: const EdgeInsets.only(
                              bottom: AppSpacing.md,
                            ),
                            child: _MentionPreviewCard(
                              platform: mention.platform,
                              content: mention.content,
                              sentiment: mention.sentiment,
                              timeAgo: _formatTimeAgo(mention.timestamp),
                              isSuspicious: mention.isFake,
                              onTap: () =>
                                  context.push('/mentions/${mention.id}'),
                            ),
                          );
                        }),
                        const SizedBox(height: AppSpacing.xl),
                      ],
                    );
                  },
                ),
              ],
            ),
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

class _StatCard extends StatelessWidget {
  const _StatCard({
    required this.label,
    required this.value,
    required this.color,
    required this.icon,
  });

  final String label;
  final String value;
  final Color color;
  final IconData icon;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.base),
      decoration: BoxDecoration(
        color: AppColors.cardDark,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        border: Border.all(color: AppColors.glassBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 18),
              const Spacer(),
              Container(
                width: 8,
                height: 8,
                decoration: BoxDecoration(color: color, shape: BoxShape.circle),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),
          Text(
            value,
            style: Theme.of(context).textTheme.headlineMedium
                ?.copyWith(color: color, fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(label, style: Theme.of(context).textTheme.bodySmall),
        ],
      ),
    );
  }
}

class _ActionChip extends StatelessWidget {
  const _ActionChip({
    required this.label,
    required this.icon,
    required this.onTap,
  });

  final String label;
  final IconData icon;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: AppColors.cardDark,
      borderRadius: BorderRadius.circular(AppRadius.md),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadius.md),
        child: Container(
          padding: const EdgeInsets.symmetric(
            vertical: AppSpacing.md,
            horizontal: AppSpacing.sm,
          ),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(AppRadius.md),
            border: Border.all(color: AppColors.glassBorder),
          ),
          child: Column(
            children: [
              Icon(icon, color: AppColors.primary, size: 22),
              const SizedBox(height: AppSpacing.xs),
              Text(
                label,
                style: Theme.of(context).textTheme.bodySmall
                    ?.copyWith(color: AppColors.textSecondaryDark),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _MentionPreviewCard extends StatelessWidget {
  const _MentionPreviewCard({
    required this.platform,
    required this.content,
    required this.sentiment,
    required this.timeAgo,
    this.isSuspicious = false,
    this.onTap,
  });

  final String platform;
  final String content;
  final String sentiment;
  final String timeAgo;
  final bool isSuspicious;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        child: Container(
          padding: const EdgeInsets.all(AppSpacing.base),
          decoration: BoxDecoration(
            color: AppColors.cardDark,
            borderRadius: BorderRadius.circular(AppRadius.lg),
            border: Border.all(color: AppColors.glassBorder),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  PlatformIcon(platform: platform, showLabel: true),
                  const Spacer(),
                  if (isSuspicious)
                    Container(
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
                  const SizedBox(width: AppSpacing.sm),
                  Text(timeAgo, style: Theme.of(context).textTheme.bodySmall),
                ],
              ),
              const SizedBox(height: AppSpacing.md),
              Text(
                '"$content"',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: AppColors.textPrimaryDark,
                  fontStyle: FontStyle.italic,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: AppSpacing.md),
              SentimentBadge(sentiment: sentiment, compact: true),
            ],
          ),
        ),
      ),
    );
  }
}

class _ScanButton extends ConsumerStatefulWidget {
  const _ScanButton();

  @override
  ConsumerState<_ScanButton> createState() => _ScanButtonState();
}

class _ScanButtonState extends ConsumerState<_ScanButton> {
  bool _scanning = false;

  Future<void> _handleScan() async {
    setState(() => _scanning = true);
    try {
      final api = ref.read(apiServiceProvider);
      await api.triggerScan();
      if (mounted) {
        context.push('/scraping');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Scan trigger failed: $e'),
            backgroundColor: AppColors.negative,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _scanning = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_scanning) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          color: AppColors.cardDark,
          borderRadius: BorderRadius.circular(AppRadius.lg),
          border: Border.all(color: AppColors.glassBorder),
        ),
        child: const Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            SizedBox(
              width: 14,
              height: 14,
              child: CircularProgressIndicator(strokeWidth: 2),
            ),
            SizedBox(width: 8),
            Text('Scanning...', style: TextStyle(fontSize: 12)),
          ],
        ),
      );
    }

    return ElevatedButton.icon(
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
      ),
      onPressed: _handleScan,
      icon: const Icon(Icons.radar_rounded, size: 16),
      label: const Text(
        'Scan Now',
        style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
      ),
    );
  }
}

class _CrisisRiskBanner extends StatelessWidget {
  const _CrisisRiskBanner({required this.level});

  final String level;

  @override
  Widget build(BuildContext context) {
    final color = level == 'Crisis Active'
        ? AppColors.negative
        : (level == 'High Risk' ? Colors.orangeAccent : AppColors.suspicious);

    return InkWell(
      onTap: () => context.push('/crisis'),
      borderRadius: BorderRadius.circular(AppRadius.lg),
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.md),
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.12),
          borderRadius: BorderRadius.circular(AppRadius.lg),
          border: Border.all(color: color.withValues(alpha: 0.4)),
        ),
        child: Row(
          children: [
            Icon(Icons.crisis_alert_rounded, color: color, size: 28),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Crisis Risk: $level',
                    style: TextStyle(
                      color: color,
                      fontWeight: FontWeight.bold,
                      fontSize: 15,
                    ),
                  ),
                  const SizedBox(height: 2),
                  const Text(
                    'Elevated negative review velocity detected. Tap to inspect crisis drivers.',
                    style: TextStyle(fontSize: 12, color: AppColors.textSecondaryDark),
                  ),
                ],
              ),
            ),
            Icon(Icons.chevron_right, color: color),
          ],
        ),
      ),
    );
  }
}

class _ManipulationRiskBanner extends StatelessWidget {
  const _ManipulationRiskBanner({
    required this.suspiciousCount,
    required this.clusterCount,
  });

  final int suspiciousCount;
  final int clusterCount;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () => context.push('/fraud'),
      borderRadius: BorderRadius.circular(AppRadius.lg),
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.md),
        decoration: BoxDecoration(
          color: AppColors.suspicious.withValues(alpha: 0.12),
          borderRadius: BorderRadius.circular(AppRadius.lg),
          border: Border.all(color: AppColors.suspicious.withValues(alpha: 0.4)),
        ),
        child: Row(
          children: [
            const Icon(Icons.shield_outlined, color: AppColors.suspicious, size: 28),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Review Manipulation Risk: $suspiciousCount flagged',
                    style: const TextStyle(
                      color: AppColors.suspicious,
                      fontWeight: FontWeight.bold,
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    clusterCount > 0
                        ? '$clusterCount coordinated cluster detected. Tap to inspect signal scores.'
                        : 'Potential artificial reviews detected. Tap to inspect signals.',
                    style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark),
                  ),
                ],
              ),
            ),
            const Icon(Icons.chevron_right, color: AppColors.suspicious),
          ],
        ),
      ),
    );
  }
}

class _TopIssuesSection extends StatelessWidget {
  const _TopIssuesSection({required this.issues});

  final List<Map<String, dynamic>> issues;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              'Top Customer Issues',
              style: Theme.of(context).textTheme.titleLarge,
            ),
          ],
        ),
        const SizedBox(height: AppSpacing.md),
        ...issues.map((issue) {
          final id = issue['id']?.toString() ?? '';
          final category = issue['category']?.toString() ?? 'General';
          final subtopic = issue['subtopic']?.toString() ?? 'Issue';
          final severity = issue['severity']?.toString() ?? 'medium';
          final count = issue['mention_count'] ?? 0;
          final platforms = issue['platforms_breakdown'] as Map<String, dynamic>? ?? {};

          final severityColor = severity == 'critical'
              ? AppColors.negative
              : (severity == 'high' ? Colors.orangeAccent : AppColors.suspicious);

          return Container(
            margin: const EdgeInsets.only(bottom: AppSpacing.md),
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: id.isNotEmpty ? () => context.push('/issues/$id') : null,
                borderRadius: BorderRadius.circular(AppRadius.lg),
                child: Container(
                  padding: const EdgeInsets.all(AppSpacing.md),
                  decoration: BoxDecoration(
                    color: AppColors.cardDark,
                    borderRadius: BorderRadius.circular(AppRadius.lg),
                    border: Border.all(color: AppColors.glassBorder),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                            decoration: BoxDecoration(
                              color: AppColors.primary.withValues(alpha: 0.15),
                              borderRadius: BorderRadius.circular(AppRadius.sm),
                            ),
                            child: Text(
                              category,
                              style: const TextStyle(
                                color: AppColors.primary,
                                fontSize: 11,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                            decoration: BoxDecoration(
                              color: severityColor.withValues(alpha: 0.15),
                              borderRadius: BorderRadius.circular(AppRadius.sm),
                            ),
                            child: Text(
                              severity.toUpperCase(),
                              style: TextStyle(
                                color: severityColor,
                                fontSize: 10,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: AppSpacing.sm),
                      Text(
                        subtopic,
                        style: const TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      const SizedBox(height: AppSpacing.xs),
                      Text(
                        '$count customer reviews',
                        style: const TextStyle(
                          fontSize: 12,
                          color: AppColors.textSecondaryDark,
                        ),
                      ),
                      if (platforms.isNotEmpty) ...[
                        const SizedBox(height: AppSpacing.sm),
                        Wrap(
                          spacing: 6,
                          runSpacing: 4,
                          children: platforms.entries.map((p) {
                            return Container(
                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                              decoration: BoxDecoration(
                                color: AppColors.surfaceDark,
                                borderRadius: BorderRadius.circular(AppRadius.sm),
                              ),
                              child: Text(
                                '${p.key}: ${p.value}',
                                style: const TextStyle(fontSize: 11),
                              ),
                            );
                          }).toList(),
                        ),
                      ],
                    ],
                  ),
                ),
              ),
            ),
          );
        }),
      ],
    );
  }
}
