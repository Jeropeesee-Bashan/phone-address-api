FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml .
COPY ./src ./src

RUN pip install --upgrade pip && \
    pip install --no-cache-dir uvicorn && \
    pip install --no-cache-dir .

EXPOSE 80

CMD ["uvicorn", "phoneaddress:app", "--host", "0.0.0.0", "--port", "80"]
