FROM python:3.11-alpine

WORKDIR /app

COPY topic_creator.py topics.json ./

RUN pip install kafka-python

CMD ["python", "topic_creator.py"]
