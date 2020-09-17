"""Get repositories from GitHub User by API"""
import requests
from getpass import getpass

username = input('Enter your name: ')
password = getpass()

string = 'https://api.github.com/user/repos'

repos = requests.get(string, auth=(username, password))
# print(repos.json()[1])

for repo in repos.json():
    if not repo['private']:
        print(repo['html_url'])
