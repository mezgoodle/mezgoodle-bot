from aiohttp import web, client
import pytest

from webservice import __main__ as main


async def test_ping():
    app = web.Application()
    app.router.add_post("/", main.main)
    client_ = await client(app)
    headers = {"x-github-event": "ping",
               "x-github-delivery": "1234"}
    data = {"zen": "testing is good"}
    response = await client_.post("/", headers=headers, json=data)
    assert response.status == 200


async def test_success():
    app = web.Application()
    app.router.add_post("/", main.main)
    client_ = await client(app)
    headers = {"x-github-event": "project",
               "x-github-delivery": "1234"}
    # Sending a payload that shouldn't trigger any networking, but no errors
    # either.
    data = {"action": "created"}
    response = await client_.post("/", headers=headers, json=data)
    assert response.status == 200


async def test_failure():
    """Even in the face of an exception, the server should not crash."""
    app = web.Application()
    app.router.add_post("/", main.main)
    client_ = await client(app)
    # Missing key headers.
    response = await client_.post("/", headers={})
    assert response.status == 500