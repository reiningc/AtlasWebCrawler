#! python3
# request.py - HTTP request web page from server

from . import parseHTML
import urllib.request
import urllib.parse
import urllib.robotparser
import urllib.error

def prepare_URL_for_crawl(URL):
    # Parses seed into 6-item named tuple: (scheme, netloc, path, params, query, fragment)
    parsedURL = urllib.parse.urlparse(URL)

    # Builds URL if no scheme (http/https) provided
    request_URL = URL
    if not len(parsedURL.scheme):
        request_URL = 'http://' + request_URL # Assume http if no scheme
    
    return request_URL

def request_website(URL):
    html = ''

    # Builds robots.txt URL
    request_URL = URL
    robots_URL = request_URL + '/robots.txt' # URL for SEED's robots.txt

    # Load robotsURL into robot file parser to later check if fetching page is allowable
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_URL)
    rp.read()

    # If robots.txt allows for fetching page, request the page
    if (rp.can_fetch('*', request_URL)):
        # try opening URL, post errors to log file if not successful
        try:
            response = urllib.request.urlopen(request_URL)
        except urllib.error.URLError as err:
            error_logfile = open('logs/error.log', 'a')
            error_message = request_URL + ' - '
            # add to error message depending on error type. check first for a HTTP error (if it has a code, its a HTTP error), otherwise it is an URL error
            if hasattr(err, 'code'):
                error_message += 'Failed to reach server. Error code: ' + str(err.code) + ': ' + err.reason + '\n'
            elif hasattr(err, 'reason'):
                error_message += 'Server could not fill the request. Reason: ' + err.reason + '\n'

            error_logfile.write(error_message)
            error_logfile.close()
        else:
            # opening URL was successful
            # read response from server - this comes in as bytes object and has to be decoded into utf-8
            html = response.read().decode('utf-8', 'replace')

    else:
        raise ValueError('robots.txt prevents fetching requested page')
    
    return html
