import requests
import base64
from getpass import getpass

username = input('Enter your name: ')
password = getpass()

repo = input('Repo: ')
# If you want only readme file
# GET /repos/:owner/:repo/readme
# If you want other file
# file_path = input('Enter path to file: ')
file_path = 'README.md'

string = f'https://api.github.com/repos/{username}/{repo}/contents/{file_path}'

file_response = requests.get(string)

file_bytes = base64.b64decode(file_response.json()['content'])
file_str = file_bytes.decode('utf-8')
print(file_str)
