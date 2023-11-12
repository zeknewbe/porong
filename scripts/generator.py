#!/usr/bin/python3

import requests
import os
import sys
import streamlink
import logging
from logging.handlers import RotatingFileHandler
import json

# Get the absolute path to the 'main' directory at the root
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../main'))

# Create the 'logs' directory under 'main' if it doesn't exist
log_directory = os.path.join(main_directory, 'logs')
os.makedirs(log_directory, exist_ok=True)

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_file = os.path.join(log_directory, "log.txt")
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

# ... (rest of your script)

if __name__ == "__main__":
    main()
