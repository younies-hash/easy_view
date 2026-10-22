import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://192.168.1.4:5000'; 

  /// Sends a command to the PC server
  static Future<bool> sendCommand(String action) async {
    final url = Uri.parse('$baseUrl/command');
    
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'action': action}),
      );

      if (response.statusCode == 200) {
        print('✅ Command "$action" sent successfully!');
        return true;
      } else {
        print('❌ Server responded with status: ${response.statusCode}');
        return false;
      }
    } catch (e) {
      print('🚨 Network Error: $e');
      return false;
    }
  }
}