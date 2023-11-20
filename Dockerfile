FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Create and activate a virtual environment
RUN python -m venv venv

# Install packages in the virtual environment
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH environment variable
ENV PYTHONPATH /usr/src/app

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run migration scripts and then start the Uvicorn server
CMD . venv/bin/activate && python scripts/mongo_models_migrations.py && uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 8
