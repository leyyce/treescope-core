FROM python:3.12-slim-bookworm

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8080

CMD ["flask", "run", "--debug"]
