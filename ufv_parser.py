import re
from bs4 import BeautifulSoup
import pickle
import sys; sys.setrecursionlimit(90000)


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


def split_classes(subject_data):
    subject_class_data = []
    for subject in subject_data:
        subject_soup = BeautifulSoup(''.join(subject))
        title = subject_soup.find('a', attrs={'name': re.compile('.*')}).text.strip()
        classes = [x.prettify() for x in subject_soup.html.body.find_all('p', recursive=False)]
        subject_class_data.append([title] + [classes])
    return subject_class_data


def parse_ufv_data(html_soup):
    # links = parse_ufv_links(html_soup.prettify())
    with open('links.pk', 'rb') as f:  # TODO REMOVE
        links = pickle.load(f)
    subject_data = split_sections_naive(html_soup)
    subject_with_classes_data = split_classes(subject_data)
    texts = html_soup.findAll(text=True)

    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element)):
            return False
        return True

    visible_texts = u''.join([x for x in list(filter(visible, texts)) if x.strip()])
    with open('testlong.txt', 'w+') as f:
        f.write(visible_texts)
    # with open('testshort.txt', 'w+') as f:
    #     f.writelines([x for x in visible_texts if x.strip()])