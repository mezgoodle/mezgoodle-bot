import requests
import json
import base64
from getpass import getpass

username = input('Enter your name: ')
password = getpass()
repo = input('Repo: ')
file_ = input('File: ')
path = input('Enter path: ')

content = 'Working GitHub API'
b_content = content.encode('utf-8')
base64_content = base64.b64encode(b_content)
base64_content_str = base64_content.decode('utf-8')

f = {
    'path': path,
    'message': 'Create new file via GitHub API',
    'content': base64_content_str
}

f_resp = requests.put(
                    f'https://api.github.com/repos/{username}/{repo}/contents/{file_}',
                    auth=(username, password),
                    headers={ "Content-Type": "application/json" },
                    data=json.dumps(f)
                )
print(f_resp.json())
