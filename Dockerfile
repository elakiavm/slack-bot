FROM python:3.8-slim-buster

EXPOSE 9000

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

WORKDIR /app

COPY . /app

CMD ["python","app.py"]