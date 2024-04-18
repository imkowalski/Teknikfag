
from flask import Flask, render_template, current_app
from datetime import datetime
from main import am
import camera

app = Flask(__name__,static_folder='./static')

@app.route("/")
def index():
    temp, hum = am.read()
    return render_template("index.html", temp=temp, hum=hum, time=60-datetime.now().minute)

@app.route("/img")
def img():
    return current_app.send_static_file("./img/img.png")
    
def run():
    app.run(port=1111,host="0.0.0.0")
