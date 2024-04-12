from flask import Flask, render_template, request, redirect, url_for
from helper import upload_file, detect_objects, remove_unwanted, find_recipe

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    return upload_file(request)

@app.route('/detect_objects/<filename>')
def detect(filename):
    return detect_objects(filename)

@app.route('/remove_unwanted', methods=['POST'])
def remove():
    return remove_unwanted()

@app.route('/find_recipe', methods=['POST'])
def find():
    return find_recipe()

if __name__ == '__main__':
    app.run(debug=True)
