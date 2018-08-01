from django.shortcuts import render
from .bot.bot_core import setup_webhook
# Create your views here.
import logging
logger = logging.getLogger(__name__).setLevel(logging.INFO)
logger = logging.getLogger(__name__)
def index(request):

    return render(request, 'Telebot/index.html')

def webhook(request):
    logger.info("Testing Webhook")
    response = setup_webhook()

    return render(request, 'Telebot/webhook.html', {'r': response})