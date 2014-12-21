import urllib2
import re


def get_data_from_site(site):
    response = urllib2.urlopen(site)
    html = response.read()
    return html


def store_data_locally(data, dest):
    with open(dest, 'w+') as f:
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
    for line in data:
        in_table = table_check(in_table, line)
        if in_table:
            sub_names.append(get_links(line))
    return [x for x in sub_names if x]


def parse_ufv_data(data):
    links = parse_ufv_links(data)
    return links


def main():
    site = 'http://www.ufv.ca/arfiles/includes/201501-timetable-with-changes.htm'
    dest = 'ufv_class_data.html'
    # data = get_data_from_site(site)
    # store_data_locally(data, dest)
    with open('ufv_class_data.html', 'r') as f:
        data = f.read()
    parse_ufv_data(data)


if __name__ == '__main__':
    main()