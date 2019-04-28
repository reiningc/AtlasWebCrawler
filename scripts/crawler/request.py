#! python3
# request.py - HTTP request web page from server

from . import parseHTML
import urllib.request
import urllib.parse
import urllib.robotparser

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
        with urllib.request.urlopen(URL) as response:
            # read response from server - this comes in as bytes object and has to be decoded into utf-8
            html = response.read().decode('utf-8')
            print(html)
            # collect links from html webpage
            links = parseHTML.get_all_links(html, URL)
            print(links)

    else:
        raise ValueError('Cannot fetch requested page')
    
    return links
