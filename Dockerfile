FROM python:latest

COPY . /app
WORKDIR /app
RUN pip install -r dev.txt
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["src/app.py"]
