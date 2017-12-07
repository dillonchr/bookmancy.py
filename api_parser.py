from html.parser import HTMLParser


class AbeSearchParser(HTMLParser):
    def __init__(self):
        self.listings = []
        self._current_listing = None
        self._capture_price = False
        super().__init__()

    @staticmethod
    def get_item_prop(attrs, prop):
        if AbeSearchParser.has_attr(attrs, 'itemprop', prop):
            return AbeSearchParser.get_attr(attrs, 'content')
        return False

    @staticmethod
    def has_attr(attrs, name, value):
        return AbeSearchParser.get_attr(attrs, name).startswith(value)

    @staticmethod
    def get_attr(attrs, name):
        matches = [t[1] for t in attrs if t[0] == name]
        return matches[0] if len(matches) > 0 else ''

    def handle_metatag(self, attrs):
        date_published = self.get_item_prop(attrs, 'datePublished')
        about = self.get_item_prop(attrs, 'about')
        if date_published:
            self._current_listing['year'] = int(date_published)
        elif about:
            self._current_listing['about'] = about

    def handle_starttag(self, tag, attrs):
        in_listing = self._current_listing is not None
        if len([t for t in attrs if t[0] == 'id' and t[1].startswith('book-')]) > 0:
            if in_listing:
                self.listings.append(self._current_listing)
            self._current_listing = {}
        elif in_listing and tag == 'meta':
            self.handle_metatag(attrs)
        elif in_listing and tag == 'span':
            self._capture_price = self.has_attr(attrs, 'class', 'price')
        elif in_listing and tag == 'img':
            if len(attrs) > 3:
                src = self.get_attr(attrs, 'src')
                self._current_listing['image'] = None if src.startswith('//') else src

    def handle_endtag(self, tag):
        if self._current_listing is not None and tag == 'body':
            self.listings.append(self._current_listing)

    def handle_data(self, data):
        if self._capture_price:
            price = data[4:]
            if 'price' in self._current_listing:
                self._current_listing['shipping'] = price
            else:
                self._current_listing['price'] = price
            self._capture_price = False

    def error(self, message):
        pass


def parse_html(html):
    parser = AbeSearchParser()
    parser.feed(html)
    return parser.listings
