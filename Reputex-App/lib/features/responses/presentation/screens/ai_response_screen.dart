import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../app/theme.dart';
import '../../../mentions/presentation/providers/mentions_feed_provider.dart';
import '../providers/response_provider.dart';

/// AI response generation, editing, and approval screen.
class AiResponseScreen extends ConsumerStatefulWidget {
  const AiResponseScreen({super.key, required this.mentionId});

  final String mentionId;

  @override
  ConsumerState<AiResponseScreen> createState() => _AiResponseScreenState();
}

class _AiResponseScreenState extends ConsumerState<AiResponseScreen> {
  bool _isEditing = false;
  String _selectedTone = 'Empathetic';
  late TextEditingController _responseController;

  static const _tones = ['Empathetic', 'Professional', 'Firm', 'Promotional'];

  @override
  void initState() {
    super.initState();
    _responseController = TextEditingController();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _triggerGeneration();
    });
  }

  @override
  void dispose() {
    _responseController.dispose();
    super.dispose();
  }

  void _triggerGeneration() {
    ref
        .read(aiResponseProvider(widget.mentionId).notifier)
        .generate(tone: _selectedTone.toLowerCase());
  }

  @override
  Widget build(BuildContext context) {
    final mentionAsync = ref.watch(mentionDetailProvider(widget.mentionId));
    final responseAsync = ref.watch(aiResponseProvider(widget.mentionId));

    // Sync text controller with response data
    ref.listen(aiResponseProvider(widget.mentionId), (_, next) {
      if (next.hasValue && next.value != null && !_isEditing) {
        _responseController.text = next.value!.generatedResponse;
      }
    });

    final isGenerating = responseAsync.isLoading;
    final isApproved =
        responseAsync.valueOrNull?.status == 'approved' ||
        responseAsync.valueOrNull?.status == 'dispatched';

    return Scaffold(
      appBar: AppBar(title: const Text('AI Response')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(AppSpacing.xl),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // ── Original Review ──
            Text(
              'Original Review',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: AppSpacing.md),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(AppSpacing.base),
              decoration: BoxDecoration(
                color: AppColors.cardDark,
                borderRadius: BorderRadius.circular(AppRadius.lg),
                border: Border.all(color: AppColors.glassBorder),
              ),
              child: mentionAsync.when(
                loading: () => const Text(
                  'Loading review content...',
                  style: TextStyle(color: AppColors.textTertiaryDark),
                ),
                error: (err, stack) => const Text('Could not load review.'),
                data: (mention) => Text(
                  '"${mention.content}"',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontStyle: FontStyle.italic,
                    color: AppColors.textPrimaryDark,
                    height: 1.6,
                  ),
                ),
              ),
            ),

            const SizedBox(height: AppSpacing.xl),

            // ── Tone Selector ──
            Text(
              'Response Tone',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: AppSpacing.md),
            Wrap(
              spacing: AppSpacing.sm,
              children: _tones.map((tone) {
                final isSelected = tone == _selectedTone;
                return ChoiceChip(
                  label: Text(tone),
                  selected: isSelected,
                  onSelected: (_) {
                    setState(() => _selectedTone = tone);
                    _triggerGeneration();
                  },
                  selectedColor: AppColors.primary.withValues(alpha: 0.2),
                  checkmarkColor: AppColors.primary,
                  labelStyle: TextStyle(
                    color: isSelected
                        ? AppColors.primary
                        : AppColors.textSecondaryDark,
                    fontWeight: isSelected
                        ? FontWeight.w600
                        : FontWeight.normal,
                  ),
                );
              }).toList(),
            ),

            const SizedBox(height: AppSpacing.xl),

            // ── Generated Response ──
            Row(
              children: [
                Text(
                  'Generated Response',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const Spacer(),
                if (!isGenerating && !isApproved)
                  TextButton.icon(
                    onPressed: () {
                      setState(() => _isEditing = !_isEditing);
                    },
                    icon: Icon(
                      _isEditing ? Icons.check_rounded : Icons.edit_rounded,
                      size: 16,
                    ),
                    label: Text(_isEditing ? 'Done' : 'Edit'),
                  ),
              ],
            ),
            const SizedBox(height: AppSpacing.md),

            if (isGenerating)
              Container(
                width: double.infinity,
                height: 200,
                padding: const EdgeInsets.all(AppSpacing.xl),
                decoration: BoxDecoration(
                  color: AppColors.cardDark,
                  borderRadius: BorderRadius.circular(AppRadius.lg),
                  border: Border.all(color: AppColors.glassBorder),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SizedBox(
                      width: 32,
                      height: 32,
                      child: CircularProgressIndicator(
                        strokeWidth: 2.5,
                        color: AppColors.primary.withValues(alpha: 0.7),
                      ),
                    ),
                    const SizedBox(height: AppSpacing.base),
                    Text(
                      'Generating response...',
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                  ],
                ),
              )
            else
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(AppSpacing.base),
                decoration: BoxDecoration(
                  color: isApproved
                      ? AppColors.positive.withValues(alpha: 0.05)
                      : AppColors.cardDark,
                  borderRadius: BorderRadius.circular(AppRadius.lg),
                  border: Border.all(
                    color: isApproved
                        ? AppColors.positive.withValues(alpha: 0.3)
                        : AppColors.glassBorder,
                  ),
                ),
                child: _isEditing
                    ? TextField(
                        controller: _responseController,
                        maxLines: null,
                        decoration: const InputDecoration(
                          border: InputBorder.none,
                          fillColor: Colors.transparent,
                          filled: true,
                        ),
                        style: Theme.of(context).textTheme.bodyLarge
                            ?.copyWith(height: 1.6),
                      )
                    : Text(
                        _responseController.text.isNotEmpty
                            ? _responseController.text
                            : responseAsync.valueOrNull?.generatedResponse ?? 'Press Regenerate to create an AI response draft.',
                        style: Theme.of(context).textTheme.bodyLarge
                            ?.copyWith(height: 1.6),
                      ),
              ),

            const SizedBox(height: AppSpacing.xl),

            // ── Actions ──
            if (!isGenerating) ...[
              if (isApproved)
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(AppSpacing.base),
                  decoration: BoxDecoration(
                    color: AppColors.positive.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(AppRadius.md),
                  ),
                  child: const Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.check_circle_rounded,
                        color: AppColors.positive,
                      ),
                      SizedBox(width: AppSpacing.sm),
                      Text(
                        'Response Approved',
                        style: TextStyle(
                          color: AppColors.positive,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                )
              else
                Row(
                  children: [
                    Expanded(
                      child: OutlinedButton.icon(
                        onPressed: _triggerGeneration,
                        icon: const Icon(Icons.refresh_rounded, size: 18),
                        label: const Text('Regenerate'),
                      ),
                    ),
                    const SizedBox(width: AppSpacing.md),
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: () async {
                          final messenger = ScaffoldMessenger.of(context);
                          final text = _responseController.text.trim();
                          final success = await ref
                              .read(
                                aiResponseProvider(widget.mentionId).notifier,
                              )
                              .approve(text: text);
                          if (mounted && success) {
                            messenger.showSnackBar(
                              const SnackBar(
                                content: Text(
                                  'Response approved successfully!',
                                ),
                              ),
                            );
                          }
                        },
                        icon: const Icon(Icons.check_rounded, size: 18),
                        label: const Text('Approve'),
                      ),
                    ),
                  ],
                ),
            ],
            const SizedBox(height: AppSpacing.xl),
          ],
        ),
      ),
    );
  }
}
