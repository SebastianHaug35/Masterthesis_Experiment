FROM python:3.12-slim

ARG UID=1000
ARG GID=1000

ENV TZ=Europe/Berlin \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && groupadd -g $GID app && useradd -m -u $UID -g $GID app

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.yaml .
COPY src/ src/
RUN mkdir -p input prompts runs results && chown -R app:app /app

USER app
CMD ["python", "-m", "src.run", "--help"]
