import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Override at build/run time if the PC's LAN IP changes:
  // flutter run --dart-define=SERVER_URL=http://192.168.1.3:5000
  static const String baseUrl = String.fromEnvironment(
    'SERVER_URL',
    defaultValue: 'http://192.168.1.3:5000',
  );

  static Future<bool> sendCommand(String action, {String? channelUrl}) async {
    final endpoint = Uri.parse('$baseUrl/command');

    try {
      final response = await http
          .post(
            endpoint,
            headers: const {'Content-Type': 'application/json'},
            body: jsonEncode({
              'action': action,
              if (channelUrl != null && channelUrl.isNotEmpty)
                'url': channelUrl,
            }),
          )
          .timeout(const Duration(seconds: 5));

      if (response.statusCode == 200) {
        print('Command "$action" sent');
        return true;
      }
      print('Server responded with status: ${response.statusCode} ${response.body}');
      return false;
    } catch (e) {
      print('Error connecting to Easy View server at $endpoint: $e');
      return false;
    }
  }
}
