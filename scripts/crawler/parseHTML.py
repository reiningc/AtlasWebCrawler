#! python3

import urllib.parse
from bs4 import BeautifulSoup

def parse_base_URL(URL):
    # Parses seed into 6-item named tuple: (scheme, netloc, path, params, query, fragment)
    parsedURL = urllib.parse.urlparse(URL)

    return parsedURL.scheme + '://' + parsedURL.netloc

def is_relative_link(link_class, link_title, link_URL, container_class):
    # relative links within a <div>
    if container_class and ('rel' in container_class or 'internal' in container_class):
        return True
    
    # relative links types:
    # - has a class and 'internal' is in the class
    # - link starts with '.': ../index.html or ./general
    # - link starts with '/', but not '//: /index.html or /general
    # - link is in the title
    # - link is just 'index.html'

    if link_class and 'internal' in link_class \
        or link_URL.startswith('.') \
        or link_URL.startswith('/') and not link_URL.startswith('//') \
        or link_title \
        or link_URL == 'index.html':
        return True

    return False

def get_page_title(webpage):
    start_of_title_index = webpage.find('<title>') + 7   # +7 chars to offset length of <title>

    # if find returns -1, then <title> has not been found in webpage
    if start_of_title_index < 0:
        raise ValueError('No title tags in webpage')
    
    end_of_title_index = webpage.find('<',start_of_title_index)

    return webpage[start_of_title_index:end_of_title_index]

def format_relative_URL(relative_URL, origin_URL):
    # levels up needed to attach relative_URL to the end of origin_URL
    relative_levels_up = 0
    # chars to skip in relative_URL to account for ../ or ./ type relative URLs
    chars_to_skip = 0

    # if the relative URL starts with ../ or ./, need to go that many levels up
    # if it starts with /, go up two levels
    if relative_URL.startswith('.'):
        for char in relative_URL:
            if char is '.':
                relative_levels_up += 1
                chars_to_skip += 1
            if char is '/':
                break
    elif relative_URL.startswith('/'):
        relative_levels_up += 2

    # determine levels up possible (-2 to exclude the // after scheme: http(s)://)
    possible_levels_up = -2
    for char in origin_URL:
        if char is '/':
            possible_levels_up += 1
    
    #print('relative_URL:',relative_URL,'origin_URL:',origin_URL)
    #if relative_levels_up > possible_levels_up:
    #    raise ValueError('Not possible to reach relative URL')
    
    # parse out sections from origin_URL
    parsed_URL = urllib.parse.urlparse(origin_URL)
    URL_path_sections = []
    section_starting_index = 0
    section_ending_index = 0
    for i in range(1, len(parsed_URL.path)):
        if parsed_URL.path[i] == '/':
            section_ending_index = i
            URL_path_sections.append(parsed_URL.path[section_starting_index:section_ending_index])
            section_starting_index = i

    # build URL based on relative level
    levels_to_build = possible_levels_up - relative_levels_up
    formatted_relative_URL = parsed_URL.scheme + "://" + parsed_URL.netloc
    """
    print('possible levels up:',possible_levels_up,', relative_levels_up:',relative_levels_up)
    print('levels to build:',levels_to_build,'relativeURL:',relative_URL,'originURL:',origin_URL)
    print('formatted_relative_URL:',formatted_relative_URL)
    print('URL_path_sections:',URL_path_sections)
    """
    for i in range(min(levels_to_build,len(URL_path_sections))):
        formatted_relative_URL += URL_path_sections[i]
        #print('ADDED TO formatted_relative_URL:',formatted_relative_URL)
    
    if not relative_URL[chars_to_skip:].startswith('/'):
        formatted_relative_URL += '/'
    formatted_relative_URL += relative_URL[chars_to_skip:]


    #print('FINAL formatted_relative_URL:',formatted_relative_URL)
    return formatted_relative_URL

