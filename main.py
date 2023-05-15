from flask import Flask

app = Flask(__name__, static_folder="fe/fe/build", static_url_path="")


@app.route("/api/route1")
def main():
  # API code here
  return "Hello, World! This is a test"


# serve the react routes
@app.route("/", defaults={"path": ""})
def react(path):
  return app.send_static_file("index.html")


app.run(host="0.0.0.0", port=8000)
