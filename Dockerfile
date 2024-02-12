FROM python:3.11.6-alpine3.18 AS build
WORKDIR /app

COPY requirements.txt .
RUN apk add --update libffi-dev openssl-dev build-base \
  && python3 -m venv ./venv \
  && . ./venv/bin/activate \
  && pip install --no-cache-dir gunicorn \
  && pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.11.6-alpine3.18 AS final
ARG UID=1001
ARG GID=1001
ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONUNBUFFERED=TRUE

WORKDIR /app

RUN addgroup --gid $GID nonroot \
  && adduser --uid $UID -G nonroot -D -H --gecos "" nonroot
COPY --from=build --chown=nonroot:nonroot /app /app

USER nonroot
EXPOSE 5000
CMD ["gunicorn" , "-w", "3", "--bind", "0.0.0.0:5000", "wsgi:flask_app"]
