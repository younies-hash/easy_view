import time
import json
from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import pyautogui
import os

from requests import request

with open('urls.json') as f:
    urls = json.load(f)
    
    
app = Flask(__name__)
CORS(app)

def get_path():
    browser_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(browser_path):
        return browser_path
    
SMART_TV_USER_AGENT = "Mozilla/5.0 (SMART-TV; Linux; Tizen 4.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"


@app.route('/tv/start')
def start():
    browser_path = get_path()
    if not browser_path:
        return jsonify({'status': 'Browser excutable not found'})
    url = urls['youtube_tv']
    
    # launch browser
    subprocess.Popen([
        browser_path, 
        '--kiosk',
        '--edge-kiosk-type=fullscreen',
        f'--user-agent={SMART_TV_USER_AGENT}',
        '--new-window',
        url
        ])
    
    time.sleep(5)
    return jsonify({'status': 'TV started'})

@app.route('/command', methods=['POST'])
def handle_command():
    # 1. Get the JSON data from the Flutter app
    data = request.get_json()
    action = data.get('action')
    
    print(f"Received command: {action}")

    # 2. Execute the command based on the action
    if action == 'Vol +':
        pyautogui.press('volumeup')
    elif action == 'Vol -':
        pyautogui.press('volumedown')
    elif action == 'shutdown':
        os.system("shutdown /s /t 0") # Windows shutdown
    else:
        return jsonify({"status": "error", "message": "Unknown command"}), 400

    return jsonify({"status": "success", "message": f"{action} executed"}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)