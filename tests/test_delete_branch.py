from gidgethub import sansio

from webservice import pr, consts


class FakeGH:
    def __init__(self):
        self.post_data = None

    async def delete(self, url):
        self.delete_url = url

    async def post(self, url):
        self.post_url = url

    async def patch(self, url):
        self.patch_url = url


async def test_pr_opened():
    data = consts.test_data
    event = sansio.Event(data, event='pull_request', delivery_id='1')

    gh = FakeGH()
    await pr.router.dispatch(event, gh)
    assert (
        gh.post_url == f'{consts.issue_url}/comments'
    )
    assert (
        gh.patch_url == consts.issue_url
    )


async def test_branch_deleted_when_pr_merged():
    data = consts.test_data_1
    event = sansio.Event(data, event='pull_request', delivery_id='1')

    gh = FakeGH()
    await pr.router.dispatch(event, gh)
    assert gh.post_data is None  # does not leave a comment
    assert (
        gh.delete_url
        == f'/repos/{consts.admin_nickname}/{consts.test_repo_name}/git/refs/heads/{consts.test_ref}'
    )


async def test_branch_deleted_when_pr_closed():
    data = consts.test_data_2
    event = sansio.Event(data, event='pull_request', delivery_id='1')

    gh = FakeGH()
    await pr.router.dispatch(event, gh)
    assert gh.post_data is None  # does not leave a comment
    assert (
        gh.delete_url
        == f'/repos/{consts.admin_nickname}/{consts.test_repo_name}/git/refs/heads/{consts.test_ref}'
    )
