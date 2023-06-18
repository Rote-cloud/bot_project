from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand
from aiogram.utils.callback_data import CallbackData
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from weather import Weather
from sheetsEntry import SheetsEntry
from actionDB import ActionRepository
from setting import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
cb = CallbackData("button", "action")
db = ActionRepository()

async def setup_bot_commands(bot):
    bot_commands = [
        BotCommand(command="/start"),
        BotCommand(command="/help")
    ]
    await bot.set_my_commands(bot_commands)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Используй /help для получения "
                        "списка доступных команд")

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    kb = [[
        types.KeyboardButton(text="Прогноз погоды на сегодня"),
        types.KeyboardButton(text="Прогноз погоды на сегодня с показом температуры через каждые 3 часа"),
        types.KeyboardButton(text="Прогноз погоды на следующие несколько дней"),
        types.KeyboardButton(text="Вывод всех ссылок с прогнозами")
    ]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True,
        input_field_placeholder="Выберете одну из доступных функций"
    )
    await message.answer("Выберете одну из функций", reply_markup=keyboard)

@dp.message_handler(Text("Прогноз погоды на сегодня"))
async def weather_today_command(message: types.Message):
    await message.answer(Weather().get_weather())

@dp.message_handler(Text("Прогноз погоды на сегодня с показом температуры через каждые 3 часа"))
async def weather_today_time_command(message: types.Message):
    url = get_url_sheets(Weather(0, True).get_weather(), message.from_user.username)

    urlBoard = InlineKeyboardMarkup(row_width=1)
    urlButton = InlineKeyboardButton(text="Ссылка", url=url)
    urlBoard.add(urlButton)
    await message.answer("Ссылка на таблицу с прогнозом", reply_markup=urlBoard)

@dp.message_handler(Text("Прогноз погоды на следующие несколько дней"))
async def weather_few_days_command(message: types.Message):
    kb = [[
        types.InlineKeyboardButton(text="1", callback_data="num_1"),
        types.InlineKeyboardButton(text="2", callback_data="num_2"),
        types.InlineKeyboardButton(text="3", callback_data="num_3"),
        types.InlineKeyboardButton(text="4", callback_data="num_4"),
        types.InlineKeyboardButton(text="5", callback_data="num_5")
    ],]
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=kb, resize_keyboard=True
    )
    await message.answer("Выбери на скольно дней сделать прогноз", reply_markup=keyboard)

@dp.message_handler(Text("Вывод всех ссылок с прогнозами"))
async def value_output(message: types.Message):
    values = db.value_output(message.from_user.username)
    if len(values) == 0:
        await message.answer("В базе данных пока нет ваших записей.\n"
                             "Воспользуйтесь сначала 2 или 3 функцией")
    else:
        string = ""
        for i in values:
            string += i[1] + "\n"
        await message.answer(f"Все зделанные вами ссылки:\n {string}")

@dp.callback_query_handler(Text(startswith="num_"))
async def future_forecast(callback: types.CallbackQuery):
    num = int(callback.data.split("_")[1])
    url = get_url_sheets(Weather(num, True).get_weather(), callback.from_user.username)

    urlBoard = InlineKeyboardMarkup(row_width=1)
    urlButton = InlineKeyboardButton(text="Ссылка", url=url)
    urlBoard.add(urlButton)
    await callback.message.answer("Ссылка на таблицу с прогнозом", reply_markup=urlBoard)

def get_url_sheets(df, user_name):
    sheets = SheetsEntry()
    url = sheets.data_entry(df, user_name, db)

    return url

if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        db.closeDB()

