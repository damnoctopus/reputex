import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/theme.dart';
import '../../../../core/constants/app_constants.dart';
import '../providers/business_provider.dart';

/// Business setup wizard — onboarding flow after registration.
class BusinessSetupScreen extends ConsumerStatefulWidget {
  const BusinessSetupScreen({super.key});

  @override
  ConsumerState<BusinessSetupScreen> createState() =>
      _BusinessSetupScreenState();
}

class _BusinessSetupScreenState extends ConsumerState<BusinessSetupScreen> {
  final _pageController = PageController();
  int _currentStep = 0;

  // Step 1: Business Info
  final _businessNameController = TextEditingController(text: 'Spice Symphony');
  final _locationController = TextEditingController(
    text: 'Indiranagar, Bengaluru',
  );
  final _descriptionController = TextEditingController();
  String _category = 'Restaurant';

  // Step 2: Keywords
  final _keywordController = TextEditingController();
  final List<String> _keywords = [
    'Spice Symphony',
    'Spice Symphony Indiranagar',
    'best biryani Indiranagar',
  ];

  // Step 3: Platforms
  final Map<String, bool> _platforms = {
    for (final p in AppConstants.platforms) p: true,
  };

  @override
  void dispose() {
    _pageController.dispose();
    _businessNameController.dispose();
    _locationController.dispose();
    _descriptionController.dispose();
    _keywordController.dispose();
    super.dispose();
  }

  void _nextStep() {
    if (_currentStep < 2) {
      _pageController.nextPage(
        duration: AppDurations.normal,
        curve: Curves.easeInOut,
      );
      setState(() => _currentStep++);
    } else {
      _finishSetup();
    }
  }

  void _previousStep() {
    if (_currentStep > 0) {
      _pageController.previousPage(
        duration: AppDurations.normal,
        curve: Curves.easeInOut,
      );
      setState(() => _currentStep--);
    }
  }

  void _addKeyword() {
    final keyword = _keywordController.text.trim();
    if (keyword.isNotEmpty && !_keywords.contains(keyword)) {
      setState(() {
        _keywords.add(keyword);
        _keywordController.clear();
      });
    }
  }

