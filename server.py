from flask import Flask, request
from waitress import serve

import gpio
import config

app = Flask(__name__, static_folder='static', static_url_path='')


@app.get('/')
def index():
    return app.send_static_file('index.html')


@app.get("/pin-status")
def pin_status():
    return { "status": gpio.get_washer_pin_status() }


def start_server():
    print("Starting web server...")
    serve(app, host="0.0.0.0", port=int(config.get("port")))

