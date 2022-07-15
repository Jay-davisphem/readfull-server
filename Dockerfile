FROM python:latest

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
