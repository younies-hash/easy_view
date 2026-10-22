import 'package:easy_view_client/api.dart';
import 'package:flutter/material.dart';

// Helper widget for the dock buttons to keep code clean
Widget buildControlButton(
  BuildContext context,
  String label, {
  IconData icon = Icons.tv,
  bool isLarge = false,
  required String action,
}) {
  return Column(
    mainAxisSize: MainAxisSize.min,
    children: [
      IconButton.filled(
        icon: Icon(icon, size: isLarge ? 32 : 28),
        style: IconButton.styleFrom(
          backgroundColor: isLarge
              ? Theme.of(context).colorScheme.primary
              : Theme.of(context).colorScheme.primaryContainer,
          foregroundColor: isLarge
              ? Theme.of(context).colorScheme.onPrimary
              : Theme.of(context).colorScheme.onPrimaryContainer,
        ),
        onPressed: () async {
          // Optional: Show a loading indicator here
          bool success = await ApiService.sendCommand(action);
          
          if (!success) {
            // Handle error (e.g., show a SnackBar)
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Failed to send command. Check connection.')),
            );
          }
        },
      ),
      const SizedBox(height: 4),
      Text(label,
          style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w500)),
    ],
  );
}
