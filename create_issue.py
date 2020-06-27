import asyncio
import os
import aiohttp
from gidgethub.aiohttp import GitHubAPI


async def main():
    async with aiohttp.ClientSession() as session:
        gh = GitHubAPI(
            session,
            "mezgoodle",
            oauth_token=os.getenv("GH_AUTH")
        )
        response = await gh.post(
            '/repos/mezgoodle/hello-github-actions/issues/7/comments',
            data={
                'body': 'I did!',
            }
        )
        print(f"Issue created at {response['html_url']}")


asyncio.run(main())