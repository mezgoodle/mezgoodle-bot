"""Test issues"""

from gidgethub import sansio

from webservice import issues, consts
from .gh import FakeGH


async def test_issue_opened():
    """Test issue comment creation"""
    data = consts.TEST_DATA_ISSUES
    event = sansio.Event(data, event='issue_comment', delivery_id='1')

    gh = FakeGH()
    await issues.router.dispatch(event, gh)
    assert (
        gh.post_url == f'{consts.ISSUE_URL}/reactions'
    )
