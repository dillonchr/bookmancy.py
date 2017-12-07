import re
import urllib.parse
import urllib.request


def is_hardback(x):
    return re.compile('hardcover|hardback|^hb$|^hc$|^h$', re.IGNORECASE).match(x) is not None


def is_paperback(x):
    return re.compile('softcover|paperback|^pb$|^p$|^s$', re.IGNORECASE).match(x) is not None


def parse_format(x):
    if not x:
        return 0
    if is_hardback(x):
        return 'h'
    if is_paperback(x):
        return 's'
    return 0


def get_html_for_search(author, title='', publisher='', year=2017, format=False):
    querystring = {
        'an': author,
        'pn': publisher,
        'tn': title,
        'yrh': year if 999 < year < 10000 else '',
        'bi': parse_format(format)
    }
    url = 'https://www.abebooks.com/servlet/SearchResults?bx=off&ds=50&recentlyadded=all&sortby=17&sts=t&' + \
          urllib.parse.urlencode(querystring)

    response = urllib.request.urlopen(url)
    html = response.read()
    response.close()
    return str(html)

