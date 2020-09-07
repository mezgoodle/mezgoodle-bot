from .utils import get_info, leave_comment
from .mail import send_mail
from .consts import pr_type
import gidgethub.routing

router = gidgethub.routing.Router()


@router.register(pr_type, action="opened")
async def pr_opened(event, gh, *args, **kwargs):
    issue_url = event.data[pr_type]["issue_url"]
    labels = event.data[pr_type]["labels"]
    username = event.data["sender"]["login"]
    sender_url = event.data["sender"]["html_url"]
    title = event.data['issue']['title']
    body = event.data['issue']['body']
    token = await get_info(event, gh)
    author_association = event.data[pr_type]["author_association"]

    # Send mail
    try:
        send_mail(pr_type, title, username, sender_url, issue_url, body)
    except BaseException:
        print('Okay')
    if author_association == 'NONE':
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
            'labels': ['needs review'] + labels,
            'assignees': ['mezgoodle'],
        },
        oauth_token=token["token"],
    )


@router.register(pr_type, action="closed")
@router.register(pr_type, action="merged")
async def events_pr(event, gh, *args, **kwargs):
    token = await get_info(event, gh)
    created_by = event.data[pr_type]["user"]["login"]
    issue_comment_url = event.data[pr_type]["issue_url"] + '/comments'
    info = event.data[pr_type]["head"]

    if event.data[pr_type]["merged"] and event.data[pr_type]["state"] == 'closed':
        merged_by = event.data[pr_type]["merged_by"]["login"]
        if created_by == merged_by or merged_by == "mezgoodle-bot":
            thanks_to = f"Thanks @{created_by} for the PR 🌮🎉."
        else:
            thanks_to = f"Thanks @{created_by} for the PR, and @{merged_by} for merging it 🌮🎉."
        message = f"{thanks_to}\n🐍🍒⛏🤖 I am not robot! I am not robot!"

        await leave_comment(gh, issue_comment_url, message, token["token"])
        owner = info["user"]["login"]
        ref = info["ref"]
        repo = info["repo"]["name"]
        url = f"/repos/{owner}/{repo}/git/refs/heads/{ref}"
        await gh.delete(url, oauth_token=token["token"],)
    else:
        await leave_comment(gh, issue_comment_url, f'Okey, @{created_by}, see you next time', token["token"])
        owner = info["user"]["login"]
        ref = info["ref"]
        repo = info["repo"]["name"]
        url = f"/repos/{owner}/{repo}/git/refs/heads/{ref}"
        await gh.delete(url, oauth_token=token["token"],)


@router.register(pr_type, action="labeled")
async def labeled_pr(event, gh, *args, **kwargs):
    token = await get_info(event, gh)
    user = event.data[pr_type]["user"]["login"]
    sender = event.data["sender"]["login"]
    issue_comment_url = event.data[pr_type]["issue_url"] + '/comments'
    message = f"Wow! New label! @{sender}, thank you a lot! @{user}, did you see it?!"
    await leave_comment(gh, issue_comment_url, message, token["token"])
