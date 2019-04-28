#! python3

# get_all_links takes in an HTML webpage and returns
# the set of unique links on that webpage
def get_all_links(webpage, URL):
    unique_links = set()
    start_of_link_index = webpage.find('href=')
    is_same_page_link = False
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

        # if a link doesn't start with http, it must be a link to another page
        # on this website. will have to add the URL to the beginning to make it
        # a useable address
        if not is_same_page_link and not link.startswith('http'):
            link = URL + link
        
        # only add links that aren't already in the list of unique links
        if not is_same_page_link and link not in unique_links and link is not URL:
            unique_links.add(link)
        # find next link
        start_of_link_index = webpage.find('href', start_of_link_index)

    return unique_links

