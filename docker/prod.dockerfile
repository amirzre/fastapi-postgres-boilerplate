# Stage 1: Build the dependencies layer
FROM python:3.11-slim AS builder

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

# Install the production dependencies into a virtual environment
RUN poetry install --no-dev --no-root --no-interaction --no-ansi

# Stage 2: Create the final runtime image
FROM python:3.11-slim AS final

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /root/.local /root/.local
ENV PATH="/root/.local/bin:$PATH"

# Copy the entire application code
COPY . .

# Expose the application port
EXPOSE 8000
