hwparser.py
===========

hwparser.py is a simple python script to parse the HTML source of the PCR PoS
(aka the new HHMS). It requires [Beautiful
Soup](http://www.crummy.com/software/BeautifulSoup/), a python library for
pulling data out of HTML and XML files. To install BS4 with `pip`:
```
pip install beautifulsoup4
```

## Usage
Authenticate, then go to the week you want to parse. Make sure that you are in
weekly view. Save the source of the page. Then, run
```
python hwparser.py /path/to/source.html
```
A file called `out.txt` will be written in the same directory with the date each
assignment is due, the class, and the details of the assignment.
