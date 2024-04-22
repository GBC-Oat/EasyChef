# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install --upgrade pip

RUN pip install python-multipart

RUN pip install requests

RUN pip install --upgrade numpy typing



# 
COPY ./app /code/app

RUN ls app/yolov5/runs/train/yolov5s_results/weights/best.pt

#
COPY ./app/test_yolov5_model.py /code/app/test_yolov5_model.py

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]