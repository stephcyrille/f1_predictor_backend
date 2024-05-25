# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /f1_predictor_api

# Copy the current directory contents into the container at /app
COPY . /f1_predictor_api

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

WORKDIR /f1_predictor_api/f1_predictor_api

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=f1_predictor_api.settings
ENV PYTHONUNBUFFERED=1

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
