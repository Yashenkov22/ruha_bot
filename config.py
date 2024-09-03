import os

from sqlalchemy.engine import URL

from dotenv import load_dotenv


load_dotenv()

#Tg bot
TOKEN_API = os.environ.get('TOKEN_API')
ADMIN_IDS = set(map(int ,os.environ.get('ADMIN_IDS').split()))
PROMO_ID = os.environ.get('PROMO_ID')

#Database
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')


db_url = URL.create(
        'postgresql+asyncpg',
        username=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

#Ngrok
PUBLIC_URL = os.environ.get('PUBLIC_URL')

#Redis
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')