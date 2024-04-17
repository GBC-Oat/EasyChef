import torch
from fastapi import FastAPI
from PIL import Image
import io
import pandas as pd

model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/yolov5s_results/weights/best.pt', force_reload=True)

def predict_objects(image: Image.Image):
    # Perform inference
    results = model(image)
    
    # Show results
    results.show()
    # Extract detected labels
    detected_objects = results.pred[0]
    labels = [model.names[int(obj[5])] for obj in detected_objects]
    unique_labels = list(set(labels))
    print(unique_labels)
    return unique_labels



def search_recipe(ingredients):
    # Search recipe based on ingredients
    df_food = pd.read_csv('food_recipe.csv')
    
    df_recipe = df_food[df_food['Ingredients'].str.contains('|'.join(ingredients))]
        

    recipes = []
    for _, row in df_recipe.head(5).iterrows():
        recipe_info = {
            "name": row['Title'],
            "ingredients": row['Ingredients'].replace("'", "").replace("[", "").replace("]", "").split(', '),  # Assuming ingredients are comma-separated
            "instructions": row['Instructions']
        }
        recipes.append(recipe_info)

    return recipes


# predict_objects('test_images/fruits-and-vegetable-rack-section.jpg')
