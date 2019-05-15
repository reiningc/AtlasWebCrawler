#! python3

# Breadth-First Crawl:
# The program will start at the start page, then follow ALL links from that page, 
# then follow ALL links from each page it visits. This makes a sprawling graph
# with the start page as the center. 
# The crawl continues until the program hits the requested breadth limit.

import crawler.request
import crawler.parseHTML
import random
import time
import json
from collections import deque
import sys

KEYWORD = None
if len(sys.argv) < 3:
    raise ValueError('Not enough arguments. Include starting URL and breadth limit.')
elif len(sys.argv) == 4:
    KEYWORD = sys.argv[3]
START = sys.argv[1]
LIMIT = int(sys.argv[2])

CRAWL_LOG_FILENAME = os.path.abspath('scripts/logs/crawl.log')

def log_crawl_to_file(crawl_data, filename):
    try:
        crawl_logfile = open(filename,'w')
    except:
        e = sys.exc_info()[0]
        print( "<p>Error: %s</p>" % e )
        print('crawl.log file open failed')
    try:
        crawl_logfile.write(crawl_data)
    except:
        e = sys.exc_info()[0]
        print( "<p>Error: %s</p>" % e )
        print('crawl.log file write failed')
    crawl_logfile.close()

def bf_crawl(starting_URL, breadth_limit, keyword=None):
    if breadth_limit < 1:
        error_message = 'Page limit must be at least 1 for breadth first crawl.'
        crawler.request.log_error_to_file(error_message,crawler.request.ERROR_LOG_FILENAME)
        return -1

    if keyword is not None:
        return bf_crawl_with_keyword(starting_URL, breadth_limit, keyword)

    cleaned_starting_URL = crawler.request.prepare_URL_for_crawl(starting_URL)
    crawl_delay = 1
    site_title = ''
    site_links = set()
    crawl_data = {}                             # crawl_data will be stored in crawl.log at end of crawl
    uncrawlable_links = set()
    sites_to_visit = deque()                    # queue for links to be visited during breadth-first traversal
    current_level_links = deque()               # queue for nodes on current level - used for adding links to sites_to_visit at end of level
    current_level_links.append(cleaned_starting_URL)
    current_breadth_level = 0

    while current_breadth_level < breadth_limit:
        # load links into nodes to visit queue from the current level's links
        while len(current_level_links) > 0:
            sites_to_visit.append(current_level_links.popleft())
        # visit each link possible in sites_to_visit
        while len(sites_to_visit) > 0:
            if starting_URL in uncrawlable_links:
                error_message = 'Breadth First Crawl failed. Starting URL: ' + starting_URL +' unable to be crawled.'
                crawler.request.log_error_to_file(error_message,crawler.request.ERROR_LOG_FILENAME)
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
                site_title = crawler.parseHTML.get_page_title(current_URL)
                site_links = crawler.parseHTML.get_all_links(site_html,current_URL,crawl_data.keys())

                crawl_data[current_URL] = {'originURL':last_visited_URL,'siteTitle':site_title,'keywordFound':False, 'links':site_links}


    return 0

def bf_crawl_with_keyword(starting_URL, breadth_limit, keyword):

    return 0



bf_crawl(START,LIMIT,KEYWORD)