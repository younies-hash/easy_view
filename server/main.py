import time
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import pyautogui
import os

try:
    with open('urls.json') as f:
        urls = json.load(f)
except FileNotFoundError:
    urls = {"youtube_tv": "https://www.youtube.com/tv"}
    
    
app = Flask(__name__)
CORS(app)

def get_path():
    # Check both common Edge installation paths
    paths_to_check = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    for path in paths_to_check:
        if os.path.exists(path):
            return path
    return None
    
SMART_TV_USER_AGENT = "Mozilla/5.0 (SMART-TV; Linux; Tizen 4.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"


@app.route('/tv/start')
def start(url=urls['youtube_tv']):
    browser_path = get_path()
    if not browser_path:
        return jsonify({'status': 'Browser excutable not found'})
    
    # launch browser
    profile_dir = os.path.join(os.getcwd(), "edge_tv_profile")
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)

    subprocess.Popen([
        browser_path, 
        f'--user-data-dir={profile_dir}', # Completely isolates this session
        '--kiosk',
        '--edge-kiosk-type=fullscreen',
        f'--user-agent={SMART_TV_USER_AGENT}', 
        '--disable-translate',
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
    url = data.get('url')
    
    print(f"Received command: {action}")

    # 2. Execute the command based on the action
    if action == 'shutdown':
        # Windows shutdown command (use 'shutdown /h' for hibernate, or adjust for Mac/Linux)
        os.system("shutdown /s /t 0")
        return jsonify({'status': 'success', 'message': 'Shutting down'})
        
    elif action == 'vol_up':
        pyautogui.press('volumeup')
        return jsonify({'status': 'success', 'message': 'Volume Up'})
        
    elif action == 'vol_down':
        pyautogui.press('volumedown')
        return jsonify({'status': 'success', 'message': 'Volume Down'})
        
    elif action == 'mute':
        pyautogui.press('volumemute')
        return jsonify({'status': 'success', 'message': 'Muted'})
    elif action == 'play_pause':
        # Spacebar is the universal play/pause toggle for YouTube TV and most media players
        pyautogui.press('space')
        return jsonify({'status': 'success', 'message': 'Play/Pause'})
        
    elif action == 'next':
        pyautogui.press('nexttrack') # or pyautogui.hotkey('shift', 'n') for YouTube specifically
        return jsonify({'status': 'success', 'message': 'Next'})
        
    elif action == 'prev':
        pyautogui.press('prevtrack')
        return jsonify({'status': 'success', 'message': 'Previous'})
        
    elif action == 'channel':
        return start(url=url)
    
    else:
        return jsonify({'status': 'error', 'message': 'Unknown command'}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)