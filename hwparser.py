import sys
from bs4 import BeautifulSoup
import re
import argparse
# import urllib2

def simple_parse(filename, output='out.txt'):
    soup = BeautifulSoup(open(filename, 'r').read())
    out = open(output, 'w')
    hw_content_stripped = [tag for tag in
            soup.find_all('div', style =
            'margin: 5px 5px 0px 5px; font-size: 12px; padding-bottom: 10px;')]
    for tag in hw_content_stripped:
        for string in tag.stripped_strings:
            out.write(string.encode('utf-8') + '\n')
        out.write('\n')

def parse(filename, output='out.txt'):
    soup = BeautifulSoup(open(filename, 'r').read())
    out = open(output, 'w')

    hw_dates = [tag.string for tag in
            soup.find_all('span', id = re.compile(r'.*StartingOn$'))]
    hw_titles = [tag.string for tag in
            soup.find_all('span', id = re.compile(r'.*lblTitle$'))]
    hw_content = [tag.get_text().strip() for tag in
            soup.find_all('div', style =
            'margin: 5px 5px 0px 5px; font-size: 12px; padding-bottom: 10px;')]
    hw_due_dates = []
    for date in hw_dates:
        if '- ' in date:
            p = re.compile(r'- ([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})')
            m = p.search(date)
            hw_due_dates.append(m.group(1))
        else:
            p = re.compile(r'^([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})')
            m = p.search(date)
            hw_due_dates.append(m.group(0))
    p = re.compile(r'\n\n\n\n\s*(.*)$')
    hw_info = []
    for content in hw_content:
        m = p.search(content)
        if m != None:
            hw_info.append(m.group(1))
        else:
            hw_info.append('')
    if len(hw_due_dates) != len(hw_titles) or len(hw_due_dates) != len(hw_info):
        raise Exception('lengths don\'t match up')
    for i in range(len(hw_due_dates)):
        out.write(hw_due_dates[i] + ': ' + hw_titles[i] + '\n')
        out.write(hw_info[i].encode('utf-8') + '\n\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='the source html file')
    parser.add_argument('output', help='the output file')
    parser.add_argument('-s', '--simple', help='dump text without sorting',
            action='store_true')
    args = parser.parse_args()
    if args.simple:
        simple_parse(args.filename, args.output)
    else:
        parse(args.filename, args.output)
