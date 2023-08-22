import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegrambot.settings.local')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from telegram.ext import CommandHandler, MessageHandler, Filters, ContextTypes, Updater, CallbackContext
from django.db import models
from applications.questions.models import Question, PosibleAnswers, QuestionBlock
from chatbot.handlers import  *


# Run the program
if __name__ == '__main__':


    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register the start command handler
    dispatcher.add_handler(question_handler)
    dispatcher.add_handler(CallbackQueryHandler(button_click))

 
    # Commands
    print('Polling...')
    updater.start_polling()
    updater.idle()