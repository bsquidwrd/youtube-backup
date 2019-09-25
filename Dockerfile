FROM python:3.7-alpine

# Comma delimited IDs
ENV FFMPEG_VERSION=3.0.2
ENV CHANNEL_IDS=comma,delimited,ids
ENV TIME_DELAY=60

RUN mkdir /code/
RUN mkdir /download/

WORKDIR /code/

ADD . /code/

RUN apk add ffmpeg
RUN python -m pip install -r requirements.txt

CMD ["python", "backup.py"]
