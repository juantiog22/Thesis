from typing import Final
from datetime import datetime, timedelta
import datetime
import logging
import random

import telegram
from telegram import Update
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Filters, ContextTypes, Updater, CallbackQueryHandler, ConversationHandler, Job, JobQueue

from django.utils import timezone
from django.db import models
from applications.questions.models import Question, PosibleAnswers, QuestionBlock
from applications.answers.models import Answer
from applications.usuarios.models import Suscriber
from applications.contexts.models import Context, Message

from .replyMessages import *

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

TOKEN: Final = '6605050919:AAHQHti_iTxcOWaBhyBGvwGH5rVk2nyVfAw'
BOT_USERNAME: Final =  '@postcovidai_bot'




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""                                                        ""
""                 'WELCOME'                              ""
""                                                        ""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

FIRST_STATE, SECOND_STATE, THIRD_STATE, FOURTH_STATE = range(4)


#Method to give welcome and register user's data
def welcome(update, context):

    chat_id=update.effective_chat.id
    name=update.message.from_user.first_name
    surname=update.message.from_user.last_name
    username=update.message.from_user.username
    #Register user's data. If exist get if not create the user
    suscriber, created = Suscriber.objects.get_or_create(
        chatid = chat_id,
        name=name,
        surname=surname,
        username=username,
    )

    logging.info(f'User {username} just enter/registered in the system')

    context.bot.send_message(chat_id=chat_id, text=messages['welcome'], reply_markup=ReplyKeyboardRemove())
    context.bot.send_message(chat_id=chat_id, text=messages['confidential_information'])
    context.bot.send_message(chat_id=chat_id, text=f"De acuerdo {name}, estas listo/a para empezar?")

    return THIRD_STATE
   

#Function that redirects to the corresponding state depending on the question history of the user
def start_handler(update, context):

    user_response = update.message.text.lower()

    if user_response in affirmation:

        try:
            suscriber = Suscriber.objects.get(chatid=update.effective_chat.id)

            question = choose_question(suscriber)

            message = choose_message(question)

            answers = PosibleAnswers.objects.filter(question=question)
            reply_markup = custom_keyboard(answers)

            context.bot.send_message(chat_id=update.effective_chat.id, text=messages['question_explanation'])
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{message}")
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{question.title}.", reply_markup=reply_markup)
            return FIRST_STATE
        
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text='No tienes preguntas por responder')
            return SECOND_STATE
    
    else: 
        context.bot.send_message(chat_id=update.effective_chat.id, text=messages['negation']['0'])
        return SECOND_STATE





""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""                                                        ""
""                 'Response Manager'                     ""
""                                                        ""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#Function to handle user's interaction
def generate_response(update, context):

    user_response = update.message.text.lower()
    message = user_response.split()
    user = update.message.from_user

    suscriber = Suscriber.objects.get(chatid=user.id) 

    con = find_context(user_response)

    if con is not None:
        
        if con == 'affirmation':
            context.bot.send_message(chat_id=user.id, text=messages['redirect'])
            #Remove the user's job
            if context.job_queue.jobs():
                MessageJob.remove_job(context, suscriber)    
            return THIRD_STATE
        else:
            length = len(messages[con])
            random_var = random.randint(0,length-1)
            context.bot.send_message(chat_id=user.id, text=messages[con][str(random_var)])

    else:
        if choose_question(suscriber):
            context.bot.send_message(chat_id=user.id, text=messages['questions_pending'])
        else: 
            buttons = [
                InlineKeyboardButton("Quién soy?", callback_data="whoami"),
                InlineKeyboardButton("Propósito", callback_data="purpose"),
                InlineKeyboardButton("Contacto", callback_data="contact"), 
                InlineKeyboardButton("Sitio Web", url="https://projects.ugr.es/postcovid-ai/es/")
                ]
            reply_markup = InlineKeyboardMarkup([buttons])

            update.message.reply_text(messages['frecuent_quest'], reply_markup=reply_markup)


def button_click(update, context):
    query = update.callback_query
    query.answer()

    if query.data == "whoami":
        context.bot.send_message(chat_id=query.message.chat_id, text=messages['whoami'])
    elif query.data == "purpose":
        context.bot.send_message(chat_id=query.message.chat_id, text=messages['purpose'])
    elif query.data == "contact":
        context.bot.send_message(chat_id=query.message.chat_id, text=messages['contact'])
    return SECOND_STATE


