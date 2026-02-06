FROM python:3.11-slim

WORKDIR /app

# Ensure system has minimal tooling for builds (if any become necessary later).
RUN python -m pip install --upgrade pip

# Copy project metadata first to leverage Docker layer caching.
COPY pyproject.toml README.md /app/

# Install project (currently metadata-only) and test tooling.
RUN pip install -e . && pip install pytest

# Copy the rest of the repository into the image.
COPY . /app

# Default command: run the test suite. Tests are expected to fail initially
# because implementations for the specified contracts do not yet exist.
CMD ["pytest", "-q"]

