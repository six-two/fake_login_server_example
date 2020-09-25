from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Any, Callable, List
import json
import traceback


class Credentials:
    '''An object containing all parameters contained within the request'''

    def __init__(self, url_params) -> None:
        self.url_params = url_params

    def get(self, arg_name: str) -> str:
        arg = self.getOrDefault(arg_name, '')
        if arg == '':
            raise Exception(f'Missing URL parameter: "{arg_name}"')
        return arg

    def getOrDefault(self, arg_name: str, default: str) -> str:
        try:
            param_list = self.url_params[arg_name]
            n = len(param_list)
            if n != 1:
                print(f'Warning: Parameter "{arg_name}" is supplied {n} times')
            return param_list[0]
        except:
            print(f'Warning: Missing url parameter: "{arg_name}"')
            return default


class CredentialCheckerEntry:
    '''Used by the CredentialChecker'''

    def __init__(self, path: str, fn_check_credentials: Callable[[Credentials], bool]) -> None:
        self.path = path
        self.fn_check_credentials = fn_check_credentials


class CredentialChecker:
    '''Check if the credentials given to it are valid'''

    def __init__(self, credential_checkers: List[CredentialCheckerEntry], default_is_valid: bool = True) -> None:
        '''param default_is_valid: What value to return, when the validity can not be checked'''
        self.default_is_valid = default_is_valid
        self.credential_checkers = credential_checkers

    def isRequestValid(self, request_path: str) -> bool:
        '''Convenience method that extracts all the required information from the "request_path" and then calls "areCredentialsValid"'''
        try:
            parsed = urlparse(request_path)
            args = parse_qs(parsed.query)
            credentials = Credentials(args)

            return self.areCredentialsValid(parsed.path, credentials)
        except:
            traceback.print_exc()
        return self.default_is_valid

    def areCredentialsValid(self, path: str, credentials: Credentials) -> bool:
        '''Checks the credentials and returns a boolean, that indicates if the credential are correct.
        If it encounters an exception it will return the "default_is_valid" value, that it got in the constructor.
        '''
        try:
            for checker in self.credential_checkers:
                if path.endswith(checker.path):
                    return checker.fn_check_credentials(credentials)

            print(f'Error: No handler for path "{path}"')
        except:
            traceback.print_exc()
        return self.default_is_valid


def sendResponseJSON(requestHandler: BaseHTTPRequestHandler, jsonData: Any) -> None:
    '''Send a JSON response with all the necessary headers'''

    replyString = json.dumps(jsonData).encode('utf-8')

    requestHandler.send_response(200)
    requestHandler.send_header('Content-type', 'application/json')
    requestHandler.send_header('Access-Control-Allow-Origin', '*')
    requestHandler.end_headers()
    requestHandler.wfile.write(replyString)

