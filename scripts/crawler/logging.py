#! Python3

import os.path
import sys
import boto3

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

def log_error_to_file(message):
    s3 = boto3.resource('s3')
    obj = s3.Object('atlascrawlerlogs','error.log')
    obj.put(Body=message)


def log_crawl_to_file(crawl_data,crawl_filename):
    s3 = boto3.resource('s3')
    obj = s3.Object('atlascrawlerlogs',crawl_filename)
    obj.put(Body=crawl_data)
