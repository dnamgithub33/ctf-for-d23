
FROM python:3.9-slim

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=5000


RUN adduser --disabled-password --gecos "" user
USER user

COPY . .

CMD ["flask", "run"]