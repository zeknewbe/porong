#!/usr/bin/python3

import requests
import os
import streamlink
import logging
from logging.handlers import RotatingFileHandler
import json

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_file = "log.txt"
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*5, backupCount=2)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Constants
BANNER = '''
Your Banner Here
'''
VALID_URL_SUFFIXES = ('.m3u', '.m3u8', '.ts')

def grab(url):
    # Directly return the URL if it has a valid suffix
    if url.endswith(VALID_URL_SUFFIXES):
        logger.debug(f"URL with valid suffix: {url}")
        return url

    # Use streamlink to grab the actual URL for streams
    try:
        session = streamlink.Streamlink()
        streams = session.streams(url)
        logger.debug(f"URL Streams {url}: {streams}")
        if "best" in streams:
            return streams["best"].url
    except Exception as e:
        logger.error(f"Streamlink error for URL {url}: {e}")
    return None

def check_url(url):
    # Stream the request to avoid downloading content
    try:
        with requests.get(url, timeout=15, stream=True) as response:
            response.raise_for_status()  # Raise an error for bad status codes
            logger.debug(f"URL is reachable: {url}")
            return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error checking URL {url}: {e}")
    return False

def process_channel_info(channel_info_path):
    channel_data = []

    with open(channel_info_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('http') or line.startswith('https'):
                if check_url(line):
                    channel_data.append(line)
                else:
                    logger.warning(f"URL check failed: {line}")
            else:
                logger.error(f"Invalid URL format: {line}")

    return channel_data

def main():
    print(BANNER)

    channel_info_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'channel_info.txt'))
    channel_data = process_channel_info(channel_info_path)

    # Generate M3U playlist
    playlist_data = ['#EXTM3U'] + channel_data

    # Debug: Print playlist data before writing to the file
    for line in playlist_data:
        print(line)

    try:
        with open("playlist.m3u", "w") as f:
            f.write('\n'.join(playlist_data))
        logger.info("Playlist has been written to playlist.m3u")
    except Exception as e:
        logger.error(f"Error writing to playlist.m3u: {e}")

if __name__ == "__main__":
    main()
