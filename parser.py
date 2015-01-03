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


def parse_ufv_data(data):
    links = parse_ufv_links(data)
    subject_data = split_sections(data, links)
    return links


def main():
    site = 'http://www.ufv.ca/arfiles/includes/201501-timetable-with-changes.htm'
    dest = 'ufv_class_data.html'
    data = str(get_data_from_site(site))
    # store_data_locally(data, dest)
    with open('ufv_class_data.html', 'rb') as f:
        data = BeautifulSoup(f)
    parse_ufv_data(data)


if __name__ == '__main__':
    main()