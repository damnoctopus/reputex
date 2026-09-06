import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../app/theme.dart';
import '../../../../core/widgets/error_widget.dart';
import '../../../../core/widgets/loading_indicator.dart';
import '../providers/sentiment_provider.dart';

/// Sentiment analytics screen with charts and breakdowns.
class SentimentAnalyticsScreen extends ConsumerWidget {
  const SentimentAnalyticsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final sentimentAsync = ref.watch(sentimentAnalyticsProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Sentiment Analytics')),
      body: sentimentAsync.when(
        loading: () => const Center(child: AppLoadingIndicator()),
        error: (error, _) => AppErrorWidget(
          message: error.toString(),
          onRetry: () => ref.refresh(sentimentAnalyticsProvider),
        ),
        data: (analytics) {
          final dist = analytics.distribution;
          final trends = analytics.trends;
          final platforms = analytics.platformBreakdown;

          return SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.xl),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // ── Overall Sentiment Donut ──
                Text(
                  'Overall Sentiment',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: AppSpacing.base),
                SizedBox(
                  height: 200,
                  child: PieChart(
                    PieChartData(
                      sectionsSpace: 3,
                      centerSpaceRadius: 50,
                      sections: [
                        PieChartSectionData(
                          value: dist.positivePercentage > 0
                              ? dist.positivePercentage
                              : 1,
                          title: '${dist.positivePercentage.round()}%',
                          color: AppColors.positive,
                          radius: 40,
                          titleStyle: const TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        PieChartSectionData(
                          value: dist.neutralPercentage > 0
                              ? dist.neutralPercentage
                              : 1,
                          title: '${dist.neutralPercentage.round()}%',
                          color: AppColors.neutral,
                          radius: 40,
                          titleStyle: const TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        PieChartSectionData(
                          value: dist.negativePercentage > 0
                              ? dist.negativePercentage
                              : 1,
                          title: '${dist.negativePercentage.round()}%',
                          color: AppColors.negative,
                          radius: 40,
                          titleStyle: const TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: AppSpacing.md),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _LegendDot(
                      color: AppColors.positive,
                      label: 'Positive (${dist.positive})',
                    ),
                    const SizedBox(width: AppSpacing.lg),
                    _LegendDot(
                      color: AppColors.neutral,
                      label: 'Neutral (${dist.neutral})',
                    ),
                    const SizedBox(width: AppSpacing.lg),
                    _LegendDot(
                      color: AppColors.negative,
                      label: 'Negative (${dist.negative})',
                    ),
                  ],
                ),

                const SizedBox(height: AppSpacing.xxl),

                // ── Sentiment Trend ──
                Text(
                  'Sentiment Trend (7-Day)',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: AppSpacing.base),
                SizedBox(
                  height: 200,
                  child: LineChart(
                    LineChartData(
                      gridData: const FlGridData(
                        show: true,
                        drawVerticalLine: false,
                        horizontalInterval: 25,
                        getDrawingHorizontalLine: _getGridLine,
                      ),
                      titlesData: FlTitlesData(
                        leftTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            reservedSize: 30,
                            getTitlesWidget: (value, meta) => Text(
                              '${value.toInt()}%',
                              style: const TextStyle(
                                color: AppColors.textTertiaryDark,
                                fontSize: 10,
                              ),
                            ),
                          ),
                        ),
                        bottomTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            getTitlesWidget: (value, meta) {
                              final idx = value.toInt();
                              if (idx >= 0 && idx < trends.length) {
                                return Text(
                                  trends[idx].date,
                                  style: const TextStyle(
                                    color: AppColors.textTertiaryDark,
                                    fontSize: 10,
                                  ),
                                );
                              }
                              return const Text('');
                            },
                          ),
                        ),
                        topTitles: const AxisTitles(
                          sideTitles: SideTitles(showTitles: false),
                        ),
                        rightTitles: const AxisTitles(
                          sideTitles: SideTitles(showTitles: false),
                        ),
                      ),
                      borderData: FlBorderData(show: false),
                      minX: 0,
                      maxX: (trends.length - 1).toDouble(),
                      minY: 0,
                      maxY: 100,
                      lineBarsData: [
                        LineChartBarData(
                          spots: trends.asMap().entries.map((e) {
                            return FlSpot(e.key.toDouble(), e.value.score);
                          }).toList(),
                          isCurved: true,
                          color: AppColors.positive,
                          barWidth: 2.5,
                          dotData: const FlDotData(show: false),
                          belowBarData: BarAreaData(
                            show: true,
                            color: AppColors.positive.withValues(alpha: 0.1),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: AppSpacing.xxl),

                // ── Platform Breakdown ──
                Text(
                  'Platform Breakdown',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: AppSpacing.base),
                ...platforms.map((p) {
                  return _PlatformBar(
                    platform: p.platform,
                    percentage: p.positivePercentage.round(),
                    rating: p.averageRating,
                    color: _getPlatformColor(p.platform),
                  );
                }),
                const SizedBox(height: AppSpacing.xl),
              ],
            ),
          );
        },
      ),
    );
  }

  static FlLine _getGridLine(double value) {
    return const FlLine(color: AppColors.borderDark, strokeWidth: 1);
  }

  static Color _getPlatformColor(String platform) {
    switch (platform.toLowerCase()) {
      case 'reddit':
        return const Color(0xFFFF5722);
      case 'x':
        return const Color(0xFF1DA1F2);
      case 'google':
      case 'google news':
        return const Color(0xFF4285F4);
      case 'justdial':
        return const Color(0xFF2196F3);
      case 'sulekha':
        return const Color(0xFFE91E63);
      case 'indiamart':
        return const Color(0xFF1565C0);
      default:
        return AppColors.primary;
    }
  }
}

class _LegendDot extends StatelessWidget {
  const _LegendDot({required this.color, required this.label});
  final Color color;
  final String label;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 10,
          height: 10,
          decoration: BoxDecoration(color: color, shape: BoxShape.circle),
        ),
        const SizedBox(width: 6),
        Text(label, style: Theme.of(context).textTheme.bodySmall),
      ],
    );
  }
}

class _PlatformBar extends StatelessWidget {
  const _PlatformBar({
    required this.platform,
    required this.percentage,
    required this.color,
    this.rating,
  });

  final String platform;
  final int percentage;
  final Color color;
  final double? rating;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppSpacing.md),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(platform, style: Theme.of(context).textTheme.bodyMedium),
              Row(
                children: [
                  if (rating != null)
                    Text(
                      '${rating!.toStringAsFixed(1)} ★  •  ',
                      style: const TextStyle(
                        color: AppColors.accentWarning,
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  Text(
                    '$percentage% positive',
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.xs),
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: percentage / 100,
              backgroundColor: AppColors.borderDark,
              valueColor: AlwaysStoppedAnimation(color),
              minHeight: 8,
            ),
          ),
        ],
      ),
    );
  }
}
