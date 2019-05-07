#! python3
# request.py - HTTP request web page from server

from . import parseHTML
import urllib.request
import urllib.parse
import urllib.robotparser
import urllib.error

ERROR_LOG_FILENAME = 'logs/error.log'

def log_error_to_file(message,filename):
    error_logfile = open(filename,'a')
    error_logfile.write(message)
    error_logfile.close()


def prepare_URL_for_crawl(URL):
    # Parses seed into 6-item named tuple: (scheme, netloc, path, params, query, fragment)
    parsed_URL = urllib.parse.urlparse(URL)

    # Builds URL if no scheme (http/https) provided
    request_URL = URL
    if len(parsed_URL.scheme) == 0 and not URL.startswith('//'):
        request_URL = 'http://' + request_URL # Assume http if no scheme
    elif URL.startswith('//'):
        request_URL = 'http:' + request_URL
    
    return request_URL

def generate_robots_URL(URL):
    parsed_URL = urllib.parse.urlparse(URL)

    robots_URL = URL
    if len(parsed_URL.scheme) == 0:
            robots_URL = 'http://' + parsed_URL.netloc
    
    return robots_URL + '/robots.txt'

def request_website(URL):
    html = ''
    request_URL = URL
    # Builds robots.txt URL
    robots_URL = generate_robots_URL(request_URL) # URL for website's robots.txt

    # Load robotsURL into robot file parser to later check if fetching page is allowable
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_URL)
    try:
        rp.read()
    except Exception:
        return -1, 1

    crawl_delay = 1
    
    # If robots.txt allows for fetching page, request the page
    if (rp.can_fetch('*', request_URL)):
        # check robots.txt for crawl delay request to slow down crawler
        # using try/except as workaround for robotparser crawl_delay returning with Attribute Error instead
        # of None when no crawl delay is in the robots.txt file
        try:
            crawl_delay = max(crawl_delay,rp.crawl_delay('*'))
        except Exception:
            pass

        # try opening URL, post errors to log file if not successful
        try:
            response = urllib.request.urlopen(request_URL)
        except urllib.error.URLError as err:
            error_message = request_URL + ' - '
            # add to error message depending on error type. check first for a HTTP error (if it has a code, its a HTTP error), otherwise it is an URL error
            if hasattr(err, 'code'):
                error_message += 'Failed to reach server. Error code: ' + str(err.code) + ': ' + err.reason + '\n'
            elif hasattr(err, 'reason'):
                error_message += 'Server could not fill the request. Reason: ' + err.reason + '\n'
            log_error_to_file(error_message,ERROR_LOG_FILENAME)
            return -1, 1
        else:
            # opening URL was successful
            # read response from server - this comes in as bytes object and has to be decoded into utf-8
            html = response.read().decode('utf-8', 'replace')

    else:
        error_message = request_URL + ' - robots.txt prevents fetching requested page\n'
        log_error_to_file(error_message, ERROR_LOG_FILENAME)
        return -1, 1

    return html, crawl_delay
