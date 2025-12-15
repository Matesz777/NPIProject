FROM python:3.13-slim AS builder

WORKDIR /build

COPY . .


FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /build /app

CMD ["python", "ruletkaDocker.py"]
