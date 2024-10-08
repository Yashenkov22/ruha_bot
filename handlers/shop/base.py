from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from utils.keyboards.main_keyboard import create_close_kb
from utils.keyboards.shop_keyboards import (create_category_kb,
                                            create_items_kb)
from utils.delete_message import (try_delete_prev_message,
                                  add_message_for_delete)
from .shop_item import item_view_router


shop_router = Router()
shop_router.include_router(item_view_router)


@shop_router.message(F.text == 'Ассортимент')
async def show_categories(message: types.Message | types.CallbackQuery,
                          state: FSMContext,
                          bot: Bot,
                          session: AsyncSession):
    await try_delete_prev_message(bot, state)

    category_kb = await create_category_kb(session)
    await message.answer('Выбери категорию',
                         disable_notification=True,
                         reply_markup=category_kb.as_markup())
    
    try:
        await message.delete()
    except Exception:
        pass
    

@shop_router.message(F.text == 'Написать продавцу')
async def show_link(message: types.Message | types.CallbackQuery,
                    bot: Bot,
                    state: FSMContext):
    await try_delete_prev_message(bot, state)

    # await state.update_data(visited=None)

    if isinstance(message, types.CallbackQuery):
        message = message.message

    await message.answer(f'По поводу заказа писать @sayflame',
                         disable_notification=True,
                         reply_markup=create_close_kb('saler').as_markup())
    
    try:
        await message.delete()
    except Exception:
        pass


#Category button callback handler
@shop_router.callback_query(F.data.startswith('cat'))
async def show_items_list(callback: types.CallbackQuery,
                          state: FSMContext,
                          session: AsyncSession,
                          cat: str = None):
    category = callback.data.split(':')[-1] if cat is None else cat
    await state.update_data(category=category)
    item_kb = await create_items_kb(category, session)
    
    if item_kb is None:
        await callback.answer('В категории пока нет товаров',
                              show_alert=True)
    else:
        await callback.message.answer('Выбери товар',
                                      disable_notification=True,
                                      reply_markup=item_kb.as_markup())
        try:
            await callback.message.delete()
        except Exception:
            pass