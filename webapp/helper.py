import logging
from flask import render_template, request, jsonify, session
import requests

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
INGREDIENTS_DETECTION_API_URL = 'http://138.197.140.119:8000/detect/'
RECIPE_API_URL = 'http://138.197.140.119:8000/find_recipe/'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEMP = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_objects():
    if 'image' not in request.files:
        return jsonify({"error": "No image part"}), 400
    
    uploaded_file = request.files['image']

    if uploaded_file and allowed_file(uploaded_file.filename):
        files = {'image': (uploaded_file.filename, uploaded_file.read())}
        logger.info(f"Sending request to {INGREDIENTS_DETECTION_API_URL} with files: {files}")
        response = requests.post(INGREDIENTS_DETECTION_API_URL, files=files)

        if response.status_code == 200:
            detected_ingredients = response.json().get('detected_labels', [])
            session['detected_ingredients'] = detected_ingredients
            logger.info(f"Received response: {response.json()}")
            return render_template('list_ingredients.html', detected_ingredients=detected_ingredients)
        else:
            logger.error(f"Error processing object detection. Status code: {response.status_code}")
            return "Error processing object detection", response.status_code
    else:
        logger.error("Invalid file format")
        return "Invalid file format", 400


def find_recipe():
    detected_ingredients = session.get('detected_ingredients', [])
    logger.info(f"Sending request to {RECIPE_API_URL} with ingredients: {detected_ingredients}")

    response = requests.post(RECIPE_API_URL, json={'ingredients': detected_ingredients})

    if response.status_code == 200:
        suggested_recipes = response.json().get('recipe', [])
        logger.info(f"Received response: {response.status_code}, Suggested recipes: {suggested_recipes}")
        return render_template('result_recipe.html', suggested_recipes=suggested_recipes)
    else:
        logger.error(f"Error finding recipe. Status code: {response.status_code}")
        return "Error finding recipe"