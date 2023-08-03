from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram import F
from consts import BOT_TOKEN

bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

@dp.message(Command(commands=["start"]))
async  def process_start_command(message):
    await message.answer('Привет!\nЯ слон. Купи меня!')

@dp.message(Command(commands=["help"]))
async  def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'и я пришлю тебе твое сообщение')

@dp.message()
async def send_echo(message:Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
        print(message.from_user.id)
    except TypeError:
        await message.reply(text='Данный тип апдейтов не поддерживается'
                                 ' методом send_copy')


if __name__ == '__main__':
    dp.run_polling(bot)