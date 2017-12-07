import api_fetch
import api_parser


def search(author, title='', publisher='', year=2017, format=False):
    return api_parser.parse_html(api_fetch.get_html_for_search(
        author,
        title,
        publisher,
        year,
        format
    ))


if __name__ == '__main__':
    search(
        author='Truman Capote',
        publisher='Random House',
        title='In Cold Blood',
        year=1965
    )
