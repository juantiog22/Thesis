from .handlers import *

class MessageJob(object):

    def __init__(self, context, suscriber):
        self.suscriber = suscriber
        self.create_job(context)
        

    def create_job(self, context):
        #Create a user's job
        context.job_queue.run_repeating(callback=self.job, interval=30, first=0, context=self.suscriber.chatid, name=self.suscriber.chatid)
        
        
    def job(self, context):
        # This function will be executed every 24 hours
        question = chooseQuestion(suscriber)
        if chooseQuestion(self.suscriber) is not None:
            context.bot.send_message(chat_id=self.suscriber.chatid, text=f"Hey {self.suscriber.name} tienes preguntas por responder. ¿Te gustaría empezar el cuestionario?")
    
    def remove_job(context, suscriber):
        for job in context.job_queue.jobs():
                if str(job.name) == str(suscriber.chatid):
                    job.schedule_removal()