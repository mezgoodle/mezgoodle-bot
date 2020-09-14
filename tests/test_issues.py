from gidgethub import sansio

from webservice import issues, consts


class FakeGH:
    async def post(self, url):
        self.post_url = url


async def test_issue_opened():
    data = consts.test_data_installation
    event = sansio.Event(data, event='issue_comment', delivery_id='1')

    gh = FakeGH()
    await issues.router.dispatch(event, gh)
    assert (
        gh.post_url == f'{consts.issue_url}/reactions'
    )
