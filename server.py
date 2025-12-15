from flask import Flask
from waitress import serve

app = Flask(__name__)

@app.route("/")
def hello():
    return "<p>Hello, World!</p>"


def start_server():
    print("Starting web server...")
    serve(app, host="0.0.0.0", port=5280)
