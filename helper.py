import os
from flask import redirect, render_template, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
DETECTION_API_URL = 'http://your-backend-api-url/detect'
REMOVAL_API_URL = 'http://your-backend-api-url/remove'
RECIPE_API_URL = 'http://your-backend-api-url/find_recipe'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            return redirect(url_for('detect', filename=filename))

def detect_objects(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    files = {'file': open(filepath, 'rb')}
    response = requests.post(DETECTION_API_URL, files=files)
    if response.status_code == 200:
        # Assuming the response contains a list of detected ingredients
        ingredients = response.json()['ingredients']
        return render_template('list_ingredients.html', ingredients=ingredients)
    else:
        return "Error processing object detection"

def remove_unwanted():
    # Placeholder for removing unwanted ingredients using API
    # This is where you would call your backend API to remove unwanted ingredients
    response = requests.post(REMOVAL_API_URL, json={'unwanted': ['ingredient1', 'ingredient2']})
    if response.status_code == 200:
        # Assuming the response contains updated list of ingredients after removal
        ingredients = response.json()['ingredients']
        return render_template('list_ingredients.html', ingredients=ingredients)
    else:
        return "Error removing unwanted ingredients"


def find_recipe():
    # Placeholder for finding recipe based on ingredients list using API
    # This is where you would call your backend API to match ingredients with recipes
    response = requests.post(RECIPE_API_URL, json={'ingredients': ['ingredient1', 'ingredient2']})
    if response.status_code == 200:
        # Assuming the response contains matched recipe details
        recipe = response.json()['recipe']
        return render_template('show_recipe.html', recipe=recipe)
    else:
        return "Error finding recipe"
