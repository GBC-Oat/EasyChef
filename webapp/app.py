from flask import Flask, render_template
from helper import detect_objects, find_recipe
from os import environ
import secrets

app = Flask(__name__)

app.secret_key = environ.get('SECRET_KEY') or secrets.token_hex(16)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect_ingredients', methods=['POST'])
def detect_ingredients():
    return detect_objects()

@app.route('/find_recipe', methods=['POST'])
def find():
    return find_recipe()

if __name__ == '__main__':
    app.run(debug=True)
