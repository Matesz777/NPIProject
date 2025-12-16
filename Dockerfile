FROM python:3.13-slim AS builder

WORKDIR /build



COPY . .


FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /build /app

CMD ["python", "ruletkaDocker.py"]
