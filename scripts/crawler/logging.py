#! Python3

import os.path
import sys

ERROR_LOG_FILENAME = os.path.abspath('logs/error.log')
CRAWL_LOG_FILENAME = os.path.abspath('logs/crawl.log')

def log_to_file(message,filename):
    try:
        logfile = open(filename,'a')
    except:
        e = sys.exc_info()[0]
        print(f'Error: {e}' )
        print(f'{filename} - file open failed')
    try:
        logfile.write(message)
    except:
        e = sys.exc_info()[0]
        print(f'Error: {e}' )
        print(f'{filename} - file write failed')
    logfile.close()

def log_error_to_file(message,filename):
    try:
        error_logfile = open(filename,'a')
    except:
        e = sys.exc_info()[0]
        print(f'Error: {e}' )
        print(f'{filename} - file open failed')
    try:
        error_logfile.write(message)
    except:
        e = sys.exc_info()[0]
        print(f'Error: {e}' )
        print(f'{filename} - file write failed')
    error_logfile.close()

def log_crawl_to_file(crawl_data, filename):
    try:
        crawl_logfile = open(filename,'w')
    except:
        e = sys.exc_info()[0]
        print(f'Error: {e}' )
        print(f'{filename} - file open failed')
    try:
        crawl_logfile.write(crawl_data)
    except:
        e = sys.exc_info()[0]
        print(f'Error: {e}' )
        print(f'{filename} - file write failed')
    crawl_logfile.close()