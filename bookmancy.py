import api_fetch
import api_parser

def search(opts):
    return api_parser.parse_html(api_fetch.get_html_for_search(opts))


if __name__ == '__main__':
    search('hey')
