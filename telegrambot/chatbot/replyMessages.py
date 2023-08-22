
#APPROVAL
affirmation = ['si', 'ok', 'vale', 'claro', 'okey', 'venga', 'yes', 'supuesto', 'efectivamente', 'absolutamente', 'course']
negation = ['no', 'nunca', 'jamas', 'jamás', 'ninguna', 'tampoco', 'ni', 'not']


#HELLO AND GOOD BYE
greetings = ['hola', 'hello', 'buenos dias', 'buenos días', 'buenas tardes', 'dias', 'tardes', 'buenos', 'buenas', 'saludos', 'hi', 'good', 'que', 'tal']
farewell = ['adios', 'adiós', 'bye', 'good bye', 'hasta', 'luego', 'vemos', 'pronto', 'buenas noches', 'noches', 'proxima', 'vaya']

#THANKS
gratitude = ['gracias', 'thanks', 'thank you', 'aprecio', 'lo agradezco']

#CREDENTIALS
name = ['llamas', 'nombre', 'llamabas']


#MOOD
mood = ['tal', 'estas', 'sientes', 'estas', 'estás']

#MOOD
goodmood = ['bien', 'contento', 'alegre', 'feliz', 'excelente', 'genial', 'maravilloso', 'aliviado', 'animado']
badmood = ['mal', 'triste', 'cansado', 'enfadado', 'enojado', 'herido', 'furioso', 'irritado']

#JOKE
joke = ['broma', 'chiste', 'burla', 'mofa']

#ASK ABOUT HELP
help = ['ayuda']

#START QUESTIONARY
redirect = ['empezar']


#ABOUT ME
contact = ['quien']


messages = {

    'welcome': 'Bienvenido a POSTCOVID-AI TelegramBot. Soy un bot conversacional diseñado para ayudar y evaluar el bienestar general de la población',

    'confidential_information': 'Toda la información que me proporciones será tratada de manera confidencial y no se compartirá con nadie más sin tu consentimiento',

    'question_explanation': 'Por favor, responde a las siguientes preguntas seleccionando la opción que consideres',

    'whoami': 'Soy POSTCOVID-AI TelegramBot.Un bot conversacional diseñado para ayudar y evaluar el bienestar general de la población',

    'purpose': 'POSTCOVID-AI ayudará a identificar indicadores cuantitativos a través del desarrollo de una novedosa plataforma inteligente para la adquisición y análisis en tiempo real de datos sociales, conductuales y emocionales, gracias a la cual será posible medir el impacto del contexto diario posterior a COVID-19 en el bienestar de la población española',

    'contact': 'Puedes contactar con nosotros mandandónos un correo a postcovid.ai@gmail.com o a través de Twitter @POSTCOVIDai',

    'redirect': 'Redireccionando al cuestionario. Por favor escriba "si" para continuar',

    'frecuent_quest': 'Lo siento no te entiendo. Aquí tienes algunas preguntas frecuentes por si tienes alguna duda',

    'questions_pending': 'Lo siento no te entiendo. Por cierto tienes preguntas pendientes ¿Te gustaría empezar el cuestionario?',

    'no_questions': 'Gracias por tu respuestas, por ahora no tengo más preguntas para hacerte!',

    'wrong_answer':'Respuesta incorrecta. Por favor selecciona una de las proporcionadas',

    'greetings':{
        '0': 'Hola!¿Que tal estas?',
        '1': 'Muy buenas!¿Como estas hoy?',
        '2': 'Hola!¿Como puedo asistirte hoy?'
    },
    'farewell':{
        '0': '¡Adiós!.¡Que tengas un buen día!',
        '1': 'Hasta luego!.¡Espero verte de nuevo pronto!',
        '2': 'Adiós. !No dudes en volver!',
    },
    'gratitude':{
        '0': '¡De nada!.¡Ha sido un placer ayudarte!',
        '1': '¡De nada!.¡Si tienes alguna pregunta no dudes en preguntarme!', 
        '2': '¡De nada!.¡Me programaron para ayudar!', 
    },
    'negation':{
        '0': 'Entiendo. Si tienes alguna pregunta o necesitas algo estaré aquí para asistirte',
        '1': 'De acuerdo, si necesitas cualquier cosa aquí estaré',
        '2': 'Vale. Aquí estoy por si necesitas cualquier cosa',
    },
    'goodmod':{
        '0': '¡Me alegra que estés de buen humor!',
        '1': '¡Increíble! Cuando estás de buen humor, todo parece más brillante',
        '2': 'Tu buen humor me alegra también.',
    },
    'badmood':{
        '0': 'Lamento escuchar que no estás teniendo un buen día. Recuerda que a veces es útil hablar sobre lo que nos preocupa',
        '1': 'Sé que no puedo cambiar lo que estás experimentando, pero puedo contarte un chiste',
        '2': 'La vida tiene sus altibajos. Espero que pronto encuentres un poco de luz en tu día',
    },
    'joke':{
        '0': '¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter',
        '1': '¿Qué le dice el semáforo al coche? No me mires me estoy cambiando',
        '2': '¿Por qué los esqueletos no pelean entre ellos?, Porque tienen "buena estructura" de convivencia.',
    },
    'name':{
        '0': 'Mi nombre es POSTCOVID-AI TelegramBot',
    },
    'mood':{
        '0': 'Estoy muy bien, gracias por preguntar'
    }
}