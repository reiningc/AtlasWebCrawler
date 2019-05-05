#! python3

import urllib.parse

def parse_base_URL(URL):
    # Parses seed into 6-item named tuple: (scheme, netloc, path, params, query, fragment)
    parsedURL = urllib.parse.urlparse(URL)

    return parsedURL.scheme + '://' + parsedURL.netloc


def get_page_title(webpage):
    start_of_title_index = webpage.find('<title>') + 7   # +7 chars to offset length of <title>

    # if find returns -1, then <title> has not been found in webpage
    if start_of_title_index < 0:
        raise ValueError('No title tags in webpage')
    
    end_of_title_index = webpage.find('<',start_of_title_index)

    return webpage[start_of_title_index:end_of_title_index]

def format_relative_URL(relative_URL, origin_URL):
    # determine levels up needed
    relative_levels_up = 0
    for char in relative_URL:
        if char is '.':
            relative_levels_up += 1
        if char is '/':
            break

    # determine levels up possible (-2 to exclude the // after scheme: http(s)://)
    possible_levels_up = -2
    for char in origin_URL:
        if char is '/':
            possible_levels_up += 1
    
    if relative_levels_up > possible_levels_up:
        raise ValueError('Not possible to reach relative URL')
    
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
    for i in range(levels_to_build):
        formatted_relative_URL += URL_path_sections[i]
    
    formatted_relative_URL += relative_URL[relative_levels_up:]

    return formatted_relative_URL


# get_all_links takes in an HTML webpage and returns
# the set of unique links on that webpage
def get_all_links(webpage, URL):
    base_URL = parse_base_URL(URL)
    ignore_endings = {'.css', '.js', '.png', '.jpg', '.txt','rss/','rss','.ico','.bmp','.jpeg', \
        '.zip','.7z','.doc', '.asx','.docx','.flv','.gif','.mid','.ppt','.mov','.mp3','.ogg','.pdf', \
        '.ra','.ram','.rm','.swf','.wav','.wma','.wmv','.xml','.m4a','.mp4','.m4b','javascript:;',\
        '.javascript','.javascript:','/db','.tgz'}
    unique_links = set()
    start_of_link_index = webpage.find('href=')
    is_same_page_link = False
    is_ignorable = False

    # find all hrefs
    while start_of_link_index is not -1:
        # move start index past 'href="' in link tag
        start_of_link_index += 6
        # find end of link at the index of the next double quote
        end_of_link_index = webpage.find('"',start_of_link_index)
        link = webpage[start_of_link_index:end_of_link_index]

        # if a link starts with #, its for the same webpage and should be ignored
        if link.startswith('#'):
            is_same_page_link = True

        # if a link doesn't start with http or //, it must be a link to another page
        # on this website. will have to add the URL to the beginning to make it
        # a useable address
        # this should catch http and https
        if not is_same_page_link:
            if not link.startswith('//') and not link.startswith('http'):
                link = base_URL + link

        # if a link ends with one of the ignore_endings, it is ignorable
        for ending in ignore_endings:
            if link.endswith(ending):
                is_ignorable = True
                break

        # if a link starts with . it is a relative link that goes up 1+ levels
        if link.startswith('.'):
            link = format_relative_URL(link,URL)

        # only add links that:
        #   - are not a link to somewhere on the same page
        #   - do not have an ignorable ending
        #   - are not already in the list of unique links
        #   - are not the starting URL
        if not is_same_page_link and not is_ignorable and link not in unique_links and link is not URL:
            unique_links.add(link)
        
        # find next link
        start_of_link_index = webpage.find('href', start_of_link_index)

        # reset sentinels
        is_same_page_link = False
        is_ignorable = False


    return unique_links

