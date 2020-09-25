#!/usr/bin/env python3

from simple_server import Credentials, CredentialChecker, CredentialCheckerEntry, sendResponseJSON
from http.server import BaseHTTPRequestHandler, HTTPServer

USERNAME_PARAM = 'u'
PASSWORD_PARAM = 'p'


def isValidDiskPassword(creds: Credentials):
    password = creds.get(PASSWORD_PARAM)
    if not password:
        return False
    return password == 'ok'


def isValidLogin(creds: Credentials):
    username = creds.get(USERNAME_PARAM)
    password = creds.get(PASSWORD_PARAM)

    print('Attempted login as "{}" with password "{}"'.format(username, password))
    if not username or not password:
        return False
    if username == 'a':
        return True
    if 'o' in password:
        return True
    return False


CHECKER = CredentialChecker([
    CredentialCheckerEntry('/disk.json', isValidDiskPassword),
    CredentialCheckerEntry('/login.json', isValidLogin),
])


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        isValid = CHECKER.isRequestValid(self.path)
        response = {'isValid': isValid}
        print(f'Sending response: {response}')
        sendResponseJSON(self, response)


def run(host: str, port: int, server_class=HTTPServer):
    host = 'localhost'
    httpd = server_class((host, port), MyHandler)
    print(f'Server listening at http://{host}:{port}')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down...')


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 1:
        run('localhost', 3333)
    elif len(argv) == 3:
        _, host, port = argv
        run(host, int(port))
    else:
        print('Usage: [<hostname> <port>]')
