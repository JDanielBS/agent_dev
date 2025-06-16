# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements if present
COPY requirements.txt ./

# Install dependencies if requirements.txt exists
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY src/ ./src/
COPY .env .env

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Default command (update as needed)
CMD ["python", "src/Filter.py"]