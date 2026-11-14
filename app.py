from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Dieses Projekt heißt: \"Partizipations-Tool\""


@app.route('/health')
def health():
    return {"status": "ok"}
