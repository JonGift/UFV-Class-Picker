import urllib.request
import re
from bs4 import BeautifulSoup
import pickle
import sys; sys.setrecursionlimit(90000)

class section:
    def __init__(self):
        self.class_list = None

class individual_class:
    def __init__(self):
        self.name = None
        self.course_number = None
        self.credit_hours = None
        self.price = None
        self.prerequisites = None
        self.professors = None
        self.dates = None
        self.class_number = None



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


def split_sections(html_soup, links):
    """returns the raw html of each block of subject data in the soup"""
    links = links[:]
    subject_data = []
    buffer = []
    # html = html_soup.prettify().split('\n')
    with open('ufv_class_data.html', 'r') as f: # TODO REMOVE
        html = f.readlines()
    for line in html:
        if 'name' in line:
            for link in links:
                if re.search(r'a\s*name\s*=\s*\"{}'.format(link), line):
                    if buffer:
                        subject_data.append(buffer)
                        buffer = []
                    buffer.append(line)
                    links.remove(link)
            else:
                if buffer:
                    buffer.append(line)
        elif buffer:
            buffer.append(line)
    else:
        subject_data.append(buffer)
    return subject_data


def split_sections_naive(html_soup):
    """returns the raw html of each block of subject data in the soup"""
    subject_data = []
    buffer = []
    # html = html_soup.prettify().split('\n')
    with open('ufv_class_data.html', 'r') as f:  # TODO REMOVE
        html = f.readlines()
    for line in html:
        if 'a name=\"' in line:
            if buffer:
                subject_data.append(buffer)
            buffer = [line]
        elif buffer:
            buffer.append(line)
    subject_data.append(buffer)
    return subject_data


def parse_ufv_data(html_soup):
    # links = parse_ufv_links(html_soup.prettify())
    with open('links.pk', 'rb') as f:  # TODO REMOVE
        links = pickle.load(f)
    subject_data = split_sections_naive(html_soup)
    return links



def remove_struck_out_classes(text_data):
    all_data_buf = []
    single_class_buf = []
    in_class = False
    last_newline = True
    for line in text_data:
        if last_newline:
            if re.search('\s+\d+'):
                pass
        if '\n' in line:
            last_newline = True

