.PHONY: all clean test generate validate feature-table docker-build docker-run docker-test docker-all setup venv

# Variables
DOCKER_IMAGE = n26-task
DOCKER_TAG = latest
PYTHON := $(shell command -v python3.9 2>/dev/null || command -v python3.10 2>/dev/null || command -v python3.11 2>/dev/null)
VENV := .venv
VENV_BIN := $(VENV)/bin
VENV_PYTHON := $(VENV_BIN)/python
VENV_PIP := $(VENV_PYTHON) -m pip
DATA_DIR := data

# Check if Python is available
ifeq ($(PYTHON),)
$(error "Python not found. Please install Python 3.9 or later")
endif

# Check if Docker is available
DOCKER_AVAILABLE := $(shell command -v docker 2> /dev/null)

# Create Python virtual environment with specific version
venv:
	@echo "Creating virtual environment..."
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@$(VENV_PIP) install --upgrade pip setuptools wheel

# Setup Python environment and install dependencies with better error handling
setup: venv
	@echo "Installing dependencies..."
	@$(VENV_PYTHON) -c "import sys; assert sys.version_info >= (3,9) and sys.version_info < (3,12), 'Python 3.9-3.11 required'" || \
		(echo "Error: Python 3.9-3.11 required. Current: $$($(VENV_PYTHON) --version)" && exit 1)
	@$(VENV_PIP) install --no-cache-dir -r requirements.txt

# Clean generated files
clean:
	@echo "Cleaning up..."
	rm -rf $(DATA_DIR)
	mkdir -p $(DATA_DIR)

# Generate data
generate:
	@echo "Generating data..."
	@$(VENV_PYTHON) src/main.py

# Validate data
validate:
	@echo "Validating data..."
	# Add your validation commands here

# Feature table test (now uses venv)
feature-table: setup
	@echo "Testing feature table queries..."
	@PYTHONPATH=. $(VENV_PYTHON) src/feature_table_test.py

# Docker commands
docker-build:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Error: Docker is not installed. Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"; \
		exit 1; \
	fi
	@echo "Attempting to build Docker image..."
	@docker pull python:3.9.18-slim && \
	docker build --no-cache -t $(DOCKER_IMAGE):$(DOCKER_TAG) . || \
	(echo "First attempt failed, trying without credentials..." && \
	docker logout && \
	docker build --no-cache --pull -t $(DOCKER_IMAGE):$(DOCKER_TAG) .)

docker-run:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Error: Docker is not installed. Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"; \
		echo "Or use: brew install --cask docker"; \
		exit 1; \
	fi
	docker run --rm -v $(PWD)/data:/app/data $(DOCKER_IMAGE):$(DOCKER_TAG)

docker-test:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Error: Docker is not installed. Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"; \
		exit 1; \
	fi
	docker run --rm -e PYTHONUNBUFFERED=1 $(DOCKER_IMAGE):$(DOCKER_TAG)

# Default target
all: setup clean generate validate feature-table

# Run everything in Docker
docker-all: docker-build docker-run docker-test

# Clean everything including virtual environment
distclean: clean
	@echo "Removing virtual environment..."
	rm -rf $(VENV)

# Help target
help:
	@echo "Available targets:"
	@echo "  all           - Clean, generate, validate and test"
	@echo "  setup         - Create venv and install dependencies"
	@echo "  venv          - Create Python virtual environment"
	@echo "  clean         - Remove generated files"
	@echo "  distclean     - Remove generated files and virtual environment"
	@echo "  generate      - Generate test data"
	@echo "  validate      - Validate data"
	@echo "  feature-table - Run feature table tests"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-run    - Run in Docker"
	@echo "  docker-test   - Run tests in Docker"
	@echo "  docker-all    - Run everything in Docker"
	@echo "  dimension-test - Run dimension deduplication test"

# Add new target
dimension-test: setup
	@echo "Testing dimension deduplication..."
	@PYTHONPATH=. $(VENV_PYTHON) src/dimension_deduplication_test.py

docker-dimension-test:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Error: Docker is not installed. Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"; \
		exit 1; \
	fi
	@echo "Running dimension deduplication tests in Docker..."
	docker run --rm -v $(PWD):/app/data $(DOCKER_IMAGE):$(DOCKER_TAG) src/dimension_deduplication_test.py

# Add new target
join-test: setup
	@echo "Testing dataset joining..."
	@PYTHONPATH=. $(VENV_PYTHON) src/join_datasets_test.py

docker-join-run:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Error: Docker is not installed. Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"; \
		exit 1; \
	fi
	@echo "Running join datasets program..."
	@mkdir -p data
	docker run --rm -v $(PWD):/app/data $(DOCKER_IMAGE):$(DOCKER_TAG) src/main.py
	@sleep 1  # Give filesystem time to sync
	docker run --rm -v $(PWD):/app/data $(DOCKER_IMAGE):$(DOCKER_TAG) src/join_datasets.py

docker-join-test:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Error: Docker is not installed. Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"; \
		exit 1; \
	fi
	@echo "Running join datasets tests..."
	@mkdir -p data
	@rm -f *.csv data/*.csv  # Clean existing data files
	docker run --rm -v $(PWD):/app/data $(DOCKER_IMAGE):$(DOCKER_TAG) src/main.py
	@sleep 1  # Give filesystem time to sync
	docker run --rm -v $(PWD):/app/data $(DOCKER_IMAGE):$(DOCKER_TAG) src/join_datasets_test.py

# Add Docker-specific test targets
docker-feature-table:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Error: Docker is not installed. Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"; \
		exit 1; \
	fi
	@echo "Running feature table tests in Docker..."
	docker run --rm -v $(PWD):/app/data $(DOCKER_IMAGE):$(DOCKER_TAG) src/feature_table_test.py 