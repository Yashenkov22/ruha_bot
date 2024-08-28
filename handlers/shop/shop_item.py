from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto

from sqlalchemy.ext.asyncio import AsyncSession

from db.queries import select_current_item, select_photos_for_item
from utils.item_photo import item_constructor

item_view_router = Router()


@item_view_router.callback_query(F.data.startswith('show_item'))
async def init_current_item(callback: types.CallbackQuery,
                            state: FSMContext,
                            session: AsyncSession):
    item_name = callback.data.split(':')[-1]
    item = await select_current_item(session, item_name)
    item = item[0]
    item_id = item.id
    photo_current_item = await select_photos_for_item(session, item_id)
    item_photos = list(map(lambda photo: photo[0], photo_current_item))
    
    if not item_photos:
        await callback.answer('У товара ещё нет фото, временно недоступен',
                              show_alert=True)
    else:
        await state.update_data(name=item.name)
        await state.update_data(price=item.price)
        await state.update_data(photos=item_photos)
        await state.update_data(photo_idx=0)
    
        await show_item(callback, state)
        await callback.message.delete()


async def show_item(callback: types.CallbackQuery,
                    state: FSMContext):
    data = await state.get_data()
    name, price, photo, photo_kb = item_constructor(data)

    if not data.get('visited'):
        await state.update_data(visited=True)

        await callback.message.answer_photo(photo,
                                            caption=f'Товар: {name}\nЦена: {price}',
                                            disable_notification=True,
                                            reply_markup=photo_kb.as_markup())
        
    else:
        await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                          type='photo',
                                                          caption=f'Товар: {name}\nЦена: {price}'),
                                          reply_markup=photo_kb.as_markup())


@item_view_router.callback_query(F.data.startswith('photo'))
async def init_current_photo(callback: types.CallbackQuery,
                            state: FSMContext):
    action = callback.data.split('_')[-1]
    data = await state.get_data()
    photo_idx = data['photo_idx']
    match action:
        case 'next':
            await state.update_data(photo_idx=photo_idx+1)
        case 'prev':
            await state.update_data(photo_idx=photo_idx-1)
    await show_item(callback, state)