  Future<void> _finishSetup() async {
    final selectedPlatforms = _platforms.entries
        .where((e) => e.value)
        .map((e) => e.key)
        .toList();

    await ref
        .read(businessProvider.notifier)
        .setupBusiness(
          name: _businessNameController.text.trim().isNotEmpty
              ? _businessNameController.text.trim()
              : 'Spice Symphony',
          category: _category,
          location: _locationController.text.trim(),
          keywords: _keywords.isNotEmpty
              ? _keywords
              : const ['Spice Symphony', 'Spice Symphony Indiranagar'],
          platforms: selectedPlatforms.isNotEmpty
              ? selectedPlatforms
              : const ['Google', 'JustDial', 'Reddit'],
        );

    if (mounted) {
      context.go('/dashboard');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Set Up Your Business'),
        leading: _currentStep > 0
            ? IconButton(
                icon: const Icon(Icons.arrow_back_rounded),
                onPressed: _previousStep,
              )
            : null,
      ),
      body: Column(
        children: [
          // ── Step Indicator ──
          Padding(
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.xl,
              vertical: AppSpacing.base,
            ),
            child: Row(
              children: List.generate(3, (index) {
                final isActive = index <= _currentStep;
                return Expanded(
                  child: Container(
                    height: 4,
                    margin: const EdgeInsets.symmetric(horizontal: 2),
                    decoration: BoxDecoration(
                      color: isActive
                          ? AppColors.primary
                          : AppColors.borderDark,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                );
              }),
            ),
          ),

          // ── Pages ──
          Expanded(
            child: PageView(
              controller: _pageController,
              physics: const NeverScrollableScrollPhysics(),
              children: [
                _buildBusinessInfoStep(),
                _buildKeywordsStep(),
                _buildPlatformsStep(),
              ],
            ),
          ),

          // ── Next/Finish Button ──
          Padding(
            padding: const EdgeInsets.all(AppSpacing.xl),
            child: SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                onPressed: _nextStep,
                child: Text(_currentStep == 2 ? 'Get Started' : 'Continue'),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBusinessInfoStep() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(AppSpacing.xl),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Business Information',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: AppSpacing.sm),
          Text(
            'Tell us about your business',
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: AppSpacing.xl),
          TextFormField(
            controller: _businessNameController,
            decoration: const InputDecoration(
              labelText: 'Business Name',
              prefixIcon: Icon(Icons.business_outlined),
            ),
          ),
          const SizedBox(height: AppSpacing.base),
          DropdownButtonFormField<String>(
            initialValue: _category,
            decoration: const InputDecoration(
              labelText: 'Category',
              prefixIcon: Icon(Icons.category_outlined),
            ),
            items: const [
              DropdownMenuItem(value: 'Restaurant', child: Text('Restaurant')),
              DropdownMenuItem(value: 'Hotel', child: Text('Hotel')),
              DropdownMenuItem(value: 'Retail', child: Text('Retail')),
              DropdownMenuItem(value: 'Healthcare', child: Text('Healthcare')),
              DropdownMenuItem(value: 'Education', child: Text('Education')),
              DropdownMenuItem(value: 'Technology', child: Text('Technology')),
              DropdownMenuItem(value: 'Services', child: Text('Services')),
              DropdownMenuItem(value: 'Other', child: Text('Other')),
            ],
            onChanged: (v) {
              if (v != null) setState(() => _category = v);
            },
          ),
          const SizedBox(height: AppSpacing.base),
          TextFormField(
            controller: _locationController,
            decoration: const InputDecoration(
              labelText: 'Location',
              prefixIcon: Icon(Icons.location_on_outlined),
            ),
          ),
          const SizedBox(height: AppSpacing.base),
          TextFormField(
            controller: _descriptionController,
            maxLines: 3,
            decoration: const InputDecoration(
              labelText: 'Description',
              prefixIcon: Icon(Icons.description_outlined),
              alignLabelWithHint: true,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildKeywordsStep() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(AppSpacing.xl),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Brand Keywords',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: AppSpacing.sm),
          Text(
            'Add keywords we should monitor for your brand',
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: AppSpacing.xl),
          Row(
            children: [
              Expanded(
                child: TextFormField(
                  controller: _keywordController,
                  decoration: const InputDecoration(
                    hintText: 'Enter a keyword',
                    prefixIcon: Icon(Icons.tag_rounded),
                  ),
                  onFieldSubmitted: (_) => _addKeyword(),
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              IconButton.filled(
                onPressed: _addKeyword,
                icon: const Icon(Icons.add_rounded),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.base),
          Wrap(
            spacing: AppSpacing.sm,
            runSpacing: AppSpacing.sm,
            children: _keywords
                .map(
                  (k) => Chip(
                    label: Text(k),
                    deleteIcon: const Icon(Icons.close, size: 16),
                    onDeleted: () => setState(() => _keywords.remove(k)),
                  ),
                )
                .toList(),
          ),
          if (_keywords.isEmpty)
            Padding(
              padding: const EdgeInsets.only(top: AppSpacing.xxl),
              child: Center(
                child: Text(
                  'Add your brand name, product names,\nand common aliases',
                  style: Theme.of(context).textTheme.bodySmall,
                  textAlign: TextAlign.center,
                ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildPlatformsStep() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(AppSpacing.xl),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Monitoring Platforms',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: AppSpacing.sm),
          Text(
            'Select platforms to monitor for mentions',
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: AppSpacing.xl),
          ..._platforms.entries.map((entry) {
            return Container(
              margin: const EdgeInsets.only(bottom: AppSpacing.sm),
              decoration: BoxDecoration(
                color: AppColors.cardDark,
                borderRadius: BorderRadius.circular(AppRadius.md),
                border: Border.all(
                  color: entry.value
                      ? AppColors.primary.withValues(alpha: 0.3)
                      : AppColors.borderDark,
                ),
              ),
              child: CheckboxListTile(
                title: Text(entry.key),
                value: entry.value,
                activeColor: AppColors.primary,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(AppRadius.md),
                ),
                onChanged: (v) {
                  setState(() => _platforms[entry.key] = v ?? false);
                },
              ),
            );
          }),
        ],
      ),
    );
  }
}
