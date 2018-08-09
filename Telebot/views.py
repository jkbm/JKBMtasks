from django.shortcuts import render
from .bot.bot_core import setup_webhook, Bot
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.
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
@require_POST
def webhook(request):
    """
    View to test and setup webhook if necessary
    """
    #response = setup_webhook()
    if request.method == "POST":
        data = request.body
        jdata = json.loads(data)
        info = "POST DATA:" + jdata
        logger.info(info)

    task_bot = Bot()
        #task_bot.get_updates()
    task_bot.send_wh_response()
        #response = setup_webhook()

    return render(request, 'Telebot/webhook.html')