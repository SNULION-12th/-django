ARG PYTHON_VERSION=3.10-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

ENV SECRET_KEY "7oVUQeuXwdifK7uaHrfILTcJ4HPGyf6AiEPHTLiuSBnEj1vXn4"
RUN python manage.py collectstatic --noinput

EXPOSE 8000

RUN python manage.py collectstatic --noinput && \
    python manage.py migrate

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "seminar.wsgi"]
