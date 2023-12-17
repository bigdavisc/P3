from flask import Flask
import I9000

app = Flask(__name__)
config = {
    "ip": "",
    "port": 0,
    "print_to_console": False,
    "send_to_printer": True,
}

@app.route("/")
def r_home():
    return f"<p>Home<br>{config}</p>"

@app.route("/config/<key>/<value>")
def r_config(key, value):
    config[key] = value
    print(f"CONFIG: Set [{key}] to [{value}]")
    return "<p>Updated config<p>"

@app.route("/m/<msg>")
def message(msg):
    return f"<p>Processing command: {msg}<p>"