#Function to find context of user's response
def find_context(response):
    words = response.split()
    for word in words:
        if word in greetings:
            return 'greetings'
        elif word in farewell:
            return 'farewell'
        elif word in gratitude:
            return 'gratitude'
        elif word in negation:
            return 'negation'
        elif word in affirmation:
            return 'affirmation'
        elif word in mood:
            return 'mood'
        elif word in name:
            return 'name'
        elif word in goodmood:
            return 'goodmod'
        elif word in badmood:
            return 'badmood'
        elif word in joke:
            return 'joke'
            
        
    return None
        
    


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""                                                        ""
""                 'Job Creator'                          ""
""                                                        ""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#Class that creates an user's job
class MessageJob(object):

    def __init__(self, context, suscriber):
        self.suscriber = suscriber
        self.create_job(context)
        

    def create_job(self, context):
        #Create an user's job
        context.job_queue.run_repeating(callback=self.job, interval=86400, first=0, context=self.suscriber.chatid, name=self.suscriber.chatid)
        
        
    def job(self, context):
        # This function will be executed every 24 hours
        question = choose_question(self.suscriber)
        if question is not None:
            context.bot.send_message(chat_id=self.suscriber.chatid, text=f"Hey {self.suscriber.name} tienes preguntas por responder. ¿Te gustaría empezar el cuestionario?")
    
    def remove_job(context, suscriber):
        for job in context.job_queue.jobs():
                if str(job.name) == str(suscriber.chatid):
                    job.schedule_removal()





""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""                                                        ""
""                 'Questions Manager'                    ""
""                                                        ""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""




#Function that return if a question is answered by an user
def is_answered(user, question):
    frecuency = QuestionBlock.objects.filter(question=question).first().frecuency

    #Check block frecuency and assign a value
    if frecuency == 'D':
        date_interval = timedelta(days=1)
    elif frecuency == 'W':
        date_interval = timedelta(weeks=1)
    elif frecuency == 'M':
        date_interval = timedelta(weeks=4)
    else:
        date_interval = timedelta(weeks=12)

    date = timezone.now() - date_interval

    return Answer.objects.filter(question=question, suscriber=user, date__gt=date).exists()
    

#Function that choose the next question to ask according to the user
def choose_question(user):
    bloques = QuestionBlock.objects.filter(active=True).order_by('-importance')
    global first
    first = False
    block_counter = 0
    question_result = None
    for block in bloques:
        questions = Question.objects.filter(blocks=block).order_by('create')
        first_value = questions.first()
        for question in questions:
            if is_answered(user, question) == False:
                question_result = question
                #if is the first question in the block show message
                if first_value == question:
                    first = True
                else:
                    first = False
                break
        block_counter += 1
    return question_result


#Function that choose the message to display on the chat
def choose_message(question):
    contexts_block = get_contexts_by_block(question.blocks.first().id)
    messages = Message.objects.filter(context=contexts_block)
    random_message = random.randint(0,messages.count()-1)
    
    return messages[random_message]


#Function that returns the contexts related to a block
def get_contexts_by_block(bloque):
    context = Context.objects.filter(block__id=bloque).first()
    return context


#Function to get a custom keyboard in Telegram
def custom_keyboard(values):
    schema = [[str(value)] for value in values]
    return ReplyKeyboardMarkup(schema, one_time_keyboard=True, resize_keyboard=True)


#Function that check if the user response is valid
def valid_answer(question, response):
    answers = PosibleAnswers.objects.filter(question=question)
    posible_answers = []
    for answer in answers:
        posible_answers.append(answer.texto)
    return response in posible_answers


#Function that performs the questionary 
def handle_answer(update, context):

        user = update.message.from_user
        user_response = update.message.text

        suscriber = Suscriber.objects.get(chatid=user.id)
        question = choose_question(suscriber)
        
        #Only jump to next question if the answer is valid
        if valid_answer(question, user_response): 
            #Store the answer in the DB if is valid
            answer = Answer.objects.create(
                    response=str(user_response),
                    question=question,
                    suscriber=suscriber,
                )
            answer.save()
            
            logging.info(f'User {suscriber.username} answer the question {question.title}')
            
            #Get next question to answer
            try:
                question = choose_question(suscriber)

                #Choose next message 
                message = choose_message(question)

                #if is the first question in the block show message
                if first:
                    update.message.reply_text(f"{message}")   
                
                #Show next questioni
                answers = PosibleAnswers.objects.filter(question=question)
                reply_markup = custom_keyboard(answers)

                update.message.reply_text(f"{question.title}", reply_markup=reply_markup)

            except:
                context.bot.send_message(chat_id=update.effective_chat.id, text=messages['no_questions'], reply_markup=ReplyKeyboardRemove())
                logging.info(f'User {suscriber.username} has no questions to answer')

                MessageJob(context, suscriber)
                return SECOND_STATE
                
        else:
            answers = PosibleAnswers.objects.filter(question=question)
            reply_markup = custom_keyboard(answers)
            context.bot.send_message(chat_id=update.effective_chat.id, text=messages['wrong_answer'], reply_markup=reply_markup)
            update.message.reply_text(f"{question.title}") 


        


def cancel(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Conversation canceled.")
    return ConversationHandler.END




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""                                                        ""
""                 'Conversational Handler'               ""
""                                                        ""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


question_handler = ConversationHandler(
    entry_points=[(CommandHandler('start', welcome))],
    states={
        FIRST_STATE: [MessageHandler(Filters.text & (~Filters.command), handle_answer)],
        SECOND_STATE: [MessageHandler(Filters.text & (~Filters.command), generate_response)],
        THIRD_STATE: [(MessageHandler(Filters.text, start_handler))],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    name="question_handler"
)

