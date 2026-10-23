import json
import os
import subprocess
import time
from pathlib import Path
from urllib.parse import urlparse

import pyautogui
from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_URLS = {"youtube": "https://www.youtube.com/"}
try:
    with (BASE_DIR / "urls.json").open(encoding="utf-8") as f:
        URLS = {**DEFAULT_URLS, **json.load(f)}
except FileNotFoundError:
    URLS = DEFAULT_URLS

app = Flask(__name__)
CORS(app)

SMART_TV_USER_AGENT = (
    "Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "SamsungBrowser/5.0 Chrome/94.0.4606.71 TV Safari/537.36"
)


def get_edge_path():
    candidates = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
    ]
    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            return candidate
    return None


def launch_tv(url=None):
    url = url or URLS["aljazeera"]
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return jsonify({"status": "error", "message": "Invalid URL"}), 400

    browser_path = get_edge_path()
    if not browser_path:
        return jsonify({
            "status": "error",
            "message": "Microsoft Edge executable not found"
        }), 500

    profile_dir = BASE_DIR / "edge_tv_profile"
    profile_dir.mkdir(exist_ok=True)
    subprocess.Popen([
        browser_path,
        f"--user-data-dir={profile_dir}",
        "--kiosk",
        f"--user-agent={SMART_TV_USER_AGENT}",
        "--disable-translate",
        "--no-first-run",
        "--new-window",
        "--autoplay-policy=no-user-gesture-required",
        url,
    ])
    return jsonify({"status": "success", "message": "TV browser launched", "url": url})


@app.get("/")
def index():
    return jsonify({
        "name": "Easy View server",
        "status": "running",
        "health": "/health",
        "start_tv": "/tv/start",
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/tv/start")
def start_tv():
    return launch_tv()


@app.post("/command")
def handle_command():
    data = request.get_json(silent=True) or {}
    action = data.get("action")
    channel_url = data.get("url")

    if action == "shutdown":
        # This intentionally shuts down the Windows PC when requested by the remote.
        subprocess.Popen(["shutdown", "/s", "/t", "0"], shell=False)
        return jsonify({"status": "success", "message": "Shutting down"})

    key_actions = {
        "vol_up": ("volumeup", "Volume Up"),
        "vol_down": ("volumedown", "Volume Down"),
        "mute": ("volumemute", "Muted"),
        "play_pause": ("space", "Play/Pause"),
        "next": ("nexttrack", "Next"),
        "prev": ("prevtrack", "Previous"),
    }
    if action in key_actions:
        key, message = key_actions[action]
        pyautogui.press(key)
        return jsonify({"status": "success", "message": message})

    if action == "channel":
        return launch_tv(channel_url)

    return jsonify({"status": "error", "message": f"Unknown command: {action}"}), 400


if __name__ == "__main__":
    # Bind to the LAN so the Flutter app can reach this PC.
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
