from gidgethub import apps
from .config import PRIVATE_KEY, APP_ID


async def get_info(event, gh):
    if hasattr(event.data, 'installation'):
        installation_id = event.data["installation"]["id"]
        installation_access_token = await apps.get_installation_access_token(
            gh,
            installation_id=installation_id,
            app_id=APP_ID,
            private_key=PRIVATE_KEY
        )
        return installation_access_token
    else:
        return None # For testing


async def leave_comment(gh, issue_comment_url, message, token):
    if token:
        data = {"body": message}
        await gh.post(
            f'{issue_comment_url}',
            data=data,
            oauth_token=token
        )
    else:
        pass # For testing
