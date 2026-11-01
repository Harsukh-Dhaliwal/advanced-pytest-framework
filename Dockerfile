# Use the official Microsoft Playwright image with Python pre-installed
FROM ://microsoft.com

# Set clean environment configurations for container execution
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PLAYWRIGHT_HEADLESS=true

# Establish the workspace directory inside the container
WORKDIR /app

# Copy dependency manifests first to leverage Docker layer caching
COPY requirements.txt .

# Upgrade package management tools and install python frameworks
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the remaining framework architecture into the workspace
COPY . .

# Default command to kick off headless multi-worker tests using production configs
CMD ["pytest", "-n", "auto", "--env=prod", "--html=report.html", "--self-contained-html"]