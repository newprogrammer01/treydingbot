from telegram.ext import Updater,CommandHandler, CallbackContext,MessageHandler,Filters,CallbackQueryHandler,ConversationHandler
from mainfuncs import (
    start,check,adminstng,addadmin,deladmin,addobuna,userfun,reklama
)

updater=Updater('7102898210:AAFng9mqV3LgKefWnKgL06zW9BZQkXEfRZo')
dp = updater.dispatcher
dp.add_handler(CommandHandler('start',start))
dp.add_handler(CallbackQueryHandler(userfun,pattern='user'))
dp.add_handler(CallbackQueryHandler(adminstng,pattern='admin'))
dp.add_handler(MessageHandler(Filters.regex(r'^admin\+'),addadmin))
dp.add_handler(MessageHandler(Filters.regex(r'^admin\-'),deladmin))
dp.add_handler(MessageHandler(Filters.regex(r'^obuna\+'),addobuna))
dp.add_handler(MessageHandler(Filters.reply,reklama))

updater.start_polling()
updater.idle()