#! Python3

import os.path
import sys
import boto3
from boto.s3.connection import S3Connection

s3 = S3Connection(os.environ['AWS_ACCESS_KEY_ID', os.environ('AWS_SECRET_ACCESS_KEY')])

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
    s3Res = boto3.resource('s3')
    obj = s3Res.Object('atlascrawlerlogs','error.log')
    obj.put(Body=message)
    """
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
    """

def log_crawl_to_file(crawl_data):
    s3Res = boto3.resource('s3')
    obj = s3Res.Object('atlascrawlerlogs','crawl.log')
    obj.put(Body=crawl_data)
    """
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
    """