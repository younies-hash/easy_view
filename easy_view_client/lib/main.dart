// ignore_for_file: prefer_const_constructors, avoid_print

import 'dart:io';
import 'package:easy_view_client/ui/buttons.dart';
import 'package:flutter/material.dart';

List<Map<String, String>> urls = [
  {"youtube1": "youtube.com/tv"},
  {"youtube2": "youtube.com/tv"},
  {"youtube3": "youtube.com/tv"},
];

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Easy View Remote',
      theme: ThemeData(
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple, brightness: Brightness.dark),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Easy View Remote'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
        actions:[
          // POWER BUTTON
          IconButton(
            icon: const Icon(Icons.power_settings_new, color: Colors.redAccent),
            onPressed: () {
              print('Power Off command sent');
              // TODO: Add HTTP call to shutdown PC
            },
          ),
          ]
      ),
      body: Padding(
          padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            //channels
            Expanded(
              child: SingleChildScrollView(
                child: GridView.builder(
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    crossAxisSpacing: 10,
                    mainAxisSpacing: 10,
                    childAspectRatio: 1.5, // square cells
                  ),
                  shrinkWrap: true, // Use this to make the GridView take only the space it needs
                  physics: NeverScrollableScrollPhysics(), // Disable scrolling for the GridView
                  itemCount: urls.length,
                  itemBuilder: (context, index) {
                    final channelName = urls[index].keys.first;
                    final channelUrl = urls[index].values.first;
                    return ElevatedButton(
                      onPressed: () {
                        // Handle button press
                        print('Button pressed for URL: $channelUrl');
                        // TODO: Add HTTP call to send URL to PC
                      },
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.all(12),
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.tv, size: 32),
                          const SizedBox(height: 8),
                          Text(
                            channelName,
                            textAlign: TextAlign.center,
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ),
            ),
            const SizedBox(height: 24),
        
            Container(
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
              borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.1),
                  blurRadius: 10,
                  offset: const Offset(0, -4),
                ),
              ],
            ),
            padding: const EdgeInsets.fromLTRB(16, 20, 16, 24), // Extra padding at top for breathing room
            
              child: Column(
                children: [
            // PLAYBACK CONTROLS
            const Text('Playback', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildControlButton(Icons.skip_previous, 'Prev'),
                _buildControlButton(Icons.play_arrow, 'Play/Pause', isLarge: true),
                _buildControlButton(Icons.skip_next, 'Next'),
              ],
            ),
            const SizedBox(height: 24),
                  // VOLUME CONTROLS
                  const Text('Volume', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 10),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _buildControlButton(Icons.volume_off, 'Mute'),
                      _buildControlButton(Icons.volume_down, 'Vol -'),
                      _buildControlButton(Icons.volume_up, 'Vol +'),
                    ],
                  ),
                  const SizedBox(height: 24),
                  // 4. STATUS BAR
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.green.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Row(
                      children: [
                        Icon(Icons.wifi, color: Colors.green, size: 20),
                        SizedBox(width: 8),
                        Text('Status: Ready to connect', style: TextStyle(color: Colors.green)),
                      ],
                    ),
                  ),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
// Helper widget for the dock buttons to keep code clean
  Widget _buildControlButton(IconData icon, String label, {bool isLarge = false}) {
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
          onPressed: () {
            print('$label pressed');
          },
        ),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w500)),
      ],
    );
  }
}

