FROM python:3.10

WORKDIR /app

RUN mkdir res

COPY . /app/

ENV RESOURCES_DIR "./res"

CMD ["python3", "UI.py"]
