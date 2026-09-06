import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../features/auth/presentation/screens/login_screen.dart';
import '../features/auth/presentation/screens/register_screen.dart';
import '../features/auth/presentation/screens/splash_screen.dart';
import '../features/onboarding/presentation/screens/business_setup_screen.dart';
import '../features/dashboard/presentation/screens/dashboard_screen.dart';
import '../features/mentions/presentation/screens/mentions_screen.dart';
import '../features/mentions/presentation/screens/review_detail_screen.dart';
import '../features/alerts/presentation/screens/alerts_screen.dart';
import '../features/settings/presentation/screens/settings_screen.dart';
import '../features/sentiment/presentation/screens/sentiment_analytics_screen.dart';
import '../features/fraud/presentation/screens/fraud_screen.dart';
import '../features/crisis/presentation/screens/crisis_screen.dart';
import '../features/crisis/presentation/screens/crisis_detail_screen.dart';
import '../features/responses/presentation/screens/ai_response_screen.dart';
import '../core/widgets/bottom_nav_scaffold.dart';

final _rootNavigatorKey = GlobalKey<NavigatorState>();
final _shellNavigatorKey = GlobalKey<NavigatorState>();

final GoRouter appRouter = GoRouter(
  navigatorKey: _rootNavigatorKey,
  initialLocation: '/splash',
  routes: [
    // ── Unauthenticated routes ──
    GoRoute(path: '/splash', builder: (context, state) => const SplashScreen()),
    GoRoute(path: '/login', builder: (context, state) => const LoginScreen()),
    GoRoute(
      path: '/register',
      builder: (context, state) => const RegisterScreen(),
    ),
    GoRoute(
      path: '/onboarding',
      builder: (context, state) => const BusinessSetupScreen(),
    ),

    // ── Main app shell with bottom navigation ──
    ShellRoute(
      navigatorKey: _shellNavigatorKey,
      builder: (context, state, child) => BottomNavScaffold(child: child),
      routes: [
        GoRoute(
          path: '/dashboard',
          pageBuilder: (context, state) =>
              const NoTransitionPage(child: DashboardScreen()),
        ),
        GoRoute(
          path: '/mentions',
          pageBuilder: (context, state) =>
              const NoTransitionPage(child: MentionsScreen()),
        ),
        GoRoute(
          path: '/alerts',
          pageBuilder: (context, state) =>
              const NoTransitionPage(child: AlertsScreen()),
        ),
        GoRoute(
          path: '/settings',
          pageBuilder: (context, state) =>
              const NoTransitionPage(child: SettingsScreen()),
        ),
      ],
    ),

    // ── Detail routes (outside shell, full-screen) ──
    GoRoute(
      path: '/mentions/:id',
      parentNavigatorKey: _rootNavigatorKey,
      builder: (context, state) =>
          ReviewDetailScreen(mentionId: state.pathParameters['id']!),
    ),
    GoRoute(
      path: '/mentions/:id/response',
      parentNavigatorKey: _rootNavigatorKey,
      builder: (context, state) =>
          AiResponseScreen(mentionId: state.pathParameters['id']!),
    ),
    GoRoute(
      path: '/analytics',
      parentNavigatorKey: _rootNavigatorKey,
      builder: (context, state) => const SentimentAnalyticsScreen(),
    ),
    GoRoute(
      path: '/fraud',
      parentNavigatorKey: _rootNavigatorKey,
      builder: (context, state) => const FraudScreen(),
    ),
    GoRoute(
      path: '/crisis',
      parentNavigatorKey: _rootNavigatorKey,
      builder: (context, state) => const CrisisScreen(),
    ),
    GoRoute(
      path: '/crisis/:id',
      parentNavigatorKey: _rootNavigatorKey,
      builder: (context, state) =>
          CrisisDetailScreen(crisisId: state.pathParameters['id']!),
    ),
  ],
);
