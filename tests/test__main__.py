from aiohttp import web, client
import pytest

from webservice import __main__ as main


async def test_ping(client):
    app = web.Application()
    app.router.add_post("/", main.main)
    client = await client(app)
    headers = {"x-github-event": "ping",
               "x-github-delivery": "1234"}
    data = {"zen": "testing is good"}
    response = await client.post("/", headers=headers, json=data)
    assert response.status == 200
