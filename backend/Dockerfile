FROM python:3.9-slim

COPY ./app /catalog

WORKDIR /catalog

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app"]
# CMD ["python app.py"]
