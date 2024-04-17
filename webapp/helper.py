from io import BytesIO
from PIL import Image
from pillow_heif import read_heif
import logging
from flask import render_template, request, jsonify, session
import requests

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heif', 'heic'}
INGREDIENTS_DETECTION_API_URL = 'http://138.197.140.119:8000/detect_ingredients/'
RECIPE_API_URL = 'http://138.197.140.119:8000/find_recipe/'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_objects():
    if 'image' not in request.files:
        return jsonify({"error": "No image part"}), 400
    
    uploaded_file = request.files['image']
    selected_model = request.form['model'] # Retrieve the selected model

    if uploaded_file.filename == '':
        return "No selected file", 400

    if uploaded_file and allowed_file(uploaded_file.filename):

        image_stream = BytesIO(uploaded_file.read())

        if uploaded_file.filename.lower().endswith(('.heic', '.heif')):
            # Decode the HEIC image
            heic_image = read_heif(image_stream)
            
            # Convert the HEIC image to a PIL Image
            img = Image.frombytes(
                heic_image.mode,
                heic_image.size,
                heic_image.data,
                "raw",
                heic_image.mode,
                heic_image.stride,
            )
        else:
            # Otherwise, assume it's already in JPEG or PNG format
            img = Image.open(image_stream)

        # Convert image to bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')

        # Create files dictionary
        files = {'image': (uploaded_file.filename, img_bytes.getvalue())}
        data = {'model': selected_model} 

        logger.info(f"Sending request to {INGREDIENTS_DETECTION_API_URL} with image: {uploaded_file.filename} and model: {selected_model}")
        response = requests.post(INGREDIENTS_DETECTION_API_URL, files=files, data=data)

        if response.status_code == 200:
            detected_ingredients = response.json().get('detected_ingredients', [])
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
    if not detected_ingredients:
        return render_template('index.html', message="Please detect ingredients first.")
    
    logger.info(f"Sending request to {RECIPE_API_URL} with ingredients: {detected_ingredients}")
    response = requests.post(RECIPE_API_URL, json={'ingredients': detected_ingredients})

    if response.status_code == 200:
        suggested_recipes = response.json().get('recipe', [])
        logger.info(f"Received response: {response.status_code}, Suggested recipes: {suggested_recipes}")
        if not suggested_recipes:
            return "No recipe matched the detected ingredients. Please try again."

        return render_template('result_recipe.html', suggested_recipes=suggested_recipes)
    else:
        logger.error(f"Error finding recipe. Status code: {response.status_code}")
        return "Error finding recipe"