FROM python:3.12-slim-bookworm

RUN apt update \
	&& apt install -y --no-install-recommends \
		postgresql-client libpq-dev python3-dev gcc

WORKDIR /usr/src/treescope_core

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN apt autopurge -y libpq-dev python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_ENV=production
ENV DATABASE_URI=postgresql://postgres:postgres@localhost:5432/treescope

COPY . .

EXPOSE 5000

CMD ["flask", "run"]
