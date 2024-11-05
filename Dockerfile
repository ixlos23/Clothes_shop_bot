# Base image with Python 3.12
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Copy the necessary project files (pyproject.toml and poetry.lock)
COPY pyproject.toml poetry.lock* /app/

# Install dependencies using poetry
RUN poetry install --no-dev

# Copy the rest of the application code
COPY . .

# Command to run your application
CMD ["python3", "main.py"]
