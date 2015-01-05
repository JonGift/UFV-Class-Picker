import urllib.request
import re
from bs4 import BeautifulSoup


def get_data_from_site(site):
    response = urllib.request.urlopen(site)
    html = response.read()
    text = html.decode('cp1252')
    return text


def store_data_locally(data, dest):
    with open(dest, 'w') as f:
        f.write(data)


def table_check(tab, line):
    if tab:
        if re.search('</tr>', line):
            return False
        else:
            return True
    else:
        if re.search('<tr>', line):
            return True
        else:
            return False


def get_links(line):
    return re.findall('(?:.*?href.+?\#)(.+?)(?=\")', line)


def parse_ufv_links(data):
    sub_names = []
    in_table = False
    for line in data.split():
        in_table = table_check(in_table, line)
        if in_table:
            sub_names.append(get_links(line))
    return [x[0] for x in sub_names if x] # only returns lists that have data


def split_sections(data, links):
    subject_data = []
    buffer = []
    for link in links:
        for line in data.split():
            if re.search(r'a.*?name.*?{}'.format(link), line):
                buffer.append(line)
            if buffer:
                if re.search('-------', line):
                    subject_data.append(buffer)
                    buffer = []
                    break


def parse_ufv_data(html_soup):
    links = parse_ufv_links(html_soup.prettify())
    subject_data = split_sections(html_soup, links)
    return links


def main():
    site = 'http://www.ufv.ca/arfiles/includes/201501-timetable-with-changes.htm'
    dest = 'ufv_class_data.html'
    # html_data = get_data_from_site(site)
    # html_soup = BeautifulSoup(html_data)
    # store_data_locally(html_soup.pretify(), dest)
    with open(dest,  'rb') as f:
        html_soup = BeautifulSoup(f)
    parse_ufv_data(html_soup)


if __name__ == '__main__':
    main()