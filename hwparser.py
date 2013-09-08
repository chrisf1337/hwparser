import sys
from bs4 import BeautifulSoup
import re
import argparse
import datetime
from operator import itemgetter
# import urllib2

def parse(filename, output='out.txt'):
    soup = BeautifulSoup(open(filename, 'r').read())
    out = open(output, 'w')
    hw_content_stripped = [tag for tag in
            soup.find_all('div', style =
            'margin: 5px 5px 0px 5px; font-size: 12px; padding-bottom: 10px;')]
    hw_content = []
    for tag in hw_content_stripped:
        assignment = []
        for string in tag.stripped_strings:
            assignment.append(string)
        hw_content.append(assignment)
    for assignment in hw_content:
        if '- ' in assignment[0]:
            p = re.compile(r'- ([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})')
            m = p.search(assignment[0])
            assignment[0] = datetime.date(int(m.group(3)), int(m.group(1)),
                    int(m.group(2)))
        else:
            p = re.compile(r'^([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})')
            m = p.search(assignment[0])
            assignment[0] = datetime.date(int(m.group(3)), int(m.group(1)),
                    int(m.group(2)))
    hw_content.sort(key=itemgetter(0))
    for assignment in hw_content:
        assignment[0] = assignment[0].strftime('%m/%d/%Y')
    for hw in hw_content:
        for string in hw:
            out.write(string.encode('utf-8') + '\n')
        out.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='the source html file')
    parser.add_argument('output', help='the output file')
    args = parser.parse_args()
    parse(args.filename, args.output)
