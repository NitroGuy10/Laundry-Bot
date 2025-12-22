from flask import Flask
from waitress import serve

app = Flask(__name__, static_folder='site', static_url_path='')


@app.get('/')
def index():
    return app.send_static_file('index.html')


@app.get("/status")
def status():
    return "<p>epic</p>"


def start_server():
    print("Starting web server...")
    serve(app, host="0.0.0.0", port=52800)

