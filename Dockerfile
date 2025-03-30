FROM python:3.12-slim


# Установить зависимости Python
WORKDIR /app

RUN apt-get update \\
  && apt-get install -y gcc libpg-dev \\
  && apt-get clean \\
  && rm -rf /var/lib/apt/lists/\*

COPY /requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

# Скопировать исходный код
COPY . .

EXPOSE 8000

CMD ("sh", "-c","python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000")
