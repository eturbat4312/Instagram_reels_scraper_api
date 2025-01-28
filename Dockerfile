# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add the root directory to PYTHONPATH
ENV PYTHONPATH=/app

# Copy the application files
COPY ./backend /app/backend

# Expose port for Flask
EXPOSE 5000

# Set default command to run the Flask app
# CMD ["python", "-m", "backend/app/api.py"]
CMD ["python", "-m", "backend.app.api"]

