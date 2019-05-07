#! python3

import unittest

import crawler.parseHTML

class Test(unittest.TestCase):
    
    def test_internal_site_link(self):
        test_text = '<a href="/events/python-events">'
        result = crawler.parseHTML.get_all_links(test_text, 'http://python.org', set())
        self.assertSetEqual(result, {'http://python.org/events/python-events'})

    def test_example_site(self):
        test_text = '<!doctype html>\n<html>\n<head>\n    <title>Example Domain</title>\n\n    <meta charset="utf-8" />\n    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <style type="text/css">\n    body {\n        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n        font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;\n        \n    }\n    div {\n        width: 600px;\n        margin: 5em auto;\n        padding: 50px;\n        background-color: #fff;\n        border-radius: 1em;\n    }\n    a:link, a:visited {\n        color: #38488f;\n        text-decoration: none;\n    }\n    @media (max-width: 700px) {\n        body {\n            background-color: #fff;\n        }\n        div {\n            width: auto;\n            margin: 0 auto;\n            border-radius: 0;\n            padding: 1em;\n        }\n    }\n    </style>    \n</head>\n\n<body>\n<div>\n    <h1>Example Domain</h1>\n    <p>This domain is established to be used for illustrative examples in documents. You may use this\n    domain in examples without prior coordination or asking for permission.</p>\n    <p><a href="http://www.iana.org/domains/example">More information...</a></p>\n</div>\n</body>\n</html>\n'
        result = crawler.parseHTML.get_all_links(test_text, 'http://example.com', set())
        self.assertSetEqual(result, {'http://www.iana.org/domains/example'})

    def test_no_links(self):
        test_text = '<!doctype html>\n<html>\n<head>\n    <title>Example Domain</title>\n\n    <meta charset="utf-8" />\n    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <style type="text/css">\n    body {\n        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n        font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;\n        \n    }\n    div {\n        width: 600px;\n        margin: 5em auto;\n        padding: 50px;\n        background-color: #fff;\n        border-radius: 1em;\n    }\n    a:link, a:visited {\n        color: #38488f;\n        text-decoration: none;\n    }\n    @media (max-width: 700px) {\n        body {\n            background-color: #fff;\n        }\n        div {\n            width: auto;\n            margin: 0 auto;\n            border-radius: 0;\n            padding: 1em;\n        }\n    }\n    </style>    \n</head>\n\n<body>\n<div>\n    <h1>Example Domain</h1>\n    <p>This domain is established to be used for illustrative examples in documents. You may use this\n    domain in examples without prior coordination or asking for permission.</p>\n    <p>More information...</p>\n</div>\n</body>\n</html>\n'
        result = crawler.parseHTML.get_all_links(test_text, 'http://example.com', set())
        self.assertSetEqual(result,set())    

    def test_only_internal_links(self):
        test_text = '<!doctype html>\n<html>\n<head>\n    <title>Example Domain</title>\n\n    <meta charset="utf-8" />\n    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <style type="text/css">\n    body {\n        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n        font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;\n        \n    }\n    div {\n        width: 600px;\n        margin: 5em auto;\n        padding: 50px;\n        background-color: #fff;\n        border-radius: 1em;\n    }\n    a:link, a:visited {\n        color: #38488f;\n        text-decoration: none;\n    }\n    @media (max-width: 700px) {\n        body {\n            background-color: #fff;\n        }\n        div {\n            width: auto;\n            margin: 0 auto;\n            border-radius: 0;\n            padding: 1em;\n        }\n    }\n    </style>    \n</head>\n\n<body>\n<div>\n    <h1>Example Domain</h1>\n    <a href="#bottom">Bottom</a><p>This domain is established to be used for illustrative examples in documents.\n <a href="#top>Top</a> You may use this\n    domain in examples without prior coordination or asking for permission.</p>\n    <p><a href="#example">More information...</a></p>\n</div>\n</body>\n</html>\n'
        result = crawler.parseHTML.get_all_links(test_text, 'http://example.com', set())
        self.assertSetEqual(result,set())
    
    def test_relative_URL_one_level_up(self):
        origin_URL = 'http://www.iana.org/gobs/dobz/rfc2606'
        relative_URL = './html/'
        result = crawler.parseHTML.format_relative_URL(relative_URL,origin_URL)
        self.assertEqual(result,'http://www.iana.org/gobs/dobz/html/')

    def test_relative_URL_two_levels_up(self):
        origin_URL = 'http://www.iana.org/gobs/dobz/rfc2606'
        relative_URL = '../html/'
        result = crawler.parseHTML.format_relative_URL(relative_URL,origin_URL)
        self.assertEqual(result,'http://www.iana.org/gobs/html/')
    
    def test_relative_URL_no_dots(self):
        origin_URL = 'http://docs.python.org/3/library/decimal.html#decimal.Decimal'
        relative_URL = 'functions.html#int'
        result = crawler.parseHTML.format_relative_URL(relative_URL, origin_URL)
        self.assertEqual(result, 'http://docs.python.org/3/library/functions.html#int')

    def test_relative_URL_forward_slash_start(self):
        origin_URL = 'https://library.oregonstate.edu/floormaps/second-floor'
        relative_URL = '/floormaps/newspapers'
        result = crawler.parseHTML.format_relative_URL(relative_URL,origin_URL)
        self.assertEqual(result,'https://library.oregonstate.edu/floormaps/newspapers')
    
    def test_parse_base_URL_http(self):
        URL = 'http://www.iana.org/gobs/dobz/rfc2606'
        result = crawler.parseHTML.parse_base_URL(URL)
        self.assertEqual(result, 'http://www.iana.org')

unittest.main(verbosity=2)