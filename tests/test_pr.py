"""Test pull requests"""

from gidgethub import sansio

from webservice import pr, consts


class FakeGH:
    """Create fake GitHub object"""

    def __init__(self):
        self.post_data = None
        self.delete_url = None
        self.post_url = None
        self.patch_url = None

    async def delete(self, url):
        """Trigger delete method"""
        self.delete_url = url

    async def post(self, url):
        """Trigger post method"""
        self.post_url = url

    async def patch(self, url):
        """Trigger patch method"""
        self.patch_url = url


async def test_pr_opened():
    """Test opened pull request"""
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
    """Test merged pull request"""
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
    """Test closed pull request"""
    data = consts.TEST_DATA_PR_2
    event = sansio.Event(data, event='pull_request', delivery_id='1')

    gh = FakeGH()
    await pr.router.dispatch(event, gh)
    assert gh.post_data is None  # does not leave a comment
    assert (
        gh.delete_url
        == f'/repos/{consts.ADMIN_NICKNAME}/{consts.TEST_REPO_NAME}/git/refs/heads/{consts.TEST_REF}'
    )
