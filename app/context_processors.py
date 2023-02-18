from aiohttp_session import get_session
from app.google_sheets.models import User



async def get_user(request):
    session = await get_session(request)
    user_id = session.get('user_id')
    if user_id:
        users = await User.query.gino.all()
        for user in users:
            if user.id == user_id:
                return {'request_user': user}
    return {}