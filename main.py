import asyncio

import uvicorn
from uvicorn import Config, Server

from fastapi import FastAPI, APIRouter

from starlette.middleware.cors import CORSMiddleware

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import TOKEN_API, db_url, PUBLIC_URL
from db.base import Base, engine, async_session
from middlewares.db import DbSessionMiddleware
from handlers.base import main_router
from handlers.shop.base import shop_router
from handlers.admin.base import admin_router
from handlers.art.base import art_router


bot = Bot(TOKEN_API)

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(admin_router)
dp.include_router(shop_router)
# dp.include_router(art_router)
dp.include_router(main_router)
dp.update.middleware(DbSessionMiddleware(session_pool=async_session))


#Initialize web server
app = FastAPI(docs_url='/docs_bot')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
event_loop = asyncio.get_event_loop()
config = Config(app=app,
                loop=event_loop,
                host='0.0.0.0',
                port=8000)
server = Server(config)


#For set webhook
WEBHOOK_PATH = f'/webhook'

#Set webhook and create database on start
@app.on_event('startup')
async def on_startup():
    await bot.set_webhook(f"{PUBLIC_URL}{WEBHOOK_PATH}",
                          drop_pending_updates=True,
                          allowed_updates=['message', 'callback_query'])
    await create_db()
    

async def create_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


#Endpoint for incoming updates
@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    tg_update = types.Update(**update)
    await dp.feed_update(bot=bot,
                         update=tg_update)


# async def main():
#     #Database connection
#     engine = create_async_engine(db_url, echo=True)
#     async_session = async_sessionmaker(engine, expire_on_commit=False)

#     bot = Bot(TOKEN_API)
    
#     dp = Dispatcher(storage=MemoryStorage())
#     dp.include_router(admin_router)
#     dp.include_router(shop_router)
#     dp.include_router(art_router)
#     dp.include_router(main_router)
    
#     dp.update.middleware(DbSessionMiddleware(session_pool=async_session))
    
#     async with engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
    
    
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot)


# if __name__ == '__main__':
#     asyncio.run(main())
if __name__ == '__main__':
    event_loop.run_until_complete(server.serve())