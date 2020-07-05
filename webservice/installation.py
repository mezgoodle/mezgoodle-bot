from .utils import get_info
import gidgethub.routing

router = gidgethub.routing.Router()


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
