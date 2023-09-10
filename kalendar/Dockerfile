FROM python:3.10

RUN mkdir /app
WORKDIR /app
EXPOSE 8085

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app.py /app/
COPY ./templates /app/
CMD ["/usr/local/bin/flask", "run", "-h", "0.0.0.0", "-p", "8085", "--debug"]
