import asyncio
import os
import sys
import traceback


import aiohttp
from aiohttp import web
import cachetools
from gidgethub import aiohttp as gh_aiohttp
from gidgethub import routing
from gidgethub import sansio
from gidgethub import apps

router = routing.Router()
cache = cachetools.LRUCache(maxsize=500)

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
    token = await get_info(event, gh)
    sender_name = event.data["sender"]["login"]
    for repo in event.data["repositories"]:

        repo_full_name = repo["full_name"]
        response = await gh.post(
            f'/repos/{repo_full_name}/issues',
            data={
                'title': 'Thanks for installing me!',
                'body': f'You are the best! @{sender_name}\n Also my creator is @mezgoodle. There you can find my body)'
            },
            oauth_token=token["token"],
        )
        issue_url = response["url"]
        await gh.patch(issue_url,
                       data={"state": "closed"},
                       oauth_token=token["token"],
                       )


@router.register("pull_request", action="opened")
async def pr_opened(event, gh, *args, **kwargs):
    issue_url = event.data["pull_request"]["issue_url"]
    labels = event.data["pull_request"]["labels"]
    username = event.data["sender"]["login"]
    token = await get_info(event, gh)
    author_association = event.data["pull_request"]["author_association"]
    if author_association == 'NONE':
        # first time contributor
        msg = f'Thanks for your first contribution @{username}'
    else:
        # seasoned contributor
        msg = f'Welcome back, @{username}. You are the {author_association}.'
    response = await gh.post(f'{issue_url}/comments',
                             data={'body': msg},
                             oauth_token=token["token"],
                             )
    print(response)

    # add label
    response = await gh.patch(
        issue_url,
        data={
            'labels': ['needs review'] + labels,
            'assignees': ['mezgoodle'],
        },
        oauth_token=token["token"],
    )
    print(response)


@router.register("pull_request", action="closed")
@router.register("pull_request", action="merged")
async def events_pr(event, gh, *args, **kwargs):
    token = await get_info(event, gh)
    created_by = event.data["pull_request"]["user"]["login"]
    issue_comment_url = event.data["pull_request"]["issue_url"] + '/comments'
    info = event.data["pull_request"]["head"]

    if event.data["pull_request"]["merged"] and event.data["pull_request"]["state"] == 'closed':
        merged_by = event.data["pull_request"]["merged_by"]["login"]
        if created_by == merged_by or merged_by == "mezgoodle-bot":
            thanks_to = f"Thanks @{created_by} for the PR 🌮🎉."
        else:
            thanks_to = f"Thanks @{created_by} for the PR, and @{merged_by} for merging it 🌮🎉."
        message = f"{thanks_to}\n🐍🍒⛏🤖 I am not robot! I am not robot!"

        await leave_comment(gh, issue_comment_url, message, token["token"])
        response = await gh.delete(
            f'{info["repo"]["url"]}/git/refs/{info["ref"]}',
            oauth_token=token["token"],
        )
        print(response)
    else:
        await leave_comment(gh, issue_comment_url, f'Okey, @{created_by}, see you next time', token["token"])
        response = await gh.delete(
            f'{info["repo"]["url"]}/git/refs/{info["ref"]}',
            oauth_token=token["token"],
        )
        print(response)
    


@router.register("pull_request", action="labeled")
async def labeled_pr(event, gh, *args, **kwargs):
    token = await get_info(event, gh)
    user = event.data["pull_request"]["user"]["login"]
    issue_comment_url = event.data["pull_request"]["issue_url"] + '/comments'
    message = f"Wow! New label. @{user}, did you see it?!"
    await leave_comment(gh, issue_comment_url, message, token["token"])


@router.register("issue_comment", action="created")
async def issue_comment_created(event, gh, *args, **kwargs):
    username = event.data["sender"]["login"]
    token = await get_info(event, gh)
    comments_url = event.data["comment"]["url"]
    if username == "mezgoodle":
        response = await gh.post(
            f'{comments_url}/reactions',
            data={'content': 'heart'},
            oauth_token=token["token"],
            accept='application/vnd.github.squirrel-girl-preview+json'
        )
        print(response)


async def get_info(event, gh):
    installation_id = event.data["installation"]["id"]
    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("GH_APP_ID"),
        private_key=os.environ.get("GH_PRIVATE_KEY")
    )
    return installation_access_token


async def leave_comment(gh, issue_comment_url, message, token):
    data = {"body": message}
    await gh.post(
        f'{issue_comment_url}', 
        data=data, 
        oauth_token=token
    )


if __name__ == "__main__":  # pragma: no cover
    app = web.Application()

    app.router.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)
    web.run_app(app, port=port)
