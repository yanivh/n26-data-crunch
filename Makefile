.PHONY: build run clean test all local help

# Variables
DOCKER_IMAGE = n26-task
DOCKER_TAG = latest
PYTHON_CMD := $(shell command -v python3 || command -v python)

# Check if Docker is available
DOCKER_AVAILABLE := $(shell command -v docker 2> /dev/null)

# Clean generated files
clean:
	rm -f *.csv
	find . -type d -name "__pycache__" -exec rm -r {} +

# Build the Docker image if Docker is available
build:
ifdef DOCKER_AVAILABLE
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
else
	@echo "Docker is not installed. Using local Python environment."
endif

# Run the application in Docker if available, otherwise run locally
run:
ifdef DOCKER_AVAILABLE
	docker run --rm $(DOCKER_IMAGE):$(DOCKER_TAG)
else
	@echo "Docker is not installed. Running locally..."
	PYTHONPATH=. $(PYTHON_CMD) src/main.py
endif

# Run the application locally
local:
	PYTHONPATH=. $(PYTHON_CMD) src/main.py

# Run tests (placeholder for future tests)
test:
	@echo "No tests implemented yet"

# Default target
all: clean
ifdef DOCKER_AVAILABLE
	@make build
	@make run
else
	@make local
endif

# Help target
help:
	@echo "Available targets:"
	@echo "  all      - Clean and run the application (with Docker if available, otherwise locally)"
	@echo "  clean    - Remove generated files and cache"
	@echo "  build    - Build Docker image (if Docker is available)"
	@echo "  run      - Run application (with Docker if available, otherwise locally)"
	@echo "  local    - Run application locally (without Docker)"
	@echo "  test     - Run tests (not implemented yet)"
	@echo "  help     - Show this help message" 