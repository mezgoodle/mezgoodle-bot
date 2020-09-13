from .utils import get_info, leave_comment
from .consts import no_association, label_name, bot_name
import gidgethub.routing

router = gidgethub.routing.Router()


@router.register("pull_request", action="opened")
async def pr_opened(event, gh, *args, **kwargs):
    issue_url = event.data["pull_request"]["issue_url"]
    labels = event.data["pull_request"]["labels"]
    username = event.data["sender"]["login"]
    token = await get_info(event, gh)
    author_association = event.data["pull_request"]["author_association"]
    if author_association == no_association:
        # first time contributor
        msg = f'Thanks for your first contribution @{username}'
    else:
        # seasoned contributor
        msg = f'Welcome back, @{username}. You are the {author_association}.'
    await gh.post(
                f'{issue_url}/comments',
                data={'body': msg},
                oauth_token=token["token"],
                )

    # add label
    await gh.patch(
        issue_url,
        data={
            'labels': [label_name] + labels,
            'assignees': ['mezgoodle'],
        },
        oauth_token=token["token"],
    )


@router.register("pull_request", action="closed")
@router.register("pull_request", action="merged")
async def events_pr(event, gh, *args, **kwargs):
    #token = await get_info(event, gh)
    created_by = event.data["pull_request"]["user"]["login"]
    issue_comment_url = event.data["pull_request"]["issue_url"] + '/comments'
    info = event.data["pull_request"]["head"]

    if event.data["pull_request"]["merged"] and event.data["pull_request"]["state"] == 'closed':
        merged_by = event.data["pull_request"]["merged_by"]["login"]
        if created_by == merged_by or merged_by == bot_name:
            thanks_to = f"Thanks @{created_by} for the PR 🌮🎉."
        else:
            thanks_to = f"Thanks @{created_by} for the PR, and @{merged_by} for merging it 🌮🎉."
        message = f"{thanks_to}\n🐍🍒⛏🤖 I am not robot! I am not robot!"

        #await leave_comment(gh, issue_comment_url, message, token["token"])
        owner = info["user"]["login"]
        ref = info["ref"]
        repo = info["repo"]["name"]
        url = f"/repos/{owner}/{repo}/git/refs/heads/{ref}"
        await gh.delete(url)
    else:
        #await leave_comment(gh, issue_comment_url, f'Okey, @{created_by}, see you next time', token["token"])
        owner = info["user"]["login"]
        ref = info["ref"]
        repo = info["repo"]["name"]
        url = f"/repos/{owner}/{repo}/git/refs/heads/{ref}"
        await gh.delete(url)


@router.register("pull_request", action="labeled")
async def labeled_pr(event, gh, *args, **kwargs):
    token = await get_info(event, gh)
    user = event.data["pull_request"]["user"]["login"]
    sender = event.data["sender"]["login"]
    issue_comment_url = event.data["pull_request"]["issue_url"] + '/comments'
    message = f"Wow! New label! @{sender}, thank you a lot! @{user}, did you see it?!"
    await leave_comment(gh, issue_comment_url, message, token["token"])
