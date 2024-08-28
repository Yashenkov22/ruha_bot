from aiogram.fsm.state import State, StatesGroup


class AddCategory(StatesGroup):
    name = State()


class DeleteCategory(StatesGroup):
    category = State()


class AddItem(StatesGroup):
    category = State()
    name = State()
    price = State()


class DeleteItem(StatesGroup):
    category = State()
    name = State()


class EditItem(StatesGroup):
    old_item = State()
    name = State()
    price = State()


class AddPhoto(StatesGroup):
    photo = State()


class AddArtist(StatesGroup):
    name = State()


class DelArtist(StatesGroup):
    name = State()