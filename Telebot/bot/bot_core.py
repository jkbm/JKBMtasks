#bot_core.py

import requests
import json
import logging

ACCESS_TOKEN = "620194850:AAFmKn8NBdgbWLWTbPlvd1uOdBd6kLWYkQk"
myurl = "https://www.jekabm.com/bot/telebot"
URL = "https://api.telegram.org/bot%s/" % ACCESS_TOKEN

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
def setup_webhook():
    resp = ""
    try:
        logger.error("Setting webhook...")
        r = requests.get(URL +"getWebhookInfo")
        rj = r.json()
        if rj['result']['url'] != "":
            logger.info("WEBHOOK is already set!")
        else:
            r = requests.get(URL + "setWebhook?url=%s" % myurl)
            logger.info("Result of setting webhook %s" % r.text)
        #r = requests.get(URL + "deleteWebhook")
        
        if r.status_code != 200:
            logger.error("Can't set hook: %s. Quit." % r.text)
        else:
            logger.debug(r.text)

        

    except Exception as e:
        logging.error("There was an error setting up WebHook: %s" % e)
    return r.text
def respond(query):

    pass
class Bot:

    def __init__(self):
        get_init = json.loads(requests.get(URL + "egetme").text)
        self.id = get_init['result']['id']
        self.name = get_init['result']['first_name']
        self.username = get_init['result']['username']

    def get_updates(self):
        self.updates = json.loads(requests.get("https://api.telegram.org/bot{0}/getUpdates".format(ACCESS_TOKEN)).text)
        self.messages = [(x['message']['from'], x['message']['text']) for x in self.updates['result']]
    
    def send_message(self, text):
        url = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}".format(ACCESS_TOKEN, self.messages[0][0]['id'], text)
        self.sent = json.loads(requests.get(url).text)

    def get_tasks(self):
        #tasks = Task.objects.all()
        return True


if __name__ == "__main__":
    task_bot = Bot()
    task_bot.get_updates()
    task_bot.send_message("Hey there!")
        