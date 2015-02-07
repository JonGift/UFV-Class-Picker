from reader import Reader
from ufv_parser import parse_ufv_data
import pickle
from html.parser import HTMLParser
from flask import Flask, request, jsonify, render_template
import html2text
import re


app = Flask(__name__)


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


def pull_info(str_input):
    string_edit = str_input
    return_list = []

    start_recording = False
    to_append = ''
    previous_letter = ''
    for index, letter in enumerate(string_edit):
        if previous_letter == '-' and letter == '-' and (string_edit[index+1]) == ' ':
            start_recording = True

        if start_recording == True:
            if previous_letter == ' ' and letter == ' ':
                if to_append != '' and to_append != ' ':
                    return_list.append(to_append)
                    to_append = ''
                else:
                    to_append = ''
            elif letter != '\n':
                if to_append == '' and letter == ' ':
                    pass
                to_append = ''.join((to_append, letter))
            if previous_letter == '-' and letter == '-' and string_edit[index+1] == '-':
                return_list.append('END BLOCK')
                start_recording = False

        previous_letter = letter

    for i in range(len(return_list)):
        print(return_list[i])
    print('The length of return list is ' + str(len(return_list)))


#@app.route('/', methods=['GET'])
def main():
    site = 'http://www.ufv.ca/arfiles/includes/201501-timetable-with-changes.htm'
    dest = 'ufv_class_data.html'
    reader = Reader(site, dest, 'cp1252')
    html_data = reader.html
    # stripped = strip_tags(html_data)
    stripped = html2text.html2text(html_data)
    # entries = ['bob', 'jim']
    # return render_template('show_entries.html', entries=entries)
    pull_info(stripped)
    #print(stripped)
    # html_soup = BeautifulSoup(html_data)
    # store_data_locally(html_soup.pretify(), dest)
    # with open('soup.pk', 'rb') as f:  # TODO REMOVE
    #    html_soup = pickle.load(f)
    # parse_ufv_data(html_soup)


if __name__ == '__main__':
    #app.debug = True
    #app.run(host='192.168.0.3')
    main()