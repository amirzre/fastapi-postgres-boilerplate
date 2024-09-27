# Use the official Python image as a base
FROM python:3.11-slim AS base

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.2

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry self add poetry-plugin-export

# Copy only the dependency files to leverage caching
COPY pyproject.toml poetry.lock ./

# Install dependencies in the virtual environment managed by Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the entire application code
COPY . .

# Expose the application port
EXPOSE 8000

# Command to run the application with hot-reloading
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
