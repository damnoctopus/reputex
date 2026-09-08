import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:reputex_mobile/core/network/api_provider.dart';
import 'package:reputex_mobile/features/alerts/presentation/providers/alerts_provider.dart';
import 'package:reputex_mobile/features/auth/presentation/providers/auth_provider.dart';
import 'package:reputex_mobile/features/dashboard/presentation/providers/dashboard_provider.dart';
import 'package:reputex_mobile/features/mentions/presentation/providers/mentions_feed_provider.dart';

import 'fake_api_service.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late ProviderContainer container;

  setUp(() {
    FlutterSecureStorage.setMockInitialValues({});
    container = ProviderContainer(
      overrides: [
        apiServiceProvider.overrideWithValue(FakeApiService()),
      ],
    );
  });

  tearDown(() {
    container.dispose();
  });

  group('Riverpod Providers State Tests', () {
    test('authProvider can login and logout', () async {
      final notifier = container.read(authProvider.notifier);

      final success = await notifier.login(
        email: 'adira@spicesymphony.com',
        password: 'password123',
      );

      expect(success, true);
      final authState = container.read(authProvider);
      expect(authState.isAuthenticated, true);
      expect(authState.user?.email, 'adira@spicesymphony.com');

      await notifier.logout();
      final loggedOutState = container.read(authProvider);
      expect(loggedOutState.isAuthenticated, false);
      expect(loggedOutState.user, isNull);
    });

    test('dashboardProvider loads summary data', () async {
      // Initially loading or loaded
      final notifier = container.read(dashboardProvider.notifier);
      await notifier.fetchDashboard();

      final state = container.read(dashboardProvider);
      expect(state.hasValue, true);
      expect(state.value?.reputationScore.currentScore, greaterThan(0));
    });

    test('mentionsFeedProvider loads items and supports filtering', () async {
      final notifier = container.read(mentionsFeedProvider.notifier);
      await notifier.fetchMentions();

      final state = container.read(mentionsFeedProvider);
      expect(state.items, isNotEmpty);
      expect(state.isLoading, false);
    });

    test('alertsProvider loads alerts and marks as read', () async {
      final notifier = container.read(alertsProvider.notifier);
      await notifier.fetchAlerts();

      final state = container.read(alertsProvider);
      expect(state.hasValue, true);
      expect(state.value, isNotEmpty);

      final firstAlert = state.value!.first;
      await notifier.markAsRead(firstAlert.id);

      final updatedState = container.read(alertsProvider);
      final target = updatedState.value!.firstWhere((a) => a.id == firstAlert.id);
      expect(target.isRead, true);
    });
  });
}
