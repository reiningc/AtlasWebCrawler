#!/usr/bin/env python2.7

# Depth-First Crawl:
# The program will start at the start page, randomly choose one of the links on that page, 
# then follow it to the next page. Then, at the next page, it randomly chooses a link 
# from the options available, and follows it. This makes a chain from the starting page. 
# This continues until the program hits the requested page limit.

import crawler.request
import crawler.parseHTML
import random
import time
import json
import sys

KEYWORD = None
if len(sys.argv) < 3:
    raise ValueError('Not enough arguments. Include starting URL and page limit.')
elif len(sys.argv) == 4:
    KEYWORD = sys.argv[3]
START = sys.argv[1]
LIMIT = int(sys.argv[2])

CRAWL_LOG_FILENAME = 'logs/crawl.log'

def log_crawl_to_file(crawl_data, filename):
    crawl_logfile = open(filename,'w')
    crawl_logfile.write(crawl_data)
    crawl_logfile.close()


def df_crawl(starting_URL, page_limit, keyword=None):
    if page_limit < 1:
        error_message = 'Page limit must be at least 1 for depth first crawl.'
        crawler.request.log_error_to_file(error_message,crawler.request.ERROR_LOG_FILENAME)
        return -1

    if keyword is not None:
        return df_crawl_with_keyword(starting_URL, page_limit, keyword)
    
    # count of pages crawled
    pages_crawled = 0
    last_visited_URL = None
    # start at starting URL
    current_URL = starting_URL

    uncrawlable_links = set()
    crawl_delay = 1
    crawl_data = {}
    site_title = ''
    site_links = set()
    # crawl until we hit page limit
    while pages_crawled < page_limit:
        next_URL_list = []
        site_html = -1
        # look for good URL to crawl from list of URLs 
        while current_URL in uncrawlable_links or site_html == -1:
            if starting_URL in uncrawlable_links:
                error_message = 'Depth First Crawl failed. Starting URL: ' + starting_URL +' unable to be crawled.'
                crawler.request.log_error_to_file(error_message,crawler.request.ERROR_LOG_FILENAME)
                return -1

            print('PREPARING URL: ', current_URL)
            # add scheme to URL if needed
            current_URL = crawler.request.prepare_URL_for_crawl(current_URL)
            # request html webpage
            site_html, crawl_delay = crawler.request.request_website(current_URL)
            # if request_website returns -1, it means site was unable to be read
            if site_html == -1:
                uncrawlable_links.add(current_URL)
                # Prevent cycles by avoiding visited links
                if len(site_links) > 1:
                    next_URL_list = random.sample(site_links,k=1)
                    while next_URL_list[0] in crawl_data.keys():
                        #print('duplicate URL avoidance ACTIVATED! url:',next_URL_list[0])
                        next_URL_list = random.sample(site_links,k=1)
                
                # If no links, error out
                if len(next_URL_list) < 1:
                    pages_crawled = page_limit
                    print("no links!")
                    raise ValueError('no links')
                
                current_URL = next_URL_list[0]


        # get title from webpage
        site_title = crawler.parseHTML.get_page_title(site_html)
        # get all links from webpage
        site_links = crawler.parseHTML.get_all_links(site_html, current_URL, crawl_data.keys())
        
        crawl_data[current_URL] = {'originURL':last_visited_URL,'siteTitle':site_title,'keywordFound':False, 'links':site_links}
        
        print("crawled",current_URL)
        last_visited_URL = current_URL

        # randomly choose one of the links to visit next
        
        # Prevent cycles by avoiding visited links
        if len(site_links) > 1:
            next_URL_list = random.sample(site_links,k=1)
            while next_URL_list[0] in crawl_data.keys():
                #print('duplicate URL avoidance ACTIVATED! url:',next_URL_list[0])
                next_URL_list = random.sample(site_links,k=1)
        
        # If no links, error out
        if len(next_URL_list) < 1:
            pages_crawled = page_limit
            print("no links!")
            #raise ValueError('No links available')
        else:
            current_URL = next_URL_list[0]
            pages_crawled += 1
        
        time.sleep(crawl_delay)
    
    # convert sets of links in crawl_data to lists for json conversion, then
    # save crawl in log file
    for website in crawl_data:
        crawl_data[website]['links'] = list(crawl_data[website]['links'])
    crawl_data_json = json.dumps(crawl_data, indent=4)
    log_crawl_to_file(crawl_data_json, CRAWL_LOG_FILENAME)

    return 0

def df_crawl_with_keyword(starting_URL, page_limit, keyword):

    return 0

df_crawl(START,LIMIT,KEYWORD)