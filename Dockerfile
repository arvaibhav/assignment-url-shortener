FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH /app

EXPOSE 8000
# Run migration scripts and then start the Uvicorn server
CMD python scripts/mongo_models_migrations.py && uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 8
