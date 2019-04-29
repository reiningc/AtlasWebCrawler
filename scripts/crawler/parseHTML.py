#! python3


def get_page_title(webpage):
    start_of_title_index = webpage.find('<title>') + 7   # +7 chars to offset length of <title>

    # if find returns -1, then <title> has not been found in webpage
    if start_of_title_index < 0:
        raise ValueError('No title tags in webpage')
    
    end_of_title_index = webpage.find('<',start_of_title_index)

    return webpage[start_of_title_index:end_of_title_index]


# get_all_links takes in an HTML webpage and returns
# the set of unique links on that webpage
def get_all_links(webpage, URL):
    ignore_endings = {'.css', '.js', '.png', '.jpg', '.txt','rss/','rss','.ico','.bmp','.jpeg', \
        '.zip','.7z','.doc', '.asx','.docx','.flv','.gif','.mid','.ppt','.mov','.mp3','.ogg','.pdf', \
        '.ra','.ram','.rm','.swf','.wav','.wma','.wmv','.xml','.m4a','.mp4','.m4b','javascript:;',\
        '.javascript','.javascript:'}
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
                link = URL + link

        # if a link ends with one of the ignore_endings, it is ignorable
        for ending in ignore_endings:
            if link.endswith(ending):
                is_ignorable = True
                break

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

