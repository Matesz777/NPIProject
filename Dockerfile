FROM python:3.13-slim

WORKDIR /app
COPY . /app

CMD ["python", "ruletkaDocker.py"]
