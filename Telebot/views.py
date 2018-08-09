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
    logger.info(request.META)
    logger.info(request.POST)
    logger.info(request.method)
    logger.info(request.body)
    if request.POST:
        data = request.POST
        jdata = json.loads(data)
        info = "POST DATA:" + jdata
        logger.info(info)
    task_bot = Bot()
        #task_bot.get_updates()
        #task_bot.send_response()
        #response = setup_webhook()

    return render(request, 'Telebot/webhook.html')