import asyncio
import os
import sys
import traceback
import random


import aiohttp
from aiohttp import web
import cachetools
from gidgethub import aiohttp as gh_aiohttp
from gidgethub import routing
from gidgethub import sansio
from gidgethub import apps

router = routing.Router()
cache = cachetools.LRUCache(maxsize=500)
EASTER_EGG = "I'm not a robot! I'm not a robot!"

routes = web.RouteTableDef()


@routes.get("/", name="home")
async def handle_get(request):
    return web.Response(text="Hello world")


@routes.post("/webhook")
async def webhook(request):
    try:
        body = await request.read()
        secret = os.environ.get("GH_SECRET")
        event = sansio.Event.from_http(request.headers, body, secret=secret)
        if event.event == "ping":
            return web.Response(status=200)
        async with aiohttp.ClientSession() as session:
            gh = gh_aiohttp.GitHubAPI(session, "demo", cache=cache)

            await asyncio.sleep(1)
            await router.dispatch(event, gh)
        try:
            print("GH requests remaining:", gh.rate_limit.remaining)
        except AttributeError:
            pass
        return web.Response(status=200)
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
        print(exc)
        return web.Response(status=500)


@router.register("installation", action="created")
async def repo_installation_added(event, gh, *args, **kwargs):
    installation_id = event.data["installation"]["id"]
    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("GH_APP_ID"),
        private_key=os.environ.get("GH_PRIVATE_KEY")
    )
    sender_name = event.data["sender"]["login"]
    for repo in event.data["repositories"]:

        repo_full_name = repo["full_name"]
        response = await gh.post(
            f'/repos/{repo_full_name}/issues',
            data={
                'title': 'Thanks for installing me!',
                'body': f'You are the best! @{sender_name}\n Also my creator is @mezgoodle. There you can find my body)'
            },
            oauth_token=installation_access_token["token"],
        )
        issue_url = response["url"]
        await gh.patch(issue_url,
                       data={"state": "closed"},
                       oauth_token=installation_access_token["token"],
                       )


@router.register("pull_request", action="opened")
async def pr_opened(event, gh, *args, **kwargs):
    issue_url = event.data["pull_request"]["issue_url"]
    labels = event.data["pull_request"]["labels"]
    username = event.data["sender"]["login"]
    installation_id = event.data["installation"]["id"]
    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("GH_APP_ID"),
        private_key=os.environ.get("GH_PRIVATE_KEY")
    )
    author_association = event.data["pull_request"]["author_association"]
    if author_association == 'NONE':
        # first time contributor
        msg = f'Thanks for your first contribution @{username}'
    else:
        # seasoned contributor
        msg = f'Welcome back, @{username}. You are the {author_association}.'
    response = await gh.post(f'{issue_url}/comments',
                             data={'body': msg},
                             oauth_token=installation_access_token["token"],
                             )
    print(response)

    # add label
    response = await gh.patch(
        issue_url,
        data={
            'labels': ['needs review'] + labels,
            'assignees': ['mezgoodle'],
        },
        oauth_token=installation_access_token["token"],
    )
    print(response)


@router.register("pull_request", action="closed")
@router.register("pull_request", action="labeled")
async def backport_pr(event, gh, *args, **kwargs):
    if event.data["pull_request"]["merged"]:

        merged_by = event.data["pull_request"]["merged_by"]["login"]
        created_by = event.data["pull_request"]["user"]["login"]
        issue_comment_url = event.data["pull_request"]["issue_url"]

        pr_labels = []
        if event.data["action"] == "labeled":
            pr_labels = [event.data["label"]]
        else:
            gh_issue = await gh.getitem(
                event.data["repository"]["issues_url"],
                {"number": f"{event.data['pull_request']['number']}"},
            )
            pr_labels = await gh.getitem(gh_issue["labels_url"])

        branches = [
            label["name"].split()[-1]
            for label in pr_labels
            if label["name"].startswith("needs backport to")
        ]

        if branches:
            easter_egg = ""
            if random.random() < 0.1:
                easter_egg = EASTER_EGG
            thanks_to = ""
            if created_by == merged_by or merged_by == "mezgoodle-bot":
                thanks_to = f"Thanks @{created_by} for the PR 🌮🎉."
            else:
                thanks_to = f"Thanks @{created_by} for the PR, and @{merged_by} for merging it 🌮🎉."
            message = (
                f"{thanks_to}. I'm working now to backport this PR to: {', '.join(branches)}."
                f"\n🐍🍒⛏🤖 {easter_egg}"
            )

            await leave_comment(gh, issue_comment_url, message)


async def leave_comment(gh, issue_comment_url, message):
    data = {"body": message}
    await gh.post(f'{issue_comment_url}/comments', data=data)


@router.register("issue_comment", action="created")
async def issue_comment_created(event, gh, *args, **kwargs):
    username = event.data["sender"]["login"]
    installation_id = event.data["installation"]["id"]
    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("GH_APP_ID"),
        private_key=os.environ.get("GH_PRIVATE_KEY")
    )
    comments_url = event.data["comment"]["url"]
    if username == "mezgoodle":
        response = await gh.post(
            f'{comments_url}/reactions',
            data={'content': 'heart'},
            oauth_token=installation_access_token["token"],
            accept='application/vnd.github.squirrel-girl-preview+json'
        )
        print(response)


if __name__ == "__main__":  # pragma: no cover
    app = web.Application()

    app.router.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)
    web.run_app(app, port=port)
