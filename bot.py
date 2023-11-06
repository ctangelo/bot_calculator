from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor, types
from aiogram import Bot
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from script import calculation

# инициализация бота
storage = MemoryStorage()
TOKEN = 'TOKEN'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

# инициализация кнопок
upload_btn = ReplyKeyboardMarkup(resize_keyboard=True)
btn = KeyboardButton('/upload')
upload_btn.add(btn)


# обработка команды /start
@dp.message_handler(commands=['start'], state="*")
async def start_message(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    # если вдруг машину состояний запустили, а потом сразу нажали команду старт, то завершаем машину состояний, чтоб не было ошибок
    if current_state:  
        await state.finish()
    await bot.send_message(message.from_user.id, '👋Привет! Нажми /upload чтоб начать', reply_markup=upload_btn)


# инициализация машины состояний для приема файла
class FSMXlsx(StatesGroup):
    file = State()


# просим пользователя загрузить документ и сохраняем его в папку с названием его телеграм айди
@dp.message_handler(commands=['upload'], state=None)
async def upload(message: types.Message, state=FSMContext):
    await FSMXlsx.file_1.set()
    await message.reply('Загрузи заполненный файл эксель')
    
    
# Принимаем документ от пользователя
@dp.message_handler(content_types=['document'], state=FSMXlsx.file)
async def import_file(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.document.download(destination_file=f"/root/doc/{user_id}/file.xlsx")
    file = f"/root/doc/{user_id}/file.xlsx"
    
    # передаю в твой скрипт путь до файла и айди пользователя (для того чтобы потом сохранить пнг в той же директории)
    calculation(file, user_id)
    # забираю готовую png из директории
    photo = InputFile(f'/root/doc/{user_id}/ready.png')
    # отправляю png
    await bot.send_photo(user_id, photo)
    # выход из машины состояний
    await state.finish()


async def on_startup(_):
    print('Bot online')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)  