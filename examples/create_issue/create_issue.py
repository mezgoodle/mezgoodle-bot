import os
import aiohttp
from gidgethub.aiohttp import GitHubAPI


async def main(nickname, repo):
    async with aiohttp.ClientSession() as session:
        gh = GitHubAPI(
            session,
            nickname,
            oauth_token=os.getenv("GH_AUTH")
        )
        response = await gh.post(
            f'/repos/{nickname}/{repo}/issues',
            data={
                'title': 'We got a problem',
                'body': 'Use more emoji!',
            }
        )
        print(f"Issue created at {response['html_url']}")
