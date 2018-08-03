from django.shortcuts import render
from .bot.bot_core import setup_webhook
# Create your views here.
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

def webhook(request):
    """
    View to test and setup webhook if necessary
    """

    response = setup_webhook()

    return render(request, 'Telebot/webhook.html', {'r': response})