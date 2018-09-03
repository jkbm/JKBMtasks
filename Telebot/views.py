from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .bot.bot_core import setup_webhook, Bot
from Telebot.models import Message, Bot_user


# Create your views here.
import os
import json
import logging
logger = logging.getLogger('django')


def index(request):
    """
    Bot home page view
    """

    logger.warning("WARNING MESSAGE...")
    logger.error("ERROR MESSAGE")
    logger.info("INFO MESSAGE")
    logger.debug("DEBUG MESSAGE")
    return render(request, 'Telebot/index.html')

@csrf_exempt
#@require_POST
def webhook(request):
    """
    View to test and setup webhook if necessary
    """

    mode = os.environ.get("BOT_MODE", "") #Set to "wh" to setup and use Webhook
    if mode == "WH":
        setup_webhook()

        if request.method == "POST":
            data = request.body
            jdata = json.loads(data)
            info = "POST DATA:" + str(jdata)
            logger.info(info)
            task_bot = Bot()
            task_bot.send_wh_response(jdata)
    elif mode == "GET":
        setup_webhook('delete')
        task_bot = Bot()
        task_bot.get_updates()
        task_bot.send_response()

    return render(request, 'Telebot/webhook.html')

def show_history(request, chat_id):
    """
    View to display dialog history with specific user
    """

    messages = Message.objects.filter(chat_id=chat_id)
    user = Bot_user.objects.get(id=chat_id)
    if user.username == None: user.username = ""
    if user.last_name == None: user.last_name = ""
    if user.first_name == None: user.first_name = ""
    username = "{0} '{1}' {2}".format(user.first_name, user.username, user.last_name)
    messages_tuple = []
    for m in messages:
        if m.sent == True:
            messages_tuple.append((m.text, "BOT"))
        else:
            messages_tuple.append((m.text, username))
    
    logger.info("Number: %s" % len(messages_tuple))


    return render(request, "Telebot/history.html", {'chat_messages': messages_tuple})

def trigger(request, uid=None):
    """
    View to trigger custom
    """

    bot = Bot()
    bot.send_briefing()

    html = "<html><body>Sent.</body></html>"

    return HttpResponse(html)