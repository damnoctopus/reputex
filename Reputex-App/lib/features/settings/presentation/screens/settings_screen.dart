import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/theme.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../../onboarding/presentation/providers/business_provider.dart';

/// Settings screen with business, monitoring, alert, API mode, and account sections.
class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);
    final businessState = ref.watch(businessProvider);

    final businessName = businessState.valueOrNull?.name ?? 'My Business';
    final userEmail = authState.user?.email ?? 'user@reputex.ai';

    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        padding: const EdgeInsets.all(AppSpacing.xl),
        children: [
          // ── Business ──
          const _SectionHeader(title: 'Business'),
          _SettingsTile(
            icon: Icons.store_rounded,
            title: 'Business Profile',
            subtitle: businessName,
            onTap: () {},
          ),

          const SizedBox(height: AppSpacing.xl),

          // ── API Configuration ──
          const _SectionHeader(title: 'Backend Configuration'),
          const _SettingsTile(
            icon: Icons.cloud_done_rounded,
            title: 'Backend Service',
            subtitle: 'Live FastAPI Backend (Real Data Pipeline)',
            trailing: Icon(Icons.check_circle_rounded, color: AppColors.positive),
          ),

          const SizedBox(height: AppSpacing.xl),

          // ── Monitoring ──
          const _SectionHeader(title: 'Monitoring'),
          _SettingsTile(
            icon: Icons.tag_rounded,
            title: 'Brand Keywords',
            subtitle: '3 active keywords',
            onTap: () {},
          ),
          _SettingsTile(
            icon: Icons.language_rounded,
            title: 'Platforms',
            subtitle: 'Reddit, X, Google News, JustDial, Sulekha...',
            onTap: () {},
          ),

          const SizedBox(height: AppSpacing.xl),

          // ── Alerts ──
          const _SectionHeader(title: 'Alerts'),
          _SettingsTile(
            icon: Icons.crisis_alert_outlined,
            title: 'Crisis Threshold',
            subtitle: '40% negative sentiment',
            onTap: () {},
          ),
          _SettingsTile(
            icon: Icons.policy_outlined,
            title: 'Fraud Threshold',
            subtitle: '60% fraud probability',
            onTap: () {},
          ),
          _SettingsTile(
            icon: Icons.notifications_outlined,
            title: 'Push Notifications',
            subtitle: 'Enabled (FCM)',
            trailing: Switch(
              value: true,
              onChanged: (v) {},
              activeThumbColor: AppColors.primary,
            ),
          ),
          _SettingsTile(
            icon: Icons.chat_outlined,
            title: 'WhatsApp Alerts',
            subtitle: 'Coming soon',
            enabled: false,
            trailing: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              decoration: BoxDecoration(
                color: AppColors.primary.withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(AppRadius.full),
              ),
              child: const Text(
                'Soon',
                style: TextStyle(
                  color: AppColors.primary,
                  fontSize: 10,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ),

          const SizedBox(height: AppSpacing.xl),

          // ── AI ──
          const _SectionHeader(title: 'AI Responses'),
          _SettingsTile(
            icon: Icons.auto_awesome_outlined,
            title: 'Default Response Tone',
            subtitle: 'Empathetic',
            onTap: () {},
          ),

          const SizedBox(height: AppSpacing.xl),

          // ── Account ──
          const _SectionHeader(title: 'Account'),
          _SettingsTile(
            icon: Icons.email_outlined,
            title: 'Email',
            subtitle: userEmail,
            onTap: () {},
          ),
          _SettingsTile(
            icon: Icons.lock_outlined,
            title: 'Change Password',
            onTap: () {},
          ),
          const SizedBox(height: AppSpacing.base),
          _SettingsTile(
            icon: Icons.logout_rounded,
            title: 'Sign Out',
            iconColor: AppColors.negative,
            titleColor: AppColors.negative,
            onTap: () {
              showDialog(
                context: context,
                builder: (ctx) => AlertDialog(
                  title: const Text('Sign Out'),
                  content: const Text('Are you sure you want to sign out?'),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(ctx),
                      child: const Text('Cancel'),
                    ),
                    TextButton(
                      onPressed: () async {
                        Navigator.pop(ctx);
                        await ref.read(authProvider.notifier).logout();
                        if (context.mounted) {
                          context.go('/login');
                        }
                      },
                      child: const Text(
                        'Sign Out',
                        style: TextStyle(color: AppColors.negative),
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
          const SizedBox(height: AppSpacing.xxl),
          Center(
            child: Text(
              'RepuTex v1.0.0 (Phase 5 Complete)',
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ),
          const SizedBox(height: AppSpacing.xl),
        ],
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  const _SectionHeader({required this.title});
  final String title;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppSpacing.md),
      child: Text(
        title,
        style: Theme.of(context).textTheme.labelLarge
            ?.copyWith(color: AppColors.textTertiaryDark, letterSpacing: 0.5),
      ),
    );
  }
}

class _SettingsTile extends StatelessWidget {
  const _SettingsTile({
    required this.icon,
    required this.title,
    this.subtitle,
    this.onTap,
    this.trailing,
    this.enabled = true,
    this.iconColor,
    this.titleColor,
  });

  final IconData icon;
  final String title;
  final String? subtitle;
  final VoidCallback? onTap;
  final Widget? trailing;
  final bool enabled;
  final Color? iconColor;
  final Color? titleColor;

  @override
  Widget build(BuildContext context) {
    return Opacity(
      opacity: enabled ? 1.0 : 0.5,
      child: Material(
        color: Colors.transparent,
        child: ListTile(
          contentPadding: const EdgeInsets.symmetric(
            horizontal: AppSpacing.base,
            vertical: AppSpacing.xs,
          ),
          leading: Icon(icon, color: iconColor ?? AppColors.textSecondaryDark),
          title: Text(title, style: TextStyle(color: titleColor)),
          subtitle: subtitle != null
              ? Text(subtitle!, style: Theme.of(context).textTheme.bodySmall)
              : null,
          trailing:
              trailing ??
              (onTap != null
                  ? const Icon(
                      Icons.chevron_right_rounded,
                      color: AppColors.textTertiaryDark,
                    )
                  : null),
          onTap: enabled ? onTap : null,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadius.md),
          ),
        ),
      ),
    );
  }
}
