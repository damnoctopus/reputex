import 'package:flutter/material.dart';

import '../../app/theme.dart';

/// Color-coded sentiment badge pill.
///
/// Displays sentiment label with appropriate color:
/// Positive → green, Neutral → gray, Negative → red.
class SentimentBadge extends StatelessWidget {
  const SentimentBadge({
    super.key,
    required this.sentiment,
    this.confidence,
    this.compact = false,
  });

  final String sentiment;
  final double? confidence;
  final bool compact;

  Color get _color {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return AppColors.positive;
      case 'negative':
        return AppColors.negative;
      case 'neutral':
        return AppColors.neutral;
      default:
        return AppColors.neutral;
    }
  }

  IconData get _icon {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return Icons.sentiment_satisfied_rounded;
      case 'negative':
        return Icons.sentiment_dissatisfied_rounded;
      case 'neutral':
        return Icons.sentiment_neutral_rounded;
      default:
        return Icons.help_outline_rounded;
    }
  }

  @override
  Widget build(BuildContext context) {
    final color = _color;

    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: compact ? AppSpacing.sm : AppSpacing.md,
        vertical: compact ? 2 : AppSpacing.xs,
      ),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(AppRadius.full),
        border: Border.all(color: color.withValues(alpha: 0.3)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(_icon, size: compact ? 12 : 14, color: color),
          const SizedBox(width: 4),
          Text(
            confidence != null
                ? '$sentiment ${(confidence! * 100).toStringAsFixed(0)}%'
                : sentiment,
            style: TextStyle(
              color: color,
              fontSize: compact ? 10 : 12,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}
