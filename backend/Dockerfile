FROM python:3.7

RUN pip install -r app/requirements.txt

EXPOSE 80

COPY ./app /app

WORKDIR /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
