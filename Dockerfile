# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy source code
COPY src/ /app/src/

# Set Python path to include src directory
ENV PYTHONPATH=/app

# Set the default command
CMD ["python", "src/main.py"] 