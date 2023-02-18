from aiohttp import web
from aiohttp_session import get_session
from app.google_sheets.models import User
import aiohttp
import redis

red = redis.Redis(host='localhost', port=6379, db=0)




@web.middleware
async def middleware1(request, handler):


    response = await handler(request)
    return response


async def request_user_middleware(app, handler):
    async def middleware(request):
        session = await get_session(request)
        request.user = None
        user_id = session.get('user_id')
        if user_id is not None:
            request.user = await request.app.objects.get(User, id=user_id)
        return await handler(request)
    return middleware

