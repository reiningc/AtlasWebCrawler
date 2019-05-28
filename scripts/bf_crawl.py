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

def add_links_to_links_already_seen(seen_links, new_links):
    for link in new_links:
        seen_links.add(link)

def add_links_to_site_origin(origins_dict, origin, links):
    for link in links:
        if link not in origins_dict.keys():
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

    current_breadth_level = 0
    keywordFound = False
    site_id_num = 0
    cleaned_starting_URL = crawler.request.prepare_URL_for_crawl(starting_URL)
    crawl_delay = 1
    site_title = ''
    site_links = set()
    crawl_data = {}                 # crawl_data will be stored in crawl.log at end of crawl
    crawl_data['nodes'] = []
    crawl_data['links'] = []        
    links_already_seen = set([cleaned_starting_URL])      # all links seen by crawler (even unvisited)
    site_origins = {}               # how crawler reached each site
    uncrawlable_links = set()       # links unable to be reached
    error_messages = []             # list of error messages encountered - will be logged to error.log
    sites_to_visit = deque()        # queue for links to be visited during breadth-first traversal
    current_level_links = deque()   # queue for nodes on current level - used for adding links to sites_to_visit at end of level
    current_level_links.append(cleaned_starting_URL)
    site_origins[cleaned_starting_URL] = None

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
                error_messages.append(crawl_delay) # if error, the error message is returned as crawl_delay from request_website()
                crawl_delay = 1
            else:
                # pull site title
                # pull webpage links (unless this is the last level)
                # add links to site_origins and current_level_links
                # add URL to crawl data
                site_title = crawler.parseHTML.get_page_title(site_html)
                if current_breadth_level+1 != breadth_limit:
                    site_links = crawler.parseHTML.get_all_links(site_html,current_URL,links_already_seen)
                add_links_to_site_origin(site_origins,site_id_num,site_links)
                add_links_to_current_level(current_level_links,site_links)

                crawl_data['nodes'].append({'id': site_id_num,'name': site_title,'link':current_URL,'keyword':keywordFound})
                if len(links_already_seen) != 1:
                    crawl_data['links'].append({'source': site_id_num, 'target': site_origins[current_URL]})
                # add all the new site links to set of links already seen
                add_links_to_links_already_seen(links_already_seen,site_links)
                site_id_num += 1
                time.sleep(crawl_delay)
        # Finished crawling current level
        current_breadth_level += 1

    # convert sets of links in crawl_data to lists for json conversion, then
    # save crawl in log file
    #for website in crawl_data['nodes']:
    #    website['site_links'] = list(website['site_links'])
    crawl_data_json = json.dumps(crawl_data)
    crawler.logging.log_crawl_to_file(crawl_data_json)
    error_data_json = json.dumps(error_messages)
    crawler.logging.log_error_to_file(error_data_json)

    return crawl_data_json

def bf_crawl_with_keyword(starting_URL, breadth_limit, keyword):

    return 0



bf_crawl(START,LIMIT,KEYWORD)