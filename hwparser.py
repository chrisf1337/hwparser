from bs4 import BeautifulSoup
import re
import argparse
import datetime
from operator import itemgetter
# import urllib2

class Assignment:
    def __init__(self, date, header, content):
        self.date = date
        self.header = header
        self.content = content
    def __repr__(self):
        return self.date.strftime('%m/%d/%Y') + ' ' + self.header

def parse(filename, output='out.txt'):
    soup = BeautifulSoup(open(filename, 'r').read())
    # get all homework content, which is contained in div tags with the given
    # style
    hw_content_stripped = [tag for tag in
            soup.find_all('div', style =
            'margin: 5px 5px 0px 5px; font-size: 12px; padding-bottom: 10px;')]
    hw_content = []
    # get all homework text and fixes whitespace issues with <br> tags
    for tag in hw_content_stripped:
        assignment = []
        for string in tag.stripped_strings:
            assignment.append(string)
        hw_content.append(assignment)
    # extract all due date strings and convert to datetime.date objects
    for assignment in hw_content:
        # if the assignment has both assigned and due dates, extract due date
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
    # sort assignments by date
    hw_content.sort(key=itemgetter(0))
    # convert all assignment lists to assignment objects
    for i in range(len(hw_content)):
        hw_content[i] = Assignment(hw_content[i][0], hw_content[i][1],
                hw_content[i][2:])
    # write assignments to output file
    with open(output, 'w') as out:
        for assignment in hw_content:
            out.write(assignment.date.strftime('%m/%d/%Y') + '\n')
            out.write(assignment.header + '\n')
            for line in assignment.content:
                out.write(line.encode('utf-8') + '\n')
            out.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='the source html file')
    parser.add_argument('output', help='the output file')
    args = parser.parse_args()
    parse(args.filename, args.output)
