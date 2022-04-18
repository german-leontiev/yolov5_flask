FROM ultralytics/yolov5:latest-cpu

WORKDIR /user/src
COPY requirements.txt .
RUN pip --no-cache install -r requirements.txt

COPY app.py templates static test_weights .
CMD ["python3", "./app.py"]