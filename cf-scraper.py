"""
Usage: 
Activate virtualenv.
Export variables CF_CONTEST_URL, CF_CONTEST_DIR
export CF_CONTEST_URL=<contest-url>
export CF_CONTEST_DIR=`pwd`

Samples
echo 'make' | python cf-scraper.py
echo 'clean' | python cf-scraper.py
"""


import requests
import html5lib
import bs4
import os
import shutil


CF_URL = 'https://codeforces.com'
CONTEST_URL = os.environ['CF_CONTEST_URL']
CF_CONTEST_DIR = os.environ['CF_CONTEST_DIR']
CF_TEST_DIR = CF_CONTEST_DIR+'/'+'Tests'
IN_PREFIX='in'
OUT_PREFIX='out'


def get_testcase(question_id, question_url):
    r = requests.get(question_url)
    bs = bs4.BeautifulSoup(r.content, 'html5lib')
    
    directory = CF_TEST_DIR+'/'+question_id
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for count, div in enumerate(bs.findAll('div', attrs={'class':'input'})):
        test = div.find('pre')
        filename = directory+'/'+IN_PREFIX+str(count+1)
        with open(filename, mode='w') as f:
            f.write(test.get_text().strip())
    
    for count, div in enumerate(bs.findAll('div', attrs={'class':'output'})):
        test = div.find('pre')
        filename = directory+'/'+OUT_PREFIX+str(count+1)
        with open(filename, mode='w') as f:
            f.write(test.get_text().strip())
            
    print("Created Tests For", question_id)
    

def create_tests(): 
    r = requests.get(CONTEST_URL)
    bs = bs4.BeautifulSoup(r.content, 'html5lib')
           
    table = bs.find('table', attrs={'class':'problems'})
    for row in table.findAll('td', attrs={'class':'id'}):
        question_id = row.a.get_text().replace(' ', '').strip()
        question_url = row.a.get('href')
        
        get_testcase(question_id, CF_URL+question_url)
    
    print("Done")


def remove_tests():
    shutil.rmtree(CF_TEST_DIR)
        
    print("Deleted Tests")
    

if __name__ == '__main__':
    what_to_do = input()
    
    print("Contest URL", CONTEST_URL)
    print("Contest Directory", CF_CONTEST_DIR)
    
    if what_to_do == 'make':
        create_tests()
    elif what_to_do == 'clean':
        remove_tests()
    else:
        print("Valid arguments are make or clean")
