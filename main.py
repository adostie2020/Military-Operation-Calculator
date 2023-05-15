from duffel_api import Duffel
from flask import Flask

app = Flask(__name__, static_folder="fe/fe/build", static_url_path="")
client = Duffel(access_token = "duffel_test_wR7qOeLxoMTMziq7CGRJcKR6as2tvwQnuMoVVR0ESfj")

@app.route("/api/route1")
def main():
  # API code here
  return "Hello, World! This is a test"


# serve the react routes
@app.route("/", defaults={"path": ""})
def react(path):
  return app.send_static_file("index.html")


app.run(host="0.0.0.0", port=8000)
