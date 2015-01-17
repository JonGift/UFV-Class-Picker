from reader import Reader
from ufv_parser import parse_ufv_data
import pickle


def main():
    site = 'http://www.ufv.ca/arfiles/includes/201501-timetable-with-changes.htm'
    dest = 'ufv_class_data.html'
    reader = Reader(site, dest, 'cp1252')
    # html_data = get_data_from_site(site)
    # html_soup = BeautifulSoup(html_data)
    # store_data_locally(html_soup.pretify(), dest)
    with open('soup.pk', 'rb') as f:  # TODO REMOVE
        html_soup = pickle.load(f)
    parse_ufv_data(html_soup)


if __name__ == '__main__':
    main()