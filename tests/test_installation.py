from gidgethub import sansio

from webservice import installation, consts


class FakeGH:
    async def post(self, url):
        self.post_url = url


async def test_installation():
    data = consts.test_data_installation
    event = sansio.Event(data, event='installation', delivery_id='1')

    gh = FakeGH()
    await installation.router.dispatch(event, gh)
    assert (
        gh.post_url == f'/repos/{consts.bot_name}/issues'
    )
