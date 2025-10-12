
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download the spaCy model
RUN python -m spacy download en_core_web_sm

# Expose the port if the application were to run a web server (not applicable for current CLI)
# EXPOSE 5000

# Define environment variable for non-interactive spaCy download
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Command to run the application
# For passive monitoring (file watcher), use: python main.py 1
# For interactive menu, run: python main.py
CMD ["python", "main.py"]
