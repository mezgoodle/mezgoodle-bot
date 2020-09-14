from gidgethub import sansio

from webservice import installation, consts


class FakeGH:
    async def post(self, url):
        self.post_url = url


async def test_installation():
    data = consts.TEST_DATA_INSTALLATION
    event = sansio.Event(data, event='installation', delivery_id='1')

    gh = FakeGH()
    await installation.router.dispatch(event, gh)
    assert (
        gh.post_url == f'/repos/{consts.BOT_NAME}/issues'
    )
