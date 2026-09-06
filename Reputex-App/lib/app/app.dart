import 'package:flutter/material.dart';

import 'router.dart';
import 'theme.dart';

class ReputexApp extends StatelessWidget {
  const ReputexApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'RepuTex',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.dark,
      routerConfig: appRouter,
    );
  }
}
