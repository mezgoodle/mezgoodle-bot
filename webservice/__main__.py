"""Main file of the bot"""

import asyncio
import os
import sys
import traceback


import aiohttp
from aiohttp import web
import cachetools
from gidgethub import aiohttp as gh_aiohttp
from gidgethub import routing
from gidgethub import sansio
from .config import SECRET
from . import issues
from . import pr
from . import installation

router = routing.Router(issues.router, pr.router, installation.router)
cache = cachetools.LRUCache(maxsize=500)

routes = web.RouteTableDef()


@routes.get('/', name='home')
async def handle_get(request):
    """Just check if server is running"""
    return web.Response(text='Hello world')


@routes.post('/webhook')
async def webhook(request):
    """Work with webhooks and start the bot"""
    try:
        body = await request.read()
        secret = SECRET
        event = sansio.Event.from_http(request.headers, body, secret=secret)
        if event.event == 'ping':
            return web.Response(status=200)
        async with aiohttp.ClientSession() as session:
            gh = gh_aiohttp.GitHubAPI(session, 'demo', cache=cache)

            await asyncio.sleep(1)
            await router.dispatch(event, gh)
        try:
            print('GH requests remaining:', gh.rate_limit.remaining)
        except AttributeError:
            pass
        return web.Response(status=200)
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
        print(exc)
        return web.Response(status=500)


if __name__ == '__main__':
    app = web.Application()

    app.router.add_routes(routes)
    port = os.environ.get('PORT')
    if port is not None:
        port = int(port)
    web.run_app(app, port=port)
