FROM lambci/lambda:build-python3.7

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /app
COPY ./rmshelper ./rmshelper/
COPY handler.py .
WORKDIR /app

CMD ["python"]