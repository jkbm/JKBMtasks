# Taks Bot response generator file

from Telebot.models import Bot_user, Message
from Tasks.models import Task, User
from datetime import datetime
import random
import urllib
import json

import logging

logger = logging.getLogger('django')

commands = {'heys': (['hello', 'hi', 'hey', 'greetings' 'sup', 'wassup', 'привет'], ['Hello', 'Hey, there', 'Hi!', 'Greetings!'])}

global reply_markup
reply_markup = None

def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

def get_answer(update):
    """
    Answer generating root function
    """
    logger.info("Generating answer...")
    text = update['message']['text']
    user = update['message']['chat']

    if text.startswith('/'):
        answer = get_command(update, text, user)
    elif text.lower() in commands['heys'][0]:
        answer = random.choice(commands['heys'][1])
    else:
        context = get_context(text, user)
        if context:
            answer = context
        else:
            answer = "Please use '/help' to discover available commands. Your previous messages was '%s'" % context
    answer = urllib.parse.quote_plus(answer)
    return answer, reply_markup


def get_command(update, text, user):
    """
    Generate command answers
    """
    words = text.split()

    if words[0] == "/start":
        answer = "Hello. This is a task management Bot. You can use this bot to create, delete or update tasks and get notifications about them. Send '/register' to create your account"
    elif words[0] == "/register":
        #CREATE USER
        bot_user = Bot_user.objects.get(id=user['id'])
        answer = "User created. You can start adding tasks by entering '/tasks add' Id: %s." % bot_user.id
    elif words[0] == "/help":
        answer = get_help(text, user)
    elif words[0] == "/user":
        answer = get_user(text, user)
    elif words[0] == "/tasks":
        answer = get_tasks(text, user)
    elif words[0] == "/complete":
        answer = complete_tasks(text, user)
    else:
        answer = "There is no such command."

    return answer

def get_tasks(text, user):
    """
    Generate 'tasks' command answers
    """
    words = text.split()
    bot_user = Bot_user.objects.get(id=user['id'])
    date = datetime.today().strftime('%Y-%m-%d')

    if len(words) > 1 and "add" == words[1]:
        args = text.split('-')[1:]
        if len(args) != 0:        
            params = {'start_date': date, 'created_by': bot_user.app_user}
            for arg in args:
                list_arg = arg.split()
                params[list_arg[0]] = " ".join(list_arg[1:])
            task = Task.objects.create(**params)
            task.created_by_bot = bot_user
            task.save()
            
            answer = "Task '{0}' created. You need to complete it by {1}.".format(task.title, task.finish_date)
        else:
            answer = "Incorect command to create a task(Use -*field* *value* template)."
    else:       
        tasks = Task.objects.filter(created_by=bot_user.app_user, completed=False, start_date__gte=datetime.now().date()).order_by('start_date')
        answer = "Your tasks: \n"
        for task in tasks:
            answer += "<b>{0}</b>: <i>{1}.</i> Complete by: {2}\n".format(task.title, task.description, task.finish_date)        

    return answer

def complete_tasks(text, user):
    """
    Orginise task completion diagloge
    """
    bot_user = Bot_user.objects.get(id=user['id'])
    tasks = Task.objects.filter(created_by=bot_user.app_user, completed=False, start_date__gte=datetime.now().date()).order_by('start_date')
    words = text.split()
    titles = [task.title for task in tasks]
    if len(words) == 1:
        answer = "Choose witch task to mark 'completed'."        
        global reply_markup
        reply_markup = build_keyboard(titles)
    elif " ".join(words[1:]) in titles:
        task = Task.objects.get(title=" ".join(words[1:]))
        task.completed = True
        task.save()
        answer = "Task '{0}' is completed.".format(" ".join(words[1:]))
    else:
        answer = "No such task. Try again or use /tasks to see a list of your active tasks."


    return answer

def get_user(text, user):
    """
    User commands answers
    """
    words = text.split()
    bot_user = Bot_user.objects.get(id=user['id'])
    
    if words[1] == "daily":
        answer = "Use 'daily on/off' to manage daily tasks notifications." 
        if len(words)>3 and words[2] == "on":
            if bot_user.daily == True:
                answer = "Daily tasks already turned on."
            else:
                bot_user.daily = True
                bot_user.save()
                answer = "Daily tasks have been turned on."
        elif len(words)>3 and words[2] == "off":
            bot_user.daily = False
            bot_user.save()
            answer = "Daily tasks have been turned off."

    return answer

def get_help(text, user):
    """
    'Help' commands answers
    """
    words = text.split()
    answer = "This <b>Bot</b> designed to help you manage you daily tasks. Use '/tasks' to display your current tasks. Send '/help *command*' to get more detailed info."
    if len(words)>1:
        if words[1] == "tasks":
            answer = "Use:\n '/tasks' to display current tasks; \n '/tasks add -t *title* -d *description*' to add new task; \n '/tasks complete *title*' to mark a task completed."
        elif words[1] == "user":
            answer = "User '/user' to modify your account settings."

    return answer

def get_context(text, user):
    messages = Message.objects.filter(chat_id=user['id'], sent=False).order_by('-time_sent')[1]
    logger.info("Prev msg: %s" % messages.text)
    context_answer = None
    if messages.text == "/complete":
        task = Task.objects.get(title=text)
        task.completed = True
        context_answer = "Task '{0}' is completed.".format(text)
    return context_answer




