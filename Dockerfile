# Use the official Python image as a base
FROM python:3.8.10

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
