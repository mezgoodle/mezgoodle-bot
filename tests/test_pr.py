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
    data = consts.TEST_DATA_PR
    event = sansio.Event(data, event='pull_request', delivery_id='1')

    gh = FakeGH()
    await pr.router.dispatch(event, gh)
    assert (
        gh.post_url == f'{consts.ISSUE_URL}/comments'
    )
    assert (
        gh.patch_url == consts.ISSUE_URL
    )


async def test_branch_deleted_when_pr_merged():
    data = consts.TEST_DATA_PR_1
    event = sansio.Event(data, event='pull_request', delivery_id='1')

    gh = FakeGH()
    await pr.router.dispatch(event, gh)
    assert gh.post_data is None  # does not leave a comment
    assert (
        gh.delete_url
        == f'/repos/{consts.ADMIN_NICKNAME}/{consts.TEST_REPO_NAME}/git/refs/heads/{consts.TEST_REF}'
    )


async def test_branch_deleted_when_pr_closed():
    data = consts.TEST_DATA_PR_2
    event = sansio.Event(data, event='pull_request', delivery_id='1')

    gh = FakeGH()
    await pr.router.dispatch(event, gh)
    assert gh.post_data is None  # does not leave a comment
    assert (
        gh.delete_url
        == f'/repos/{consts.ADMIN_NICKNAME}/{consts.TEST_REPO_NAME}/git/refs/heads/{consts.TEST_REF}'
    )
