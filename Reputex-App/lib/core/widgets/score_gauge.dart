import 'package:flutter/material.dart';

import 'dart:math' as math;

import '../../app/theme.dart';

/// Animated circular gauge for the reputation score (0–100).
///
/// Uses a custom painter to draw the arc with gradient colors
/// and an animated fill based on the score value.
class ScoreGauge extends StatefulWidget {
  const ScoreGauge({
    super.key,
    required this.score,
    this.size = 160,
    this.strokeWidth = 12,
    this.animate = true,
  });

  final int score;
  final double size;
  final double strokeWidth;
  final bool animate;

  @override
  State<ScoreGauge> createState() => _ScoreGaugeState();
}

class _ScoreGaugeState extends State<ScoreGauge>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: AppDurations.chart,
      vsync: this,
    );
    _animation = Tween<double>(
      begin: 0,
      end: widget.score.toDouble(),
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeOutCubic));

    if (widget.animate) {
      _controller.forward();
    } else {
      _controller.value = 1.0;
    }
  }

  @override
  void didUpdateWidget(ScoreGauge oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.score != widget.score) {
      _animation =
          Tween<double>(
            begin: _animation.value,
            end: widget.score.toDouble(),
          ).animate(
            CurvedAnimation(parent: _controller, curve: Curves.easeOutCubic),
          );
      _controller
        ..reset()
        ..forward();
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Color _scoreColor(double score) {
    if (score >= 80) return AppColors.positive;
    if (score >= 60) return AppColors.primaryLight;
    if (score >= 40) return AppColors.suspicious;
    return AppColors.negative;
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        final animatedScore = _animation.value;
        final color = _scoreColor(animatedScore);

        return SizedBox(
          width: widget.size,
          height: widget.size,
          child: Stack(
            alignment: Alignment.center,
            children: [
              CustomPaint(
                size: Size(widget.size, widget.size),
                painter: _ScoreArcPainter(
                  score: animatedScore / 100,
                  color: color,
                  strokeWidth: widget.strokeWidth,
                  backgroundColor: AppColors.borderDark,
                ),
              ),
              Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    animatedScore.toStringAsFixed(0),
                    style: TextStyle(
                      fontSize: widget.size * 0.25,
                      fontWeight: FontWeight.w700,
                      color: color,
                    ),
                  ),
                  Text(
                    'out of 100',
                    style: TextStyle(
                      fontSize: widget.size * 0.08,
                      color: AppColors.textTertiaryDark,
                    ),
                  ),
                ],
              ),
            ],
          ),
        );
      },
    );
  }
}

class _ScoreArcPainter extends CustomPainter {
  _ScoreArcPainter({
    required this.score,
    required this.color,
    required this.strokeWidth,
    required this.backgroundColor,
  });

  final double score;
  final Color color;
  final double strokeWidth;
  final Color backgroundColor;

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = (size.width - strokeWidth) / 2;
    const startAngle = -math.pi * 0.75;
    const sweepTotal = math.pi * 1.5;

    // Background arc
    final bgPaint = Paint()
      ..color = backgroundColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;

    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      startAngle,
      sweepTotal,
      false,
      bgPaint,
    );

    // Score arc
    if (score > 0) {
      final scorePaint = Paint()
        ..color = color
        ..style = PaintingStyle.stroke
        ..strokeWidth = strokeWidth
        ..strokeCap = StrokeCap.round;

      canvas.drawArc(
        Rect.fromCircle(center: center, radius: radius),
        startAngle,
        sweepTotal * score,
        false,
        scorePaint,
      );
    }
  }

  @override
  bool shouldRepaint(_ScoreArcPainter oldDelegate) =>
      oldDelegate.score != score || oldDelegate.color != color;
}
