FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml .
COPY ./phoneaddress ./phoneaddress

RUN pip install --upgrade pip && pip install --no-cache-dir .

EXPOSE 80

CMD ["phoneaddress"]
