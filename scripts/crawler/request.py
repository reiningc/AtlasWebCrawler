#! python3
# request.py - HTTP request web page from server

from . import parseHTML
import urllib.request
import urllib.parse
import urllib.robotparser
import urllib.error

def request_website(URL):
    # Parses seed into 6-item named tuple: (scheme, netloc, path, params, query, fragment)
    parsedURL = urllib.parse.urlparse(URL)

    # Builds robots.txt URL
    robotsURL = parsedURL.scheme + '://' + parsedURL.netloc + '/robots.txt' # URL for SEED's robots.txt

    # Load robotsURL into robot file parser to later check if fetching page is allowable
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robotsURL)
    rp.read()

    links = set()
    # If robots.txt allows for fetching page, request the page
    if (rp.can_fetch('*', URL)):
        # try opening URL, post errors to log file if not successful
        try:
            response = urllib.request.urlopen(URL)
        except urllib.error.URLError as err:
            error_logfile = open('logs/error.log', 'a')
            error_message = URL + ' - '
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
            html = response.read().decode('utf-8')

            # collect links from html webpage
            links = parseHTML.get_all_links(html, URL)
    else:
        raise ValueError('robots.txt prevents fetching requested page')
    
    return links
