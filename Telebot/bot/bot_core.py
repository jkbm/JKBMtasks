#bot_core.py

import requests
import json
import logging
from Tasks.models import Task
from ..models import Bot_user, Message
from .bot_response import get_answer, get_tasks, get_notes
from Telebot.misc.currency import get_rates
from Telebot.misc.weather import get_weather
from datetime import datetime
import os

logger = logging.getLogger('django')

ACCESS_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
myurl = "https://fierce-bayou-86062.herokuapp.com/bot/webhook/"
URL = "https://api.telegram.org/bot%s/" % ACCESS_TOKEN


def setup_webhook(action='get'):
    """
    Checking webhook status. Setup/remove if necessary
    """
    r = requests.get(URL +"getWebhookInfo")
    if r.status_code != 200:
        logger.error("Can't set hook: %s. Quit." % r.text)
    check = json.loads(r.text)

    if action == 'get':
        if check['result']['url'] == '':
            r = requests.get(URL + "setWebhook?url=%s" % myurl)
    elif action == 'delete':
        if check['result']['url'] == '':
            logger.info("Webhook not set.")
        else:
            r = requests.get(URL + "deleteWebhook")
            logger.info("Webhook was deleted.")
        
    

def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


class Bot:
    """
    Telegram bot for tasks management class
    """

    URL = "https://api.telegram.org/bot{0}".format(ACCESS_TOKEN)
    def __init__(self):
        get_url = URL + "getme"
        get_init = json.loads(requests.get(get_url).text)
        self.id = get_init['result']['id']
        self.name = get_init['result']['first_name']
        self.username = get_init['result']['username']

    def get_request(self, url):
        r = requests.get(url).text
        jr = json.loads(r)
        return r, jr

    def get_bot_user(self, user):
        bot_user, created = Bot_user.objects.get_or_create(id=user['id'])
        bot_user = Bot_user.objects.filter(id=user.pop('id')).update(**user)  

    def get_updates(self):
        get_url = "{0}getUpdates".format(URL)
        self.updates = json.loads(requests.get(get_url).text)
        #self.messages = [(x['message']['from'], x['message']['text']) for x in self.updates['result']]
        user = self.updates['result'][-1]['message']['from']
        user.pop('is_bot')
        user.pop('language_code')
        self.get_bot_user(user)   
    
    def get_last_chat_id_and_text(self):
        num_updates = len(self.updates["result"])
        if num_updates > 0:
            last_update = num_updates - 1
            last = self.updates["result"][last_update]
            text = self.updates["result"][last_update]["message"]["text"]
            chat_id = self.updates["result"][last_update]["message"]["chat"]["id"]
        else:
            text, chat_id = ""

        return (text, chat_id, last)

    def save_message(self, update, text=None):

        params = {'chat_id': update['message']['chat']['id'],
                  'time_sent': datetime.fromtimestamp(update['message']['date'])}

        if text == None:
            params['sent'] = False
            params['text'] = update['message']['text']
        else:
            params['text'] = text
            params['sent'] = True
            params['time_sent'] = datetime.now()

        message = Message.objects.create(**params)

    def send_response(self, text=None, reply_markup=None):
        #get_url = "{0}sendMessage?chat_id={1}&text={2}".format(URL, self.messages[0][0]['id'], text)
        #self.sent = json.loads(requests.get(get_url).text)
        last_text, chat_id, last_update = self.get_last_chat_id_and_text()
        if text == None:
            text = last_text
        else:
            text = "Your tasks: %s" % text
        
        answer, reply_markup = get_answer(last_update)
        
        if chat_id != "":
            url = URL + "sendMessage?parse_mode=html&text={0}&chat_id={1}".format(answer, chat_id)
            if reply_markup:
                url += "&reply_markup={0}".format(reply_markup)
            r, jr = self.get_request(url)
            logger.info("Result: {0}".format(r))
            self.save_message(last_update)
            self.save_message(last_update, answer)
    
    def send_wh_response(self, update=None, reply_markup=None):
        try:
            logger.info("Update: {0}".format(update))
            user = update['message']['from']
            user.pop('is_bot')
            user.pop('language_code')
            self.get_bot_user(user)
            chat_id = update['message']['chat']['id']
            answer, reply_markup = get_answer(update)
            
            if chat_id != "":
                url = URL + "sendMessage?parse_mode=html&text={0}&chat_id={1}".format(answer, chat_id)
                if reply_markup:                    
                    url += "&reply_markup={0}".format(reply_markup)
                self.save_message(update)
                self.save_message(update, answer)
                r, jr = self.get_request(url)
                logger.info("Result: {0}".format(r))
        except Exception as e:
            logger.error("Response error: {0}: {1}".format(e, e.args))
 
    def send_tasks(self, chat_id="263702884"):
        user = {'id': chat_id}
        text = "/tasks"
        bot_user = Bot_user.objects.get(id=user['id'])
        if bot_user.daily_tasks == True:
            tasks = get_tasks(text, user)
            url = URL + "sendMessage?parse_mode=html&text={0}&chat_id={1}".format(tasks, chat_id)
            r, jr = self.get_request(url)
            logger.info("Tasks sent: %s" % r)

    def send_briefing(self, chat_id="263702884"):
        user = {'id': chat_id}
        bot_user = Bot_user.objects.get(id=user['id'])
        if bot_user.daily_tasks == True:
            tasks = get_tasks("/tasks", user)
            notes = get_notes("/notes", user)
            currencies = "\n<b>{0}</b>".format(get_rates())
            text = tasks + "\n" + notes + currencies
            text += "\n" +  get_weather()
            url = URL + "sendMessage?parse_mode=html&text={0}&chat_id={1}".format(text, chat_id)
            r, jr = self.get_request(url)
            logger.info("Daily brief sent: %s" % r)


if __name__ == "__main__":
    task_bot = Bot()
    task_bot.get_updates()
        