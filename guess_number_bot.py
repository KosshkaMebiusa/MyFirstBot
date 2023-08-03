from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command
from aiogram.types import Message
from consts import BOT_TOKEN
import requests
API_CAT_URL = 'https://api.thecatapi.com/v1/images/search'
API_DOG_URL = 'https://random.dog/woof.json'
API_FOX_URL = 'https://randomfox.ca/floof/'
import random

bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

ATTEMPTS: int = 5
MAX_NUMBER = 100
users: dict = {}

def get_random_number() -> int:
    return random.randint(1, MAX_NUMBER)


def get_cat_image_link() -> str:
    cat_response = requests.get(API_CAT_URL)
    return cat_response.json()[0]['url']


def get_dog_image_link() -> str:
    dog_response = requests.get(API_DOG_URL)
    return dog_response.json()['url']


def get_fox_image_link() -> str:
    fox_response = requests.get(API_FOX_URL)
    return fox_response.json()['image']


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Давай сыграем с тобой в игру!\nЯ загадаю число, а ты должен его угадать\n'
                         'Подробные правила можешь прочитать по команде /help')
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}

@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до {MAX_NUMBER}, '
                         f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')

@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
                         f'Игр выиграно: {users[message.from_user.id]["wins"]}')
    await message.answer_photo(photo=get_fox_image_link())

@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('А мы итак с вами не играем. '
                             'Может, сыграем разок?')

@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра',
                       'Играть', 'Хочу играть'], ignore_case=True))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(f'Ура!\n\nЯ загадал число от 1 до {MAX_NUMBER}, '
                             'попробуй угадать!')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer(f'Пока мы играем в игру я могу '
                             f'реагировать только на числа от 1 до {MAX_NUMBER} '
                             f'и команды /cancel и /stat')

# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             f'пожалуйста, числа от 1 до {MAX_NUMBER}')


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= MAX_NUMBER)
async def process_number_answer(message:Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Ура!!! Вы угадали число!\nВот котик для победителя')
            await message.answer_photo(photo=get_cat_image_link())
            await message.answer('Может, сыграем еще?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Моё число меньше')
            users[message.from_user.id]['attempts'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer('Моё число больше')
            users[message.from_user.id]['attempts'] -= 1
        if users[message.from_user.id]['attempts'] <= 0:
            await message.answer(f'К сожалению, у вас больше не осталось '
                                 f'попыток. Вы проиграли :(\n\nМое число '
                                 f'было {users[message.from_user.id]["secret_number"]}\nВот вам утешительный пёсик')
            await message.answer_photo(photo=get_dog_image_link())
            await message.answer('Давайте сыграем еще?')

            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


@dp.message()
async def process_other_text_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(f'Мы же сейчас с вами играем. '
                             f'Присылайте, пожалуйста, числа от 1 до {MAX_NUMBER}')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')

if __name__ == '__main__':
    dp.run_polling(bot)