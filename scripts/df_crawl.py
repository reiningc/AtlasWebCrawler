#!/usr/bin/env python3.7

# Depth-First Crawl:
# The program will start at the start page, randomly choose one of the links on that page, 
# then follow it to the next page. Then, at the next page, it randomly chooses a link 
# from the options available, and follows it. This makes a chain from the starting page. 
# This continues until the program hits the requested page limit.

import crawler.request
import crawler.parseHTML
import crawler.logging
import random
import time
import json
import sys
import os.path

KEYWORD = None
#if len(sys.argv) < 3:
    #raise ValueError('Not enough arguments. Include starting URL and page limit.')
#elif len(sys.argv) > 4:
    #raise ValueError('Too many arguments. Include starting URL, page limit, and keyword (optional).')
#elif len(sys.argv) == 4:
    #KEYWORD = sys.argv[3]
#START = sys.argv[1]
#LIMIT = int(sys.argv[2])


def df_crawl(starting_URL, page_limit, keyword=None):
    if page_limit < 1:
        error_message = 'Page limit must be at least 1 for depth first crawl.'
        crawler.logging.log_to_file(error_message,crawler.logging.ERROR_LOG_FILENAME)
        return -1
    
    # count of pages crawled
    pages_crawled = 0
    keywordFound = False
    site_id_num = 0
    last_site_id_num = None
    # start at starting URL
    cleaned_starting_URL = crawler.request.prepare_URL_for_crawl(starting_URL)
    current_URL = cleaned_starting_URL

    uncrawlable_links = set()
    crawl_delay = 1
    crawl_data = {}
    crawl_data['nodes'] = []
    crawl_data['links'] = []
    crawled_sites = set()
    site_title = ''
    site_links = set()
    error_messages = []     # list of error messages encountered - will be logged to error.log

    # crawl until we hit page limit
    while pages_crawled < page_limit:
        next_URL_list = []
        site_html = -1
        # look for good URL to crawl from list of URLs 
        while current_URL in uncrawlable_links or site_html == -1:
            # add scheme to URL if needed
            current_URL = crawler.request.prepare_URL_for_crawl(current_URL)
            # request html webpage
            site_html, crawl_delay = crawler.request.request_website(current_URL)
            # if request_website returns -1, it means site was unable to be read
            if site_html == -1:
                uncrawlable_links.add(current_URL)
                # Exit if starting URL is uncrawlable
                if cleaned_starting_URL in uncrawlable_links:
                    error_message = f'Depth First Crawl failed. Starting URL: {starting_URL} unable to be crawled.'
                    print(error_message)
                    crawler.logging.log_error_to_file(error_message)
                    return -1

                # Prevent cycles by avoiding visited links
                if len(site_links) > 1:
                    next_URL_list = random.sample(site_links,k=1)
                    while next_URL_list[0] in crawl_data.keys():
                        next_URL_list = random.sample(site_links,k=1)
                
                # If no links, error out
                if len(next_URL_list) < 1:
                    pages_crawled = page_limit
                    error_message = f"{current_URL}: no accessible links!"
                    print(error_message)
                    error_messages.append(error_message)
                
                if next_URL_list:
                    current_URL = next_URL_list[0]
                error_messages.append(crawl_delay) # if error, the error message is returned as crawl_delay from request_website()
                crawl_delay = 1


        # get title from webpage
        site_title = crawler.parseHTML.get_page_title(site_html)
        # get all links from webpage
        site_links = crawler.parseHTML.get_all_links(site_html, current_URL, crawl_data.keys())
        # check for keyword on webpage
        if keyword is not None:
            keywordFound = crawler.parseHTML.contains_keyword(site_html, keyword)

        crawl_data['nodes'].append({'id': site_id_num, 'name': site_title,'link': current_URL,'keyword': keywordFound})
        # don't add links for first site crawled
        if len(crawled_sites) != 0:
            crawl_data['links'].append({'source': site_id_num,'target': last_site_id_num})
        crawled_sites.add(current_URL)

        last_site_id_num = site_id_num
        site_id_num += 1

        # if keyword found, stop crawl
        if keyword is not None and keywordFound:
            break

        # randomly choose one of the links to visit next
        
        # Prevent cycles by avoiding visited links
        if len(site_links) >= 1:
            next_URL_list = random.sample(site_links,k=1)
            while next_URL_list[0] in crawled_sites:
                #print('duplicate URL avoidance ACTIVATED! url:',next_URL_list[0])
                next_URL_list = random.sample(site_links,k=1)
        
        # If no links, error out
        if len(next_URL_list) < 1:
            pages_crawled = page_limit
            error_messages.append(f"Site URL:{current_URL} ==> length of next_URL_list is < 1 - no links!")
            #raise ValueError('No links available')
        else:
            current_URL = next_URL_list[0]
            pages_crawled += 1
        
        time.sleep(crawl_delay)

    # convert sets of links in crawl_data to lists for json conversion, then
    # save crawl in log file
    # save errors in log file
    #crawl_data_json = json.dumps(crawl_data, indent=4)
    crawl_data_json = json.dumps(crawl_data)
    crawler.logging.log_crawl_to_file(crawl_data_json)
    error_data_json = json.dumps(error_messages)
    crawler.logging.log_error_to_file(error_data_json)
    return crawl_data_json


#df_crawl(START,LIMIT,KEYWORD)