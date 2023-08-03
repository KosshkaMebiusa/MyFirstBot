from aiogram import Bot, Dispatcher
from aiogram.filters import BaseFilter, Text
from aiogram.types import Message
from consts import BOT_TOKEN

bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()

class NumbersInMesage(BaseFilter):
    async def __call__ (self, message: Message) -> bool | dict[str, list[int]]:
        numbers = []
        for word in message.text.split(' '):
            normalized_word = word.replace('.', '').replace(',', '').strip()
            if normalized_word.isdigit():
                numbers.append(int(normalized_word))
        if numbers:
            return {'numbers': numbers}
        return False

@dp.message(Text(startswith='найди числа', ignore_case=True), NumbersInMesage())
async def process_if_numbers(message:Message, numbers: list[int]):
    await message.answer(text=f'Нашёл: {", ".join(str(num) for num in numbers)}')

@dp.message(Text(startswith='найди числа', ignore_case=True))
async  def process_if_not_numbers(message: Message):
    await message.answer(text='Не нашел что-то :(')


if __name__ == '__main__':
    dp.run_polling(bot)