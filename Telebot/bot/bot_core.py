#bot_core.py

import requests
import json
import logging
from Tasks.models import Task
from ..models import Bot_user
from .bot_response import get_answer
logger = logging.getLogger('django')

ACCESS_TOKEN = "620194850:AAFmKn8NBdgbWLWTbPlvd1uOdBd6kLWYkQk"
myurl = "https://www.jekabm.com/bot/telebot"
URL = "https://api.telegram.org/bot%s/" % ACCESS_TOKEN


def setup_webhook(action='get'):
    """
    Checking webhook status. Setup/remove if necessary
    """
    if action == 'set':
        r = requests.get(URL + "setWebhook?url=%s" % myurl)
    elif action == 'delete':
        r = requests.get(URL + "deleteWebhook")
    else:
        r = requests.get(URL +"getWebhookInfo")

    try:
        #r = requests.get(URL + "deleteWebhook")
        
        if r.status_code != 200:
            logger.error("Can't set hook: %s. Quit." % r.text)
        else:
            logger.info("Result of webhook check %s" % r.text)

        

    except Exception as e:
        logging.error("There was an error setting up WebHook: %s" % e)
    return r.text



def respond(query):

    pass


class Bot:
    URL = "https://api.telegram.org/bot{0}".format(ACCESS_TOKEN)
    def __init__(self):
        get_url = URL + "getme"
        get_init = json.loads(requests.get(get_url).text)
        logger.info(get_url)
        self.id = get_init['result']['id']
        self.name = get_init['result']['first_name']
        self.username = get_init['result']['username']

    def get_request(self, url):
        r = requests.get(url).text
        jr = json.loads(r)
        return r, jr

    def get_updates(self):
        get_url = "{0}getUpdates".format(URL)
        self.updates = json.loads(requests.get(get_url).text)
        #self.messages = [(x['message']['from'], x['message']['text']) for x in self.updates['result']]
        user = self.updates['result'][-1]['message']['from']
        user.pop('is_bot')
        user.pop('language_code')
        bot_user, created = Bot_user.objects.get_or_create(id=user['id'])
        bot_user = Bot_user.objects.filter(id=user.pop('id')).update(**user)        
    
    def get_last_chat_id_and_text(self):
        num_updates = len(self.updates["result"])
        if num_updates > 0:
            last_update = num_updates - 1
            last = text = self.updates["result"][last_update]
            text = self.updates["result"][last_update]["message"]["text"]
            chat_id = self.updates["result"][last_update]["message"]["chat"]["id"]
        else:
            text, chat_id = ""

        return (text, chat_id, last)

    def send_response(self, text=None):
        #get_url = "{0}sendMessage?chat_id={1}&text={2}".format(URL, self.messages[0][0]['id'], text)
        #self.sent = json.loads(requests.get(get_url).text)
        last_text, chat_id, last_update = self.get_last_chat_id_and_text()
        if text == None:
            text = last_text
        else:
            text = "Your tasks: %s" % text

        answer = get_answer(last_update)
        if chat_id != "":
            url = URL + "sendMessage?parse_mode=html&text={0}&chat_id={1}".format(answer, chat_id)
            r, jr = self.get_request(url)
            logger.info("Result: {0}".format(r))
 
    def send_tasks(self):
        tasks = Task.objects.all()
        tasks_names = [t.title for t in tasks]
        self.send_response(tasks_names)


    def get_tasks(self):
        #tasks = Task.objects.all()
        return True


if __name__ == "__main__":
    task_bot = Bot()
    task_bot.get_updates()
        