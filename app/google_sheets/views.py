import aiohttp
import aiohttp_jinja2
from aiohttp.web_exceptions import HTTPFound
from sqlalchemy import select
from sqlalchemy.orm import session
from aiohttp_session import get_session
from app.google_sheets.models import User
import redis
import os
import json
from app.utils import hash_password, Validator, get_credentials_json
from app.google_sheets_writer import GSWriter
red = redis.Redis(host='localhost', port=6379, db=0)


async def get_user_email(request):
   session_id = request.cookies.get('AIOHTTP_SESSION')
   redis_session_id = red.get(session_id)
   if redis_session_id:
      users = await User.query.gino.all()
      for user in users:
         if str(user.id) == redis_session_id.decode():
            return user.email
   return None



@aiohttp_jinja2.template("index.html")
async def index(request):
   return {'kk': os.environ.get('KEY')}


@aiohttp_jinja2.template("sign_in.html")
async def sign_in(request):
   if request.method == 'POST':
      data = await request.post()
      email = data['email']
      password = data['password']
      users = await User.query.gino.all()
      for user in users:
         if user.email == email and user.password == password:
            session = await get_session(request)
            session.update({'user_id': user.id})
            raise HTTPFound('/dashboard/')


async def logout(request):
   session = await get_session(request)
   session.pop('user_id')
   raise HTTPFound('/')


# создаем функцию, которая будет отдавать html-файл
@aiohttp_jinja2.template("dashboard/dashboard_main.html")
async def dashboard(request):
   session = await get_session(request)
   return {'session': session}


@aiohttp_jinja2.template("connection_types.html")
async def connection_types(request):
   return


@aiohttp_jinja2.template("hard_connection_type.html")
async def hard_connection_type(request):
         if request.method == 'POST':
            data = await request.post()
            email = data['email']
            password1 = data['password1']
            password2 = data['password2']
            credentials_dict = json.loads(data['credentials'].file.read().decode())
            data_to_validate = Validator(email, password1, password2, credentials_dict)
            if data_to_validate.is_valid():
               user = await request.app["db"].user.create(
                  email=email,
                  password=password2
               )
               credentials = await request.app['db'].credentials.create(
                  type=credentials_dict['type'],
                  project_id = credentials_dict['project_id'],
                  private_key_id = credentials_dict['private_key_id'],
                  private_key = credentials_dict['private_key'],
                  client_email = credentials_dict['client_email'],
                  client_id = credentials_dict['client_id'],
                  auth_uri = credentials_dict['auth_uri'],
                  token_uri = credentials_dict['token_uri'],
                  auth_provider_x509_cert_url = credentials_dict['auth_provider_x509_cert_url'],
                  client_x509_cert_url = credentials_dict['client_x509_cert_url'],
                  user_id = user.id
               )
               raise HTTPFound('/sign-in/')
            else:
               return {'form_errors': data_to_validate.invalid_fields_errors}


@aiohttp_jinja2.template("dashboard/yandex_metrika.html")
async def metrika(request):
   return


@aiohttp_jinja2.template("dashboard/google_analytics.html")
async def analytics(request):
   return


async def metrila_new_connection(request):
   return


async def analytics_new_connection(request):
   user_credentials = await get_credentials_json(3)
   gs_writer = GSWriter(credentials_file='sample.json', gs_url='https://docs.google.com/spreadsheets/d/1wE7MXeg6pNT37sKQxon0IP8gt1PaqvR7a2sIlAD3aww/edit#gid=0')
   gs_writer.write()
   return


