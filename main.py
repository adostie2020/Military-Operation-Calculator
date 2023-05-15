import json
import request
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def main():
  return 'Hello, World!'

app.run(host='0.0.0.0', port=8080)