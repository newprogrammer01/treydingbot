from telegram.ext import Updater,CommandHandler, CallbackContext,MessageHandler,Filters,CallbackQueryHandler,ConversationHandler
from mainfuncs import (
    start,check,adminstng,addadmin,deladmin,addobuna,userfun,reklama,delobuna,query,tel_raqam,contact_received
)

updater=Updater('6629517046:AAE2CliIyW4zYf_3uy2vJXgafTtZtBPGXAA')
dp = updater.dispatcher
dp.add_handler(CommandHandler('start',start))
dp.add_handler(MessageHandler(Filters.contact, contact_received))
dp.add_handler(CallbackQueryHandler(userfun,pattern='user'))
dp.add_handler(CallbackQueryHandler(adminstng,pattern='admin'))
dp.add_handler(MessageHandler(Filters.regex(r'^admin\+'),addadmin))
dp.add_handler(MessageHandler(Filters.regex(r'^admin\-'),deladmin))
dp.add_handler(MessageHandler(Filters.regex(r'^obuna\+'),addobuna))
dp.add_handler(MessageHandler(Filters.regex(r'^obuna\-'),delobuna))
dp.add_handler(MessageHandler(Filters.reply,reklama))
dp.add_handler(CallbackQueryHandler(query))
dp.add_handler(MessageHandler(Filters.text('Telefon raqamimni ulashish 📞'), tel_raqam))









updater.start_polling()
updater.idle()