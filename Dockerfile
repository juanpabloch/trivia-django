# Pull base image
FROM python:3.8.1-slim-buster

RUN useradd trivia


# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app


RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    gettext \
 && rm -rf /var/lib/apt/lists/*


RUN pip install "gunicorn==20.0.4"

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# CMD set -xe; python manage.py migrate --noinput; gunicorn cxawards.wsgi:application