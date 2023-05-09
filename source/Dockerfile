# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the project's source code into the container
COPY . /app/

# Download the pre-trained ResNet and YOLO weights
RUN mkdir -p /app/object_classification/weights && \
    mkdir -p /app/object_detection/weights

COPY object_classification/weights/resnet50_food.pt /app/object_classification/weights/
COPY object_detection/weights/model_200.pt /app/object_detection/weights/

# Expose port 8000 for the Django app to run on
EXPOSE 8000

# Run the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "price_calculator.wsgi:application"]
