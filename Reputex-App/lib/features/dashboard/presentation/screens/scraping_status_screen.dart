import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/theme.dart';
import '../../../../core/network/api_provider.dart';
import '../providers/dashboard_provider.dart';

/// Screen displayed while the backend scraper processes live reviews and social mentions.
///
/// Features dynamic sonar radar animation, real-time polling of platform
/// scraping jobs (Google Maps, Reddit, X / Twitter), and transitions to
/// the dashboard upon scan completion.
class ScrapingStatusScreen extends ConsumerStatefulWidget {
  const ScrapingStatusScreen({super.key});

  @override
  ConsumerState<ScrapingStatusScreen> createState() =>
      _ScrapingStatusScreenState();
}

class _ScrapingStatusScreenState extends ConsumerState<ScrapingStatusScreen>
    with SingleTickerProviderStateMixin {
  late final AnimationController _pulseController;
  late final Animation<double> _pulseAnimation;

  Timer? _pollingTimer;
  int _secondsElapsed = 0;
  bool _isCompleted = false;
  String? _errorMessage;
  Map<String, dynamic>? _scanStatus;

  // Platform scan state tracking
  final Map<String, _PlatformStatus> _platformStatuses = {
    'google': const _PlatformStatus(
      name: 'Google Maps / Places',
      icon: Icons.place_rounded,
      color: Color(0xFF4285F4),
    ),
    'reddit': const _PlatformStatus(
      name: 'Reddit Discussions',
      icon: Icons.forum_rounded,
      color: Color(0xFFFF4500),
    ),
    'twitter': const _PlatformStatus(
      name: 'X / Twitter Feeds',
      icon: Icons.chat_bubble_outline_rounded,
      color: Color(0xFF1DA1F2),
    ),
    'web': const _PlatformStatus(
      name: 'JustDial & Web Sources',
      icon: Icons.public_rounded,
      color: Color(0xFF10B981),
    ),
  };

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1800),
    )..repeat(reverse: true);

    _pulseAnimation = Tween<double>(begin: 0.95, end: 1.15).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );

    _startPolling();
  }

  void _startPolling() {
    _secondsElapsed = 0;
    _errorMessage = null;

    // Trigger initial poll immediately
    _pollStatus();

    _pollingTimer?.cancel();
    _pollingTimer = Timer.periodic(const Duration(seconds: 2), (timer) {
      if (!mounted) {
        timer.cancel();
        return;
      }
      setState(() => _secondsElapsed += 2);
      _pollStatus();
    });
  }

  Future<void> _pollStatus() async {
    try {
      final api = ref.read(apiServiceProvider);
      final statusData = await api.getScanStatus();

      if (!mounted) return;

      setState(() {
        _scanStatus = statusData;
        final overallStatus = statusData['status'] as String? ?? 'running';

        // Parse individual platform jobs if available
        final jobs = statusData['jobs'] as List<dynamic>? ?? [];
        for (final job in jobs) {
          if (job is Map<String, dynamic>) {
            final plat = (job['platform'] as String? ?? '').toLowerCase();
            final jobStatus = job['status'] as String? ?? 'running';
            final count = job['records_inserted'] as int? ?? 0;

            if (_platformStatuses.containsKey(plat)) {
              _platformStatuses[plat] = _platformStatuses[plat]!.copyWith(
                isFinished: jobStatus == 'completed',
                recordsFound: count,
                isFailed: jobStatus == 'failed',
              );
            }
          }
        }

        if (overallStatus == 'completed') {
          _isCompleted = true;
          _pollingTimer?.cancel();
          ref.read(dashboardProvider.notifier).refresh();
        }
      });
    } catch (e) {
      // Background poll failure, wait for next tick
      if (_secondsElapsed > 35 && _scanStatus == null && mounted) {
        setState(() {
          _errorMessage = 'Scan is taking longer than expected. You can check the dashboard now.';
        });
      }
    }
  }

  @override
  void dispose() {
    _pollingTimer?.cancel();
    _pulseController.dispose();
    super.dispose();
  }

  void _proceedToDashboard() {
    ref.read(dashboardProvider.notifier).refresh();
    context.go('/dashboard');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundDark,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xl),
          child: Column(
            children: [
              const SizedBox(height: AppSpacing.xxl),

              // ── Animated Radar Sonar Visual ──
              Center(
                child: SizedBox(
                  width: 140,
                  height: 140,
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      // Outer glowing pulse ring
                      AnimatedBuilder(
                        animation: _pulseAnimation,
                        builder: (context, child) {
                          return Container(
                            width: 130 * _pulseAnimation.value,
                            height: 130 * _pulseAnimation.value,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: _isCompleted
                                  ? AppColors.positive.withValues(alpha: 0.12)
                                  : AppColors.primary.withValues(alpha: 0.12),
                            ),
                          );
                        },
                      ),
                      // Inner ring
                      Container(
                        width: 96,
                        height: 96,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: _isCompleted
                              ? AppColors.positive.withValues(alpha: 0.2)
                              : AppColors.primary.withValues(alpha: 0.2),
                          border: Border.all(
                            color: _isCompleted
                                ? AppColors.positiveLight
                                : AppColors.primaryLight,
                            width: 2,
                          ),
                        ),
                      ),
                      // Center Icon
                      Icon(
                        _isCompleted
                            ? Icons.check_circle_rounded
                            : Icons.radar_rounded,
                        size: 48,
                        color: _isCompleted
                            ? AppColors.positive
                            : AppColors.primaryLight,
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: AppSpacing.xl),

              // ── Status Title & Subtitle ──
              Text(
                _isCompleted
                    ? 'Intelligence Acquired!'
                    : 'Getting & Scraping Data',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: AppColors.textPrimaryDark,
                    ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: AppSpacing.sm),

              Text(
                _isCompleted
                    ? 'Authentic customer reviews and social mentions have been ingested and analyzed.'
                    : 'Extracting live reputation data across Google Maps, Reddit, and X. Please wait...',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: AppColors.textSecondaryDark,
                    ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: AppSpacing.xxl),

              // ── Pipeline Progress Cards ──
              Expanded(
                child: ListView(
                  children: [
                    ..._platformStatuses.entries.map((entry) {
                      final status = entry.value;
                      final isPlatformDone = _isCompleted || status.isFinished;

                      return Container(
                        margin: const EdgeInsets.only(bottom: AppSpacing.md),
                        padding: const EdgeInsets.all(AppSpacing.base),
                        decoration: BoxDecoration(
                          color: AppColors.cardDark,
                          borderRadius: BorderRadius.circular(AppRadius.md),
                          border: Border.all(
                            color: isPlatformDone
                                ? AppColors.positive.withValues(alpha: 0.4)
                                : AppColors.glassBorder,
                          ),
                        ),
                        child: Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(AppSpacing.sm),
                              decoration: BoxDecoration(
                                color: status.color.withValues(alpha: 0.15),
                                borderRadius:
                                    BorderRadius.circular(AppRadius.sm),
                              ),
                              child: Icon(status.icon,
                                  color: status.color, size: 22),
                            ),
                            const SizedBox(width: AppSpacing.base),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    status.name,
                                    style: const TextStyle(
                                      fontWeight: FontWeight.w600,
                                      fontSize: 14,
                                      color: AppColors.textPrimaryDark,
                                    ),
                                  ),
                                  const SizedBox(height: 2),
                                  Text(
                                    isPlatformDone
                                        ? (status.recordsFound > 0
                                            ? '${status.recordsFound} authentic records scraped'
                                            : 'Completed & synced')
                                        : 'Querying and filtering discussions...',
                                    style: TextStyle(
                                      fontSize: 12,
                                      color: isPlatformDone
                                          ? AppColors.positiveLight
                                          : AppColors.textSecondaryDark,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            if (isPlatformDone)
                              const Icon(Icons.check_circle_rounded,
                                  color: AppColors.positive, size: 22)
                            else
                              const SizedBox(
                                width: 18,
                                height: 18,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  valueColor: AlwaysStoppedAnimation<Color>(
                                      AppColors.primaryLight),
                                ),
                              ),
                          ],
                        ),
                      );
                    }),

                    // AI Processing Stage
                    Container(
                      margin: const EdgeInsets.only(bottom: AppSpacing.md),
                      padding: const EdgeInsets.all(AppSpacing.base),
                      decoration: BoxDecoration(
                        color: AppColors.cardDark,
                        borderRadius: BorderRadius.circular(AppRadius.md),
                        border: Border.all(
                          color: _isCompleted
                              ? AppColors.positive.withValues(alpha: 0.4)
                              : AppColors.glassBorder,
                        ),
                      ),
                      child: Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(AppSpacing.sm),
                            decoration: BoxDecoration(
                              color: AppColors.primary.withValues(alpha: 0.15),
                              borderRadius:
                                  BorderRadius.circular(AppRadius.sm),
                            ),
                            child: const Icon(
                              Icons.auto_awesome_rounded,
                              color: AppColors.primaryLight,
                              size: 22,
                            ),
                          ),
                          const SizedBox(width: AppSpacing.base),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'AI Sentiment & Threat Synthesis',
                                  style: TextStyle(
                                    fontWeight: FontWeight.w600,
                                    fontSize: 14,
                                    color: AppColors.textPrimaryDark,
                                  ),
                                ),
                                const SizedBox(height: 2),
                                Text(
                                  _isCompleted
                                      ? 'Reputation score & findings calculated'
                                      : 'Calculating sentiment and fraud vectors...',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: _isCompleted
                                        ? AppColors.positiveLight
                                        : AppColors.textSecondaryDark,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          if (_isCompleted)
                            const Icon(Icons.check_circle_rounded,
                                color: AppColors.positive, size: 22)
                          else
                            const SizedBox(
                              width: 18,
                              height: 18,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                valueColor: AlwaysStoppedAnimation<Color>(
                                    AppColors.primaryLight),
                              ),
                            ),
                        ],
                      ),
                    ),

                    if (_errorMessage != null) ...[
                      const SizedBox(height: AppSpacing.md),
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.base),
                        decoration: BoxDecoration(
                          color: AppColors.cardDark,
                          borderRadius: BorderRadius.circular(AppRadius.md),
                          border: Border.all(color: AppColors.accentWarning),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.info_outline_rounded,
                                color: AppColors.accentWarning),
                            const SizedBox(width: AppSpacing.base),
                            Expanded(
                              child: Text(
                                _errorMessage!,
                                style: const TextStyle(
                                  fontSize: 13,
                                  color: AppColors.textPrimaryDark,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ],
                ),
              ),

              // ── Action Controls ──
              Padding(
                padding: const EdgeInsets.symmetric(vertical: AppSpacing.xl),
                child: Column(
                  children: [
                    SizedBox(
                      width: double.infinity,
                      height: 52,
                      child: ElevatedButton(
                        onPressed: _proceedToDashboard,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: _isCompleted
                              ? AppColors.positive
                              : AppColors.primary,
                        ),
                        child: Text(
                          _isCompleted
                              ? 'View Dashboard'
                              : 'Proceed to Dashboard',
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                    ),
                    if (!_isCompleted) ...[
                      const SizedBox(height: AppSpacing.sm),
                      TextButton.icon(
                        onPressed: () {
                          ref.read(apiServiceProvider).triggerScan();
                          _startPolling();
                        },
                        icon: const Icon(Icons.refresh_rounded, size: 18),
                        label: const Text('Refresh / Retry Scan'),
                      ),
                    ],
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _PlatformStatus {
  final String name;
  final IconData icon;
  final Color color;
  final bool isFinished;
  final int recordsFound;
  final bool isFailed;

  const _PlatformStatus({
    required this.name,
    required this.icon,
    required this.color,
    this.isFinished = false,
    this.recordsFound = 0,
    this.isFailed = false,
  });

  _PlatformStatus copyWith({
    bool? isFinished,
    int? recordsFound,
    bool? isFailed,
  }) {
    return _PlatformStatus(
      name: name,
      icon: icon,
      color: color,
      isFinished: isFinished ?? this.isFinished,
      recordsFound: recordsFound ?? this.recordsFound,
      isFailed: isFailed ?? this.isFailed,
    );
  }
}
