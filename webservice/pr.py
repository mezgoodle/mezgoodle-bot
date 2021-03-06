"""Pull requests trigger"""

import gidgethub.routing

from .utils import get_info, leave_comment
from .consts import NO_ASSOCIATION, LABEL_NAME, BOT_NAME

router = gidgethub.routing.Router()


@router.register('pull_request', action='opened')
async def pr_opened(event, gh, *args, **kwargs):
    """Opened pull request"""
    issue_url = event.data['pull_request']['issue_url']
    labels = event.data['pull_request']['labels']
    username = event.data['sender']['login']
    token = await get_info(event, gh)
    author_association = event.data['pull_request']['author_association']
    if author_association == NO_ASSOCIATION:
        # first time contributor
        msg = f'Thanks for your first contribution @{username}'
    else:
        # seasoned contributor
        msg = f'Welcome back, @{username}. You are the {author_association}.'

    if token is not None:
        await gh.post(
            f'{issue_url}/comments',
            data={'body': msg},
            oauth_token=token['token'],
        )

        # add label
        await gh.patch(
            issue_url,
            data={
                'labels': [LABEL_NAME] + labels,
                'assignees': ['mezgoodle'],
            },
            oauth_token=token['token'],
        )
    else:
        await gh.post(f'{issue_url}/comments')
        await gh.patch(issue_url)


@router.register('pull_request', action='closed')
@router.register('pull_request', action='merged')
async def events_pr(event, gh, *args, **kwargs):
    """Closed or merged pull request"""
    token = await get_info(event, gh)
    created_by = event.data['pull_request']['user']['login']
    issue_comment_url = event.data['pull_request']['issue_url'] + '/comments'
    info = event.data['pull_request']['head']

    if event.data['pull_request']['merged'] and event.data['pull_request']['state'] == 'closed':
        merged_by = event.data['pull_request']['merged_by']['login']
        if created_by == merged_by or merged_by == BOT_NAME:
            thanks_to = f'Thanks @{created_by} for the PR 🌮🎉.'
        else:
            thanks_to = f'Thanks @{created_by} for the PR, and @{merged_by} for merging it 🌮🎉.'
        message = f'{thanks_to}\n🐍🍒⛏🤖 I am not robot! I am not robot!'

        owner = info['user']['login']
        ref = info['ref']
        repo = info['repo']['name']
        url = f'/repos/{owner}/{repo}/git/refs/heads/{ref}'
        if token is not None:
            await leave_comment(gh, issue_comment_url, message, token['token'])
            await gh.delete(url, oauth_token=token['token'],)
        else:  # For tests
            await gh.delete(url)
    else:
        message = f'Okey, @{created_by}, see you next time'
        owner = info['user']['login']
        ref = info['ref']
        repo = info['repo']['name']
        url = f'/repos/{owner}/{repo}/git/refs/heads/{ref}'
        if token is not None:
            await leave_comment(gh, issue_comment_url, message, token['token'])
            await gh.delete(url, oauth_token=token['token'],)
        else:  # For tests
            await gh.delete(url)


@router.register('pull_request', action='labeled')
async def labeled_pr(event, gh, *args, **kwargs):
    """Labeled pull request"""
    token = await get_info(event, gh)
    user = event.data['pull_request']['user']['login']
    sender = event.data['sender']['login']
    issue_comment_url = event.data['pull_request']['issue_url'] + '/comments'
    message = f'Wow! New label! @{sender}, thank you a lot! @{user}, did you see it?!'
    await leave_comment(gh, issue_comment_url, message, token['token'])
