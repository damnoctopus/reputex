import 'package:flutter/material.dart';

import '../../app/theme.dart';

/// Platform icon widget that displays a styled icon/label for each data source.
class PlatformIcon extends StatelessWidget {
  const PlatformIcon({
    super.key,
    required this.platform,
    this.size = 20,
    this.showLabel = false,
  });

  final String platform;
  final double size;
  final bool showLabel;

  static const Map<String, IconData> _icons = {
    'reddit': Icons.forum_rounded,
    'x': Icons.tag_rounded,
    'google news': Icons.newspaper_rounded,
    'justdial': Icons.store_rounded,
    'sulekha': Icons.business_rounded,
    'indiamart': Icons.factory_rounded,
  };

  static const Map<String, Color> _colors = {
    'reddit': Color(0xFFFF5722),
    'x': Color(0xFF1DA1F2),
    'google news': Color(0xFF4285F4),
    'justdial': Color(0xFF2196F3),
    'sulekha': Color(0xFFE91E63),
    'indiamart': Color(0xFF1565C0),
  };

  @override
  Widget build(BuildContext context) {
    final key = platform.toLowerCase();
    final icon = _icons[key] ?? Icons.language_rounded;
    final color = _colors[key] ?? AppColors.primary;

    if (showLabel) {
      return Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            padding: const EdgeInsets.all(AppSpacing.xs),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(AppRadius.sm),
            ),
            child: Icon(icon, size: size, color: color),
          ),
          const SizedBox(width: AppSpacing.sm),
          Text(
            platform,
            style: TextStyle(
              color: color,
              fontSize: 12,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      );
    }

    return Container(
      padding: const EdgeInsets.all(AppSpacing.xs),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(AppRadius.sm),
      ),
      child: Icon(icon, size: size, color: color),
    );
  }
}
