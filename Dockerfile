FROM --platform=linux/arm64 python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY .. .
ENV PYTHONPATH=/app/kefir_test

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]