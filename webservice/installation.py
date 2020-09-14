"""Main file of the bot"""

import gidgethub.routing

from .utils import get_info

router = gidgethub.routing.Router()


@router.register('installation', action='created')
async def repo_installation_added(event, gh, *args, **kwargs):
    """Installed bot to repository"""
    token = await get_info(event, gh)
    sender_name = event.data['sender']['login']
    for repo in event.data['repositories']:

        repo_full_name = repo['full_name']
        if token:
            response = await gh.post(
                f'/repos/{repo_full_name}/issues',
                data={
                    'title': 'Thanks for installing me!',
                    'body': f'You are the best! @{sender_name}\n Also my creator is @mezgoodle. \
                    There you can find my body)'
                },
                oauth_token=token['token'],
            )
            issue_url = response['url']
            await gh.patch(
                issue_url,
                data={'state': 'closed'},
                oauth_token=token['token'],
            )
        else:
            await gh.post(f'/repos/{repo_full_name}/issues')
