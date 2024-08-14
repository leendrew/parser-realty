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
ARG APP_ENV
COPY --from=builder /app/.env.${APP_ENV} ./.env
COPY --from=builder /app/src ./src
CMD ["python3", "-m", "src.main"]

# CMD ["uvicorn", "src.main:app", "--host", "${APP_HOST}", "--port", "${APP_PORT}"]