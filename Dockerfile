# Chemesty Docker Container
# Provides a reproducible environment for the Chemesty chemistry library

FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libffi-dev \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==$POETRY_VERSION

# Create app directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock poetry.toml ./

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root \
    && rm -rf $POETRY_CACHE_DIR

# Copy application code
COPY . .

# Install the package
RUN poetry install --no-dev

# Create non-root user
RUN useradd --create-home --shell /bin/bash chemesty
RUN chown -R chemesty:chemesty /app
USER chemesty

# Set up data directory.
RUN mkdir -p /app/data


# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import chemesty; print('Chemesty is healthy')" || exit 1

# Default command
CMD ["python", "-c", "import chemesty; print('Chemesty container is ready!')"]

# Labels for metadata
LABEL maintainer="Chemesty Team" \
      version="1.0.0" \
      description="Chemesty chemistry library container" \
      org.opencontainers.image.title="Chemesty" \
      org.opencontainers.image.description="A comprehensive chemistry package for working with elements, molecules, and chemical datasets" \
      org.opencontainers.image.licenses="MIT"