from handlers import *
from job import *



def generate_response(update, context):

    user_response = update.message.text.lower()
    user = update.message.from_user

    suscriber = Suscriber.objects.get(chatid=user.id)

    random_var = random.randint(0,2)
    
    if user_response in greetings:
        context.bot.send_message(chat_id=user.id, text=messages['greetings'][str(random_var)])
    elif user_response in farewell:
        context.bot.send_message(chat_id=user.id, text=messages['farewell'][str(random_var)])
    elif user_response in gratitude:
        context.bot.send_message(chat_id=user.id, text=messages['gratitude'][str(random_var)])
    elif user_response in negation:
        context.bot.send_message(chat_id=user.id, text=messages['not'])
    elif user_response in affirmation:
        context.bot.send_message(chat_id=user.id, text=messages['redirect'])
        #Remove the user's job
        if context.job_queue.jobs():
            MessageJob.remove_job(context, suscriber)    
        return THIRD_STATE
    else:
        if chooseQuestion(suscriber):
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