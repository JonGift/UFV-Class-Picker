from reader import Reader
from ufv_parser import parse_ufv_data
import pickle
from html.parser import HTMLParser
from flask import Flask, request, jsonify, render_template

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
    previous_index = 0
    previous_letter = ''
    for index, letter in enumerate(string_edit):
        if start_recording == True:
            if letter == ' ' and previous_letter == ' ':
                return_list.append(to_append)
                to_append = ''
                start_recording = False
            elif letter != ' ':
                print(letter)
                ''.join((to_append, letter))
        if previous_letter == '-':
            if letter == ' ':
                if string_edit[index+1].isupper() == True and string_edit[index + 2].isupper() == True:
                    start_recording = True

        previous_index = index
        previous_letter = letter

    return return_list


#@app.route('/', methods=['GET'])
def main():
    site = 'http://www.ufv.ca/arfiles/includes/201501-timetable-with-changes.htm'
    dest = 'ufv_class_data.html'
    reader = Reader(site, dest, 'cp1252')
    html_data = reader.html

    import html2text
    print(html2text.html2text(html_data))
    #stripped = strip_tags(html_data)
    #entries = ['bob', 'jim']
    #return render_template('show_entries.html', entries=entries)
    #print(pull_info(stripped))
    # html_soup = BeautifulSoup(html_data)
    # store_data_locally(html_soup.pretify(), dest)
    # with open('soup.pk', 'rb') as f:  # TODO REMOVE
    #    html_soup = pickle.load(f)
    # parse_ufv_data(html_soup)


if __name__ == '__main__':
    #app.debug = True
    #app.run(host='192.168.0.3')
    main()