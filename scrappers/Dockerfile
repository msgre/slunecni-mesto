FROM python:3.10

RUN mkdir /app
WORKDIR /app/mesto

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/
