from urllib.request import urlopen

def get_html_for_search(search):
    response = urlopen('https://www.abebooks.com/servlet/SearchResults?bx=off&ds=50&recentlyadded=all&sortby=17&sts=t&an=derleth&pn=arkham')
    html = response.read()
    response.close()
    return str(html)

