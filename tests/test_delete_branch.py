from gidgethub import sansio

from webservice import pr, consts


class FakeGH:
    def __init__(self):
        self.post_data = None

    async def delete(self, url):
        self.delete_url = url


async def test_branch_deleted_when_pr_merged():
    data = {
        'action': 'closed',
        'pull_request': {
            'number': consts.test_number,
            'user': {'login': consts.bot_name},
            'merged': True,
            'merged_by': {'login': consts.admin_nickname},
            'head': {
                'ref': consts.test_ref, 'user': {'login': consts.admin_nickname},
                'repo': {'name': consts.test_repo_name}
            },
            'issue_url': consts.issue_url,
            'state': 'closed',
        },
    }
    event = sansio.Event(data, event='pull_request', delivery_id='1')

    gh = FakeGH()
    await pr.router.dispatch(event, gh)
    assert gh.post_data is None  # does not leave a comment
    assert (
        gh.delete_url
        == f'/repos/{consts.admin_nickname}/{consts.test_repo_name}/git/refs/heads/{consts.test_ref}'
    )
