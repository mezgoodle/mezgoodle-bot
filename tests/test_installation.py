"""Test installation the bot"""

from gidgethub import sansio

from webservice import installation, consts
from .gh import FakeGH


async def test_installation():
    """Test installation feedback"""
    data = consts.TEST_DATA_INSTALLATION
    event = sansio.Event(data, event='installation', delivery_id='1')

    gh = FakeGH()
    await installation.router.dispatch(event, gh)
    assert (
        gh.post_url == f'/repos/{consts.BOT_NAME}/issues'
    )
