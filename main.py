import os
import pathlib

import jinja2  # шаблонизатор jinja2
import aiohttp_jinja2  # адаптация jinja2 к aiohttp
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiopg import create_pool

from app.settings import config
from app.store.database.accessor import PostgresAccessor
import aioredis
from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
from app.middleware import middleware1, request_user_middleware
from app.context_processors import get_user
import dotenv
BASE_DIR = pathlib.Path().absolute()
dotenv_file = os.path.join(BASE_DIR, ".env")


from aiohttp import web


def setup_config(app):
   app["config"] = config

def setup_accessors(app):
   app['db'] = PostgresAccessor()
   app['db'].setup(app)

# в этой функции производится настройка url-путей для всего приложения
def setup_routes(app):
   from app.google_sheets.routes import setup_routes as setup_forum_routes
   setup_forum_routes(app)  # настраиваем url-пути приложения forum

def setup_external_libraries(app: web.Application) -> None:
   # указываем шаблонизатору, что html-шаблоны надо искать в папке templates
   aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("templates"), context_processors=[get_user])



def setup_app(app):
   # настройка всего приложения состоит из:
   dotenv.load_dotenv(dotenv_file)
   setup_accessors(app)
   setup_config(app)
   setup_external_libraries(app)  # настройки внешних библиотек, например шаблонизатора
   setup_routes(app)  # настройки роутера приложения


app = web.Application(middlewares=[

   session_middleware(EncryptedCookieStorage(b'Thirty  two  length  bytes  key.')),
])  # создаем наш веб-сервер

if __name__ == "__main__":  # эта строчка указывает, что данный файл можно запустить как скрипт
   setup_app(app)  # настраиваем приложение
   web.run_app(app, port=config["common"]["port"])  # запускаем приложение