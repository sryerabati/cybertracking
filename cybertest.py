from flask import Flask, request, send_file, redirect, send_from_directory
from datetime import datetime
import os

app = Flask(__name__)

# === TRACKING PIXEL ===
@app.route('/track/<email_id>.png')
def track_pixel(email_id):
    log_line = f"[{datetime.now()}] EMAIL OPENED: {email_id} - IP: {request.remote_addr} - UA: {request.headers.get('User-Agent')}\n"
    with open("open_log.txt", "a") as f:
        f.write(log_line)
    return send_file("pixel.png", mimetype='image/png')

# === CLICK REDIRECT ===
@app.route('/r')
def click_tracker():
    user = request.args.get('u', 'unknown')
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')

    log_line = f"[{datetime.now()}] LINK CLICKED: {user} - IP: {ip} - UA: {ua}\n"
    with open("click_log.txt", "a") as f:
        f.write(log_line)

    return redirect("https://alwaysjudgeabookbyitscover.com/", code=302)

# === OPTIONAL: HANDLE FAVICON ===
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# === ENTRYPOINT ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # fallback to 10000 for local
    app.run(host='0.0.0.0', port=port)
