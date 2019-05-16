#! python3

# Breadth-First Crawl:
# The program will start at the start page, then follow ALL links from that page, 
# then follow ALL links from each page it visits. This makes a sprawling graph
# with the start page as the center. 
# The crawl continues until the program hits the requested breadth limit.

import crawler.request
import crawler.parseHTML
import crawler.logging
import random
import time
import json
import sys
import os.path
from collections import deque

KEYWORD = None
if len(sys.argv) < 3:
    raise ValueError('Not enough arguments. Include starting URL and breadth limit.')
elif len(sys.argv) > 4:
    raise ValueError('Too many arguments. Include starting URL, page limit, and keyword (optional).')
elif len(sys.argv) == 4:
    KEYWORD = sys.argv[3]
START = sys.argv[1]
LIMIT = int(sys.argv[2])


def add_links_to_site_origin(origins_dict, origin, links):
    for link in links:
        origins_dict[link] = origin

def add_links_to_current_level(current_level_links,links):
    for link in links:
        current_level_links.append(link)

def bf_crawl(starting_URL, breadth_limit, keyword=None):
    if breadth_limit < 1:
        error_message = 'Breadth limit must be at least 1 for breadth first crawl.'
        crawler.logging.log_to_file(error_message,crawler.logging.ERROR_LOG_FILENAME)
        return -1

    if keyword is not None:
        return bf_crawl_with_keyword(starting_URL, breadth_limit, keyword)

    cleaned_starting_URL = crawler.request.prepare_URL_for_crawl(starting_URL)
    crawl_delay = 1
    site_title = ''
    site_links = set()
    crawl_data = {}                 # crawl_data will be stored in crawl.log at end of crawl
    site_origins = {}               # how crawler reached each site
    uncrawlable_links = set()       # links unable to be reached
    sites_to_visit = deque()        # queue for links to be visited during breadth-first traversal
    current_level_links = deque()   # queue for nodes on current level - used for adding links to sites_to_visit at end of level
    current_level_links.append(cleaned_starting_URL)
    site_origins[cleaned_starting_URL] = None
    current_breadth_level = 0

    while current_breadth_level < breadth_limit:
        # load links into nodes to visit queue from the current level's links
        while len(current_level_links) > 0:
            sites_to_visit.append(current_level_links.popleft())
        # visit each link possible in sites_to_visit
        while len(sites_to_visit) > 0:
            if starting_URL in uncrawlable_links:
                error_message = f'Breadth First Crawl failed. Starting URL: {starting_URL} unable to be crawled.'
                crawler.logging.log_to_file(error_message,crawler.logging.ERROR_LOG_FILENAME)
                return -1
            current_URL = sites_to_visit.popleft()
            # prep URL for requesting webpage (add scheme if needed)
            # request webpage
            # confirm webpage retrieved successfully
            current_URL = crawler.request.prepare_URL_for_crawl(current_URL)
            site_html, crawl_delay = crawler.request.request_website(current_URL)
            if site_html == -1:
                uncrawlable_links.add(current_URL)
            else:
                # pull site title
                # pull webpage links
                # add links to site_origins and current_level_links
                # add URL to crawl data
                site_title = crawler.parseHTML.get_page_title(site_html)
                site_links = crawler.parseHTML.get_all_links(site_html,current_URL,crawl_data.keys())
                add_links_to_site_origin(site_origins,current_URL,site_links)
                add_links_to_current_level(current_level_links,site_links)
                crawl_data[current_URL] = {'originURL':site_origins[current_URL],'siteTitle':site_title,'keywordFound':False, 'links':site_links}
                time.sleep(crawl_delay)
        # Finished crawling current level
        current_breadth_level += 1

    # convert sets of links in crawl_data to lists for json conversion, then
    # save crawl in log file
    for website in crawl_data:
        crawl_data[website]['links'] = list(crawl_data[website]['links'])
    crawl_data_json = json.dumps(crawl_data, indent=4)
    crawler.logging.log_crawl_to_file(crawl_data_json, crawler.logging.CRAWL_LOG_FILENAME)

    return 0

def bf_crawl_with_keyword(starting_URL, breadth_limit, keyword):

    return 0



bf_crawl(START,LIMIT,KEYWORD)