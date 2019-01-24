FROM python:3.6-alpine3.7 AS runner
RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt


COPY main.py /app/
ADD s3statistics /app/s3statistics
ADD tests /app/tests
