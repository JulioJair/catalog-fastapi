FROM python:3.9-slim

COPY ./app /catalog

WORKDIR /catalog

RUN pip install -r requirements.txt

EXPOSE 8080
EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "157.230.81.172", "--port", "80"]
# CMD ["python app.py"]
