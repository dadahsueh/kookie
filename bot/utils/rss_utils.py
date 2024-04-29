﻿import asyncio
import hashlib
import logging
import re
import time
from datetime import datetime, timedelta

import feedparser
import html2text
import ping3

logger = logging.getLogger(__name__)


class RssUtils(object):
    @staticmethod
    async def is_host_reachable(host):
        try:
            host = host.split('//')[1].split('/')[0]
            # Perform ICMP ping to check host reachability
            if ping3.ping(host, timeout=2) is not None:
                return True
        except Exception as e:
            raise ValueError(f"Failed to ping {host} {e}")
        return False

    @staticmethod
    def color_code_from_string(string_text):
        color_code = '#4169E1'
        try:
            hash_value = hashlib.md5(string_text.encode()).hexdigest()
            # Extract RGB components from the hash value
            red = int(hash_value[0:2], 16)   # Use first two characters as red component
            green = int(hash_value[2:4], 16) # Use next two characters as green component
            blue = int(hash_value[4:6], 16)  # Use last two characters as blue component

            # Format as hex color code (#RRGGBB)
            color_code = f'#{red:02x}{green:02x}{blue:02x}'
        except Exception as e:
            logger.error(e)
        return color_code

    @staticmethod
    async def parse_feed_with_retry(url, max_retries=3, retry_delay=1):
        for attempt in range(max_retries):
            try:
                feed = feedparser.parse(url)

                if feed is None or len(feed.entries) == 0:
                    raise ValueError(f"feed is None or len(feed.entries) == 0 for {url}")

                return feed
            except Exception as e:
                logger.info(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)

        raise ValueError(f"All retries failed to parse {url}")

    @staticmethod
    def extract_url(raw_url):
        try:
            url_pattern = r'(https?:\/\/[^\s()\[\]]+)'
            match = re.search(url_pattern, raw_url)
            if match is None:
                raise ValueError(f"could not parse url from > {raw_url}")
            url = match.group(1)
            return url
        except Exception as e:
            logger.error(f"Failed extract url from {raw_url}. {e}")
            raise

    @staticmethod
    def string_truncate(string, max_length):
        if len(string) > max_length:
            return string[:max_length] + '…'
        else:
            return string

    @staticmethod
    def parse_feed_title(feed, max_length=42):
        if 'feed' not in feed:
            return ''
        feed_title = feed.feed.get('title', '')
        return RssUtils.string_truncate(feed_title, max_length)

    @staticmethod
    def parse_title(entry: dict, max_length=64):
        raw_title = entry.get('plaintitle', entry.get('title', ''))
        pattern = r'\/[^\/]*\/|\[[^\]]*\]'
        title = re.sub(pattern, '', raw_title)
        title.strip()
        return RssUtils.string_truncate(title, max_length)

    @staticmethod
    def parse_date(entry: dict):
        if 'published_parsed' not in entry:
            return ''
        beijing_utc_timedelta = timedelta(hours=8)
        entry_date = datetime.utcfromtimestamp(time.mktime(entry['published_parsed'])) + beijing_utc_timedelta
        date_format = "%Y-%m-%d %H:%M:%S"

        date = entry_date.strftime(date_format)
        return date

    @staticmethod
    def parse_link(entry: dict):
        if 'link' not in entry:
            return ''
        link = entry['link']
        return link

    @staticmethod
    def parse_image(entry: dict):
        image = ''
        if 'media_thumbnail' in entry:
            r = re.search(r'(https?://\S+?\.(?:jpg|gif|png))', str(entry['media_thumbnail']))
            image = r.group(1) if r else ''

        if len(image) != 0:
            return image

        if 'content' in entry and len(entry['content']) > 0:
            r = re.search(r'(?:<img[^>]*src="([^"]+)"[^>]*\/?>)', entry['content'][0].value)
            image = r.group(1) if r else ''

        if len(image) != 0:
            return image

        if 'summary' in entry:
            r = re.search(r'(?:<img[^>]*src="([^"]+)"[^>]*\/?>)', entry['summary'])
            image = r.group(1) if r else ''

        return image

    @staticmethod
    def parse_summary(entry: dict, max_length=296):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.bypass_tables = False
        h.ignore_images = True
        h.images_to_alt = True
        parsed_summary = ''
        if 'content' in entry and len(entry['content']) > 0:
            parsed_summary = h.handle(entry['content'][0].value)

        if len(parsed_summary) == 0:
            if 'summary_detail' in entry and len(entry['summary_detail']) > 0:
                parsed_summary = h.handle(entry['summary_detail'].value)
            if len(parsed_summary) == 0 and 'summary' in entry:
                parsed_summary = h.handle(entry['summary'].value)

        parsed_summary = re.sub(r'\n\n+', '\n', parsed_summary)
        return RssUtils.string_truncate(parsed_summary, max_length)

    @staticmethod
    def parse_tags(entry: dict):
        if 'title' not in entry:
            return []
        pattern = r'\/([^\/]*?)\/|\[([^\[\]]*?)\]'
        tags_list = re.findall(pattern, entry['title'])
        tags_list = [match[0] if match[0] else match[1] for match in tags_list]
        tags = ', '.join(tag for tag in tags_list)
        return tags
