"""Test installation the bot"""

from gidgethub import sansio

from webservice import installation, consts


class FakeGH:
	"""Create fake GitHub object"""
	def __init__(self):
		self.post_data = None

	async def post(self, url):
		"""Trigger post method"""
		self.post_url = url


async def test_installation():
	"""Test installation feedback"""
	data = consts.TEST_DATA_INSTALLATION
	event = sansio.Event(data, event='installation', delivery_id='1')

	gh = FakeGH()
	await installation.router.dispatch(event, gh)
	assert (
	    gh.post_url == f'/repos/{consts.BOT_NAME}/issues'
	)
