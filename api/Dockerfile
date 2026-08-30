FROM python:3.13-slim

WORKDIR /app

# copy only requirements first — this layer gets cached and skipped
# on rebuilds unless requirements.txt actually changes, speeding up iteration
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# now copy the actual application code
COPY core ./core
COPY api ./api

# data/ is where the SQLite file lives — created here so the volume
# mount point exists even before the app writes to it
RUN mkdir -p /app/data

ENV DB_PATH=/app/data/stock.db

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]