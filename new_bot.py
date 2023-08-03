from aiogram import Bot, Dispatcher
from aiogram.filters import BaseFilter
from  consts import BOT_TOKEN
from aiogram.types import Message

admin_ids: list[int] = [59179985]

class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

@dp.message(IsAdmin(admin_ids))
async def answer_if_admin_update(message: Message):
    await message.answer(text='Вы админ')


@dp.message()
async def answer_if_not_admin(message:Message):
    await message.answer(text='Вы не админ')

if __name__ == '__main__':
    dp.run_polling(bot)
