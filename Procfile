web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile -


release: python manage.py collectstatic --noinput
web: gunicorn config.wsgi --log-file -
