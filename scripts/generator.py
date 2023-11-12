#!/usr/bin/python3

# ... [rest of your imports] ...

# ... [logger setup] ...

# Constants
BANNER = '''
Your Banner Here
'''
VALID_URL_SUFFIXES = ('.m3u', '.m3u8', '.ts')

# ... [rest of your functions] ...

def grab(url):
    # Check for both http and https URLs with valid streaming suffixes
    if url.startswith(('http://', 'https://')) and url.endswith(VALID_URL_SUFFIXES):
        logger.debug("URL ends with a valid streaming suffix and has a correct protocol: %s", url)
        if check_url(url):
            return url
        else:
            logger.error("URL is not reachable or did not pass validation: %s", url)
            return None
    else:
        logger.error("URL does not have a correct protocol or valid streaming suffix: %s", url)
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

# ... [rest of your functions] ...

def main():
    print(BANNER)

    # Assuming channel_info.txt is at the root of your repository
    channel_info_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../channel_info.txt'))
    channel_data = process_channel_info(channel_info_path)

    # ... [rest of your main function] ...

if __name__ == "__main__":
    main()
