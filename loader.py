from flask import Flask
import I9000
import re

MARKER = "~`~"
MSG_RE = f"(?:^|{MARKER})(?:{MARKER})(.*)(?:{MARKER})(?:{MARKER}|$)" #Only matches one so far

app = Flask(__name__)
config = {
    "ip": "",
    "port": 0,
    "print_to_console": False,
    "send_to_printer": True,
}

def cprint(msg):
    if config["print_to_console"]:
        print(msg)

@app.route("/")
def r_home():
    return f"<p>Home<br>{config}</p>"

@app.route("/config/<key>/<value>")
def r_config(key, value):
    # Try to convert value to correct boolean
    if value == "True":
        config[key] = True
    elif value == "False":
        config[key] = False
    else:
        # Try to convert value to int
        try:
            i = int(value)
            config[key] = i
        except ValueError:
            config[key] = value
    cprint(f"CONFIG: Set [{key}] to [{value}]")
    return "<p>Updated config<p>"

@app.route("/m/<msg>")
def message(msg):
    cprint(f"PARSING MESSAGE: {msg}")
    out = ""
    messages = re.findall(MSG_RE, msg)
    if len(messages) == 0:
        cprint("ERROR PARSING MESSAGE")
        return f"<p>Error parsing message: {msg}<p>"
    return f"<p>{messages}<p>"
