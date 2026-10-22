import time
import json
from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import pyautogui
import os

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

@app.route('/tv/up')
def press_up():
    pyautogui.press('up')
    return jsonify({'status': 'nav up'})

@app.route('/tv/down')
def press_down():
    pyautogui.press('down')
    return jsonify({'status': 'nav down'})

@app.route('/tv/select')
def select():
    pyautogui.press('enter')
    return jsonify({'status': 'selecte'})

@app.route('/tv/back')
def press_back():
    pyautogui.press('esc')
    return jsonify({'status': 'back'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)