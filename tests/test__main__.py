"""Test bot as app on server"""

from aiohttp import web

from webservice import __main__ as main, consts


async def test_ping(aiohttp_client):
    """Test launch the app"""
    app = web.Application()
    app.router.add_post('/', main.webhook)
    client = await aiohttp_client(app)
    headers = consts.HEADERS
    data = {'zen': 'testing is good'}
    response = await client.post('/', headers=headers, json=data)
    assert response.status == 200


async def test_success(aiohttp_client):
    """Test success action"""
    app = web.Application()
    app.router.add_post('/', main.webhook)
    client = await aiohttp_client(app)
    headers = consts.HEADERS
    # Sending a payload that shouldn't trigger any networking, but no errors
    # either.
    data = {'action': 'created'}
    response = await client.post('/', headers=headers, json=data)
    assert response.status == 200


async def test_failure(aiohttp_client):
    """Test the app without headers"""
    app = web.Application()
    app.router.add_post('/', main.webhook)
    client = await aiohttp_client(app)
    # Missing key headers.
    response = await client.post('/', headers={})
    assert response.status == 500
