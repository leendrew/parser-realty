FROM python:3.9-slim AS builder
WORKDIR /app
COPY ./requirements.txt ./
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt
COPY . .

FROM builder AS runner
WORKDIR /app
ARG BUILD_ENV
COPY --from=builder /app/.env.${BUILD_ENV} ./.env
COPY --from=builder /app/src ./src
CMD ["python3", "./src/main.py"]

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]