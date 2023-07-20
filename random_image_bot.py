import time
import requests
import pprint as p

API_BOT_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '978109895:AAF4HaYciZeBgeNgOy7maYxyrceYGbCR9HI'
API_CAT_URL = 'https://api.thecatapi.com/v1/images/search'
API_DOG_URL = 'https://random.dog/woof.json'
API_FOX_URL = 'https://randomfox.ca/floof/'
ERROR_TEXT: str = 'Здесь должна была быть картинка :('


offset: int = -2
counter: int = 0
chat_response: requests.Response
link: str
field: str
chat_id:int

while counter < 100:
            print('attempt = ', counter)

            updates = requests.get(f'{API_BOT_URL}{BOT_TOKEN}/getUpdates?offset={offset+1}').json()
            if updates['result']:
                for result in updates['result']:
                    offset = result['update_id']
                    chat_id = result['message']['from']['id']
                    match result['message']['text']:
                        case '/cat':
                            chat_response = requests.get(API_CAT_URL)
                            link = chat_response.json()[0]['url']
                        case '/dog':
                            chat_response = requests.get(API_DOG_URL)
                            link = chat_response.json()['url']
                        case '/fox':
                            chat_response = requests.get(API_FOX_URL)
                            link = chat_response.json()['image']

                    if chat_response.status_code == 200:
                        requests.get(f'{API_BOT_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={link}')
                    else:
                        requests.get(f'{API_BOT_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

            time.sleep(1)
            counter += 1
