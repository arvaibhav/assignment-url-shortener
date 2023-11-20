FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN python -m venv venv
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH environment variable
ENV PYTHONPATH /usr/src/app

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["./venv/bin/python", "src/main.py"]
