# Dockerfile

# Use a lightweight Python image
FROM python:3.9-slim

# Create a working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port where Flask will run (if needed)
EXPOSE 5000

# The default command can be overridden by Docker Compose
CMD ["python", "app.py"]
