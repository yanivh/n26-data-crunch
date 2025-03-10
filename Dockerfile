# Use Python 3.9.18 slim image (specific version)
FROM python:3.9.18-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p src/queries/feature_table

# Copy all source code and config files
COPY src/ ./src/
COPY Makefile .

# Create data directory
RUN mkdir -p data

# Set Python as entrypoint
ENTRYPOINT ["python"]
CMD ["src/join_datasets.py"] 