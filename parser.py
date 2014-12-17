import urllib2
import re


def main():
    response = urllib2.urlopen('http://www.ufv.ca/arfiles/includes/201501-timetable-with-changes.htm')
    html = response.read()

    with open("ufv_class_data.html", "w+") as f:
        f.write(html)

    print len(html.split('-' * 132))


if __name__ == '__main__':
    main()