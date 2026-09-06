import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';

import '../../../../app/theme.dart';
import '../../../../core/widgets/error_widget.dart';
import '../../../../core/widgets/loading_indicator.dart';
import '../../../../core/widgets/platform_icon.dart';
import '../../../../core/widgets/sentiment_badge.dart';
import '../../../fraud/presentation/providers/fraud_provider.dart';
import '../providers/mentions_feed_provider.dart';

/// Review detail screen showing full review, sentiment analysis, and fraud analysis.
class ReviewDetailScreen extends ConsumerWidget {
  const ReviewDetailScreen({super.key, required this.mentionId});

  final String mentionId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final mentionAsync = ref.watch(mentionDetailProvider(mentionId));
    final fraudAsync = ref.watch(fraudAnalysisProvider(mentionId));

    return Scaffold(
      appBar: AppBar(title: const Text('Review Details')),
      body: mentionAsync.when(
        loading: () => const Center(child: AppLoadingIndicator()),
        error: (error, _) => AppErrorWidget(
          message: error.toString(),
          onRetry: () => ref.refresh(mentionDetailProvider(mentionId)),
        ),
        data: (mention) {
          final formattedDate = DateFormat('dd MMM yyyy, hh:mm a')
              .format(mention.timestamp);

          return SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.xl),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // ── Source Info ──
                _SectionCard(
                  children: [
                    _InfoRow(
                      label: 'Platform',
                      child: PlatformIcon(
                        platform: mention.platform,
                        showLabel: true,
                      ),
                    ),
                    const Divider(height: AppSpacing.xl),
                    _InfoRow(label: 'Author', value: mention.author),
                    const Divider(height: AppSpacing.xl),
                    _InfoRow(label: 'Date', value: formattedDate),
                    if (mention.rating != null) ...[
                      const Divider(height: AppSpacing.xl),
                      _InfoRow(
                        label: 'Rating',
                        value: '${mention.rating!.toStringAsFixed(1)} ★',
                      ),
                    ],
                  ],
                ),
                const SizedBox(height: AppSpacing.base),

                // ── Review Content ──
                _SectionCard(
                  children: [
                    Text(
                      'Review',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: AppSpacing.md),
                    Text(
                      '"${mention.content}"',
                      style: Theme.of(context).textTheme.bodyLarge
                          ?.copyWith(fontStyle: FontStyle.italic, height: 1.6),
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.base),

                // ── Sentiment Analysis ──
                _SectionCard(
                  children: [
                    Text(
                      'Sentiment Analysis',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: AppSpacing.base),
                    Row(
                      children: [
                        SentimentBadge(sentiment: mention.sentiment),
                        const SizedBox(width: AppSpacing.md),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Confidence: ${(mention.sentimentScore.abs() * 100).round()}%',
                                style: Theme.of(context).textTheme.bodyMedium,
                              ),
                              const SizedBox(height: AppSpacing.xs),
                              ClipRRect(
                                borderRadius: BorderRadius.circular(4),
                                child: LinearProgressIndicator(
                                  value: mention.sentimentScore.abs().clamp(
                                    0.0,
                                    1.0,
                                  ),
                                  backgroundColor: AppColors.borderDark,
                                  valueColor: AlwaysStoppedAnimation(
                                    mention.sentiment.toLowerCase() ==
                                            'positive'
                                        ? AppColors.positive
                                        : mention.sentiment.toLowerCase() ==
                                              'negative'
                                        ? AppColors.negative
                                        : AppColors.neutral,
                                  ),
                                  minHeight: 6,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.base),

                // ── Fraud Analysis ──
                fraudAsync.when(
                  loading: () => const ShimmerCard(height: 140),
                  error: (err, stack) => const SizedBox.shrink(),
                  data: (fraud) {
                    return _SectionCard(
                      borderColor: fraud.isFraudulent
                          ? AppColors.suspicious.withValues(alpha: 0.3)
                          : AppColors.glassBorder,
                      children: [
                        Row(
                          children: [
                            Text(
                              'Fraud Analysis',
                              style: Theme.of(context).textTheme.titleMedium,
                            ),
                            const Spacer(),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: AppSpacing.md,
                                vertical: AppSpacing.xs,
                              ),
                              decoration: BoxDecoration(
                                color: fraud.isFraudulent
                                    ? AppColors.suspicious.withValues(
                                        alpha: 0.15,
                                      )
                                    : AppColors.positive.withValues(
                                        alpha: 0.15,
                                      ),
                                borderRadius: BorderRadius.circular(
                                  AppRadius.full,
                                ),
                              ),
                              child: Text(
                                fraud.isFraudulent
                                    ? '⚠ ${fraud.riskLevel.toUpperCase()} RISK'
                                    : '✓ GENUINE',
                                style: TextStyle(
                                  color: fraud.isFraudulent
                                      ? AppColors.suspicious
                                      : AppColors.positive,
                                  fontSize: 12,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: AppSpacing.base),
                        _InfoRow(
                          label: 'Fraud Probability',
                          value: '${(fraud.confidence * 100).round()}%',
                        ),
                        if (fraud.reasons.isNotEmpty) ...[
                          const SizedBox(height: AppSpacing.base),
                          Text(
                            'Indicators:',
                            style: Theme.of(context).textTheme.bodyMedium
                                ?.copyWith(fontWeight: FontWeight.w600),
                          ),
                          const SizedBox(height: AppSpacing.sm),
                          ...fraud.reasons.map(
                            (r) => Padding(
                              padding: const EdgeInsets.only(
                                bottom: AppSpacing.xs,
                              ),
                              child: _ReasonChip(text: r),
                            ),
                          ),
                        ],
                      ],
                    );
                  },
                ),
                const SizedBox(height: AppSpacing.xl),

                // ── Generate AI Response ──
                SizedBox(
                  width: double.infinity,
                  height: 52,
                  child: ElevatedButton.icon(
                    onPressed: () =>
                        context.push('/mentions/$mentionId/response'),
                    icon: const Icon(Icons.auto_awesome_rounded),
                    label: Text(
                      mention.responseStatus != 'none'
                          ? 'View / Edit AI Response'
                          : 'Generate AI Response',
                    ),
                  ),
                ),
                const SizedBox(height: AppSpacing.xl),
              ],
            ),
          );
        },
      ),
    );
  }
}

class _SectionCard extends StatelessWidget {
  const _SectionCard({required this.children, this.borderColor});

  final List<Widget> children;
  final Color? borderColor;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(AppSpacing.base),
      decoration: BoxDecoration(
        color: AppColors.cardDark,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        border: Border.all(color: borderColor ?? AppColors.glassBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: children,
      ),
    );
  }
}

class _InfoRow extends StatelessWidget {
  const _InfoRow({required this.label, this.value, this.child});

  final String label;
  final String? value;
  final Widget? child;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: Theme.of(context).textTheme.bodySmall),
        child ??
            Text(
              value ?? '',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: AppColors.textPrimaryDark,
                fontWeight: FontWeight.w500,
              ),
            ),
      ],
    );
  }
}

class _ReasonChip extends StatelessWidget {
  const _ReasonChip({required this.text});

  final String text;

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.only(top: 2),
          child: Icon(
            Icons.check_circle_outline_rounded,
            size: 16,
            color: AppColors.suspicious,
          ),
        ),
        const SizedBox(width: AppSpacing.sm),
        Expanded(
          child: Text(text, style: Theme.of(context).textTheme.bodyMedium),
        ),
      ],
    );
  }
}
