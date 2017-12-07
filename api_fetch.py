import re
import urllib.parse
import urllib.request

is_hardback = lambda x: re.compile('hardcover|hardback|^hb$|^hc$|^h$', re.IGNORECASE).match(x) is not None
is_paperback = lambda x: re.compile('softcover|paperback|^pb$|^p$|^s$', re.IGNORECASE).match(x) is not None


def get_html_for_search(author, title='', publisher='', year=2017, format=False):
    querystring = {
        'an': author,
        'pn': publisher,
        'tn': title,
        'yrh': year if 999 < year < 10000 else '',
        'bi': 0 if not format else 'h' if is_hardback(format) else 's' if is_paperback(format) else 0
    }
    url = 'https://www.abebooks.com/servlet/SearchResults?bx=off&ds=50&recentlyadded=all&sortby=17&sts=t&' + \
          urllib.parse.urlencode(querystring)

    response = urllib.request.urlopen(url)
    html = response.read()
    response.close()
    return str(html)

