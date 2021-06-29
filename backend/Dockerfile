FROM python:3.9-slim

COPY ./app /catalog

WORKDIR /catalog

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["python app.py"]
