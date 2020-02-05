import requests, sys
from bs4 import BeautifulSoup

wfp2_site = sys.argv[1]

url = f'''http://{wfp2_site}/mongodb/example2/?search=admin'''

resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')

if ('admin' in soup.find('table').getText()):
    print("admin found")
else:
    print("admin not found")