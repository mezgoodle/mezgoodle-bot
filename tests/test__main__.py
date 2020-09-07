from aiohttp import web
# import pytest

from webservice import __main__ as main


async def test_ping(aiohttp_client):
    app = web.Application()
    app.router.add_post("/", main.webhook)
    client = await aiohttp_client(app)
    headers = {"x-github-event": "ping",
               "x-github-delivery": "1234"}
    data = {"zen": "testing is good"}
    response = await client.post("/", headers=headers, json=data)
    assert response.status == 200
