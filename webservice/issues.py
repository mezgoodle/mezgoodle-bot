"""Issues trigger"""

import gidgethub.routing

from .utils import get_info, leave_comment
from .consts import ADMIN_NICKNAME

router = gidgethub.routing.Router()


@router.register('issues', action='labeled')
async def labeled_issue(event, gh, *args, **kwargs):
    """Labeled issue"""
    token = await get_info(event, gh)
    url = event.data['issue']['comments_url']
    sender = event.data['sender']['login']
    message = f'Wow! New label! @{sender}, thank you!'
    await leave_comment(gh, url, message, token['token'])


@router.register('issue_comment', action='created')
async def issue_comment_created(event, gh, *args, **kwargs):
    """Created issue comment"""
    username = event.data['sender']['login']
    token = await get_info(event, gh)
    comments_url = event.data['comment']['url']
    if username == ADMIN_NICKNAME:
        if token:
            await gh.post(
                f'{comments_url}/reactions',
                data={'content': 'heart'},
                oauth_token=token['token'],
                accept='application/vnd.github.squirrel-girl-preview+json'
            )
        else:
            await gh.post(f'{comments_url}/reactions')


@router.register('issues', action='opened')
async def issue_created(event, gh, *args, **kwargs):
    """Opened issue"""
    token = await get_info(event, gh)
    url = event.data['issue']['comments_url']
    sender = event.data['sender']['login']

    if sender == ADMIN_NICKNAME:
        msg = 'Nice to meet you here, sensei!'
    else:
        msg = f'Nice to meet you, @{sender}\nI wish you have a nice \
        day😊\n@mezgoodle will answer as soon as he can.'

    await leave_comment(gh, url, msg, token['token'])


@router.register('issues', action='closed')
async def issue_closed(event, gh, *args, **kwargs):
    """Opened issue"""
    token = await get_info(event, gh)
    url = event.data['issue']['comments_url']
    author = event.data['issue']['user']['login']
    sender = event.data['sender']['login']

    msg = f'Thanks for issue, @{author}! @{sender}, thank \
    you for closing this issue, I have less work. \
    I will look forward to our next meeting😜'

    await leave_comment(gh, url, msg, token['token'])
