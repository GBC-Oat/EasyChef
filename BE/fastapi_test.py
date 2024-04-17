from typing import Union
from PIL import Image
from fastapi import FastAPI, UploadFile, File
# from pydantic import BaseModel
from test_yolov5_model import predict_objects, search_recipe
import io
from typing import Dict, List


app = FastAPI()


# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/detect_ingredients/")
async def detect_objects(image: UploadFile = File(...)):
    # Read image file
    contents = await image.read()
    img = Image.open(io.BytesIO(contents))
    # Predict objects
    labels = predict_objects(img) 
    
    # recipe = search_recipe(labels)
    
    return {"detected_ingredients": labels}



@app.post("/find_recipe/")
async def search_recipe_api(data: Dict[str, List[str]]):
    ingredients = data.get("ingredients", [])
    
    # Search for recipe
    recipe = search_recipe(ingredients)
    
    return {"recipe": recipe}
