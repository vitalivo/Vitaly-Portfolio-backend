FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings.development

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/development.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p logs staticfiles media

# ✅ Создаем миграции и собираем статику
RUN python manage.py makemigrations --settings=config.settings.development || true
RUN python manage.py migrate --settings=config.settings.development || true
RUN python manage.py collectstatic --noinput --settings=config.settings.development

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Run development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=config.settings.development"]