def has_ignorable_beginning_or_ending(link_URL):
    ignore_endings = {'.css', '.js', '.png', '.jpg', '.txt','rss/','rss','.ico','.bmp','.jpeg', \
        '.zip','.7z','.doc', '.asx','.docx','.flv','.gif','.mid','.ppt','.mov','.mp3','.ogg','.pdf', \
        '.ra','.ram','.rm','.swf','.wav','.wma','.wmv','.xml','.m4a','.mp4','.m4b','javascript:;',\
        '.javascript','.javascript:','/db','.tgz','/print'}
    ignore_beginnings = {'exmail.','email','gmail','mail','mailto','fonts.googleapis.com','tel:','ftp:',\
        'javascript:','javascript:;','search.'}
    
    # parse link to check ending against set of ignorable link endings
    parsed_link = urllib.parse.urlparse(link_URL)
    parsed_link_ending_start_index = parsed_link.path.rfind('/')
    parsed_link_ending_end_index = len(parsed_link.path)
    parsed_link_ending = parsed_link.path[parsed_link_ending_start_index:parsed_link_ending_end_index]

    # if a link ends with one of the ignore_endings, or just has it in the ending (ex: ../style.css?mvmir), it is ignorable
    for ending in ignore_endings:
        if link_URL.endswith(ending) or parsed_link_ending.endswith(ending):
            return True

    # if a link starts with one of the ignore_beginnings, it is ignorable
    for beginning in ignore_beginnings:
        if link_URL.startswith(beginning) or parsed_link.netloc.startswith(beginning):
            return True
    
    return False

# get_all_links takes in an HTML webpage and returns
# the set of unique links on that webpage
def get_all_links(webpage, URL, visited_URLs):
    base_URL = parse_base_URL(URL)
    soup = BeautifulSoup(webpage,'html.parser')

    unique_links = set()
    relative_links = set()
    

    # find all hrefs
    for link in soup.find_all('a'):
        link_URL = link.get('href')
        is_ignorable_link = False

        # links can be ignored if:
        # if a link is empty - *check for Nonetypes to prevent errors in the following conditionals*
        # if a link starts with #, its for a subsection on the same webpage
        # if a link is for an ignorable type (email, documents, etc)
        # if a link just links back to itself
        if link_URL == None or link_URL == '' or link_URL.startswith('#') \
            or link_URL == URL:
            is_ignorable_link = True
        elif has_ignorable_beginning_or_ending(link_URL):
            is_ignorable_link = True
        elif is_relative_link(link.get('class'),link.get('title'),link_URL,link.parent.get('class')) \
            and link_URL not in relative_links:
            relative_links.add(link_URL)
        # cut off any trailing /'s in link
        elif link_URL[len(link_URL)-1] == '/':
            link_URL = link_URL[:len(link_URL)-1]  
        
        if not is_ignorable_link:
            # if a link does start with //, need to prepend http: so the website can be requested by urllib.request
            # if a link doesn't start with http or //, it must be a link to another page
            # on this website. will have to add the URL to the beginning to make it
            # a useable address
            # this should catch http and https
            if link_URL.startswith('//'):
                link_URL = 'http:' + link_URL
            elif not link_URL.startswith('http') and not link_URL.startswith('https'):
                link_URL = base_URL + link_URL

            # check for duplicate links with different http/https schemes
            if link_URL.startswith('http://') \
                and 'https://' + link_URL[len('http://'):] in visited_URLs:
                    is_ignorable_link = True
            elif link_URL.startswith('https://') \
                and 'http://' + link_URL[len('https://'):] in visited_URLs:
                    is_ignorable_link = True


            # only add links that:
            #   - are not an ignorable link
            #   - are not already in the list of unique links
            #   - are not the starting URL
            #   - are not already in the list of relative links
            if not is_ignorable_link \
                and link_URL not in unique_links \
                and link_URL is not URL \
                and link_URL not in relative_links:
                unique_links.add(link_URL)

        # reset ignorable
        #is_ignorable_link = False

    # format relative links and to unique links
    for link in relative_links:
        formatted_link = format_relative_URL(link,URL)
        if formatted_link not in unique_links:
            unique_links.add(formatted_link)

    return unique_links

