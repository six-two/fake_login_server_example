# Fake login server example

This is an example of how to write a server, that communicates with one of my fake login web apps.

## Supported fake logins

- [Kali linux](https://projects.six-two.dev/react_fake_kali_login/)
- [Windows 10](https://projects.six-two.dev/www.google.com)

## Architecture

The server accepts HTTP GET requests.
The path of the request indicates, what type of credentials should be checked.
The credentials that should be checked are passed via the URL search query section.
