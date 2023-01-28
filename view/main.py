from flask import render_template
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', name="test")