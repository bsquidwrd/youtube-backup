from __future__ import unicode_literals
import os
import time
import youtube_dl
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
log.addHandler(handler)


class MyLogger(object):
    def debug(self, msg):
        # log.debug(msg)
        pass

    def warning(self, msg):
        # log.warning(msg)
        pass

    def error(self, msg):
        log.error(msg)


def my_hook(d):
    if d['status'] == 'finished':
        log.info('Done downloading, now converting ...')


ydl_opts = {
    'merge_output_format': 'mkv',
    'writeinfojson': True,
    'writedescription': True,
    'writeannotations': True,
    'writethumbnail': True,
    'writesubtitles': True,
    'ignoreerrors': True,
    'restrictfilenames': True,
    'rejecttitle': '.*live.*',
    'outtmpl': '/download/%(uploader)s/%(upload_date)s_%(title)s_%(display_id)s.%(ext)s',
    'download_archive': '/download/downloaded.txt',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

# Default is bsquidwrd
channel_ids = os.getenv('CHANNEL_IDS', 'UCzgE8qqYb6GmlKqiI21cQmw').split(',')
RAW_TIME_DELAY = os.getenv('TIME_DELAY', '60')
TIME_DELAY = None

try:
    TIME_DELAY = int(RAW_TIME_DELAY)
except:
    TIME_DELAY = 60
    log.error(f"Could not parse TIME_DELAY to int, received {RAW_TIME_DELAY}. Setting 60 as default")

BASE_URL = 'https://www.youtube.com/channel/{channel_id}'
# Generate list to pass youtube-dl
channels = [BASE_URL.format(channel_id=i) for i in channel_ids]

log.info(f"Channels to download: {channel_ids}")
log.info(f"Time delay: {TIME_DELAY}")

while True:
    log.info("Starting download...")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(channels)
    log.info(f"Waiting {TIME_DELAY} seconds to run again")
    time.sleep(TIME_DELAY)
