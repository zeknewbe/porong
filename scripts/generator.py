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
    if url.endswith(VALID_URL_SUFFIXES):
        logger.debug("URL ends with a valid streaming suffix: %s", url)
        if check_url(url):
            return url
        else:
            logger.error("Valid streaming URL is not reachable: %s", url)
            return None

    try:
        session = streamlink.Streamlink()
        streams = session.streams(url)
        logger.debug("URL Streams %s: %s", url, streams)
        if "best" in streams:
            return streams["best"].url
        return None
    except streamlink.exceptions.NoPluginError as err:
        logger.error("URL Error No PluginError %s: %s", url, err)
        return url
    except streamlink.StreamlinkError as err:
        logger.error("URL Error %s: %s", url, err)
        return None


def check_url(url):
    try:
        response = requests.get(url, timeout=15, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes
        logger.debug(f"URL is reachable: {url}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error checking URL {url}: {e}")
    return False


def process_channel_info(channel_info_path):
    channel_data = []

    try:
        with open(channel_info_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if not line.startswith('http') and not line.startswith('https'):
                    logger.error(f"Invalid URL format: {line}")
                    continue
                link = grab(line)
                if link:
                    channel_data.append({'url': link})
                else:
                    logger.warning(f"Unreachable or unsupported URL: {line}")
    except Exception as e:
        logger.error(f"Error processing channel info: {e}")

    return channel_data


def main():
    print(BANNER)

    channel_info_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'channel_info.txt'))
    channel_data = process_channel_info(channel_info_path)

    # Generate M3U playlist
    playlist_data = ['#EXTM3U']
    
    for item in channel_data:
        if 'url' in item:
            playlist_data.append(item['url'])

    try:
        with open("playlist.m3u", "w") as f:
            f.write('\n'.join(playlist_data))
    except Exception as e:
        logger.error(f"Error writing to playlist.m3u: {e}")


if __name__ == "__main__":
    main()
