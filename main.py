from reader import Reader
from ufv_parser import parse_ufv_data
import pickle
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def main():
    site = 'http://www.ufv.ca/arfiles/includes/201501-timetable-with-changes.htm'
    dest = 'ufv_class_data.html'
    reader = Reader(site, dest, 'cp1252')
    html_data = reader.html
    stripped = strip_tags(html_data)
    print(stripped)
    # html_soup = BeautifulSoup(html_data)
    # store_data_locally(html_soup.pretify(), dest)
    # with open('soup.pk', 'rb') as f:  # TODO REMOVE
    #    html_soup = pickle.load(f)
    # parse_ufv_data(html_soup)


if __name__ == '__main__':
    main()
