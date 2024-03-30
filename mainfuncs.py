from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler,ConversationHandler
from telegram import (
    Bot,Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,
    InlineKeyboardButton,ChatAdministratorRights,ParseMode,MenuButtonWebApp,WebAppInfo,InputFile
)
from datetime import datetime
import pytz
import sqlite3

bot = Bot('7102898210:AAFng9mqV3LgKefWnKgL06zW9BZQkXEfRZo')

def start(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    chat_id = update.message.chat_id
    command = f"""
        SELECT * FROM Admins WHERE chat_id = "{chat_id}"
    """
    a=cr.execute(command).fetchall()
    if a or str(chat_id)=='6527423854':
        text = "Assalomu alaykum botga xush kelibsiz, bo'limlardan birini tanlang."
        btn1 = InlineKeyboardButton('Statistika',callback_data=f'admin stc')
        btn2 = InlineKeyboardButton('Admin⚙️',callback_data='admin stng')
        btn3 = InlineKeyboardButton('Majburiy obuna',callback_data='admin obuna')
        btn4 = InlineKeyboardButton('Xabar yuborish',callback_data='admin msg')
        btn = InlineKeyboardMarkup([[btn2,btn1], [btn3,btn4]])
    else:
        command = f"""
        SELECT * FROM Users WHERE chat_id = "{chat_id}"
        """
        b = cr.execute(command).fetchall()
        if not b:
            command = f"""
            INSERT INTO Users (chat_id) VALUES ("{chat_id}")
            """
            cr.execute(command)
            cnt.commit()
        command = f"""
        SELECT kanal FROM Obuna
        """
        channel = cr.execute(command).fetchall()
        text = f"Assalomu alaykum {update.message.from_user.first_name}.\nBotdan foydalanish uchun quyidagi kanallarga a'zo bo'ling 👇"
        btn=[]
        for chnl in channel:
            chat = context.bot.get_chat(chnl[0])
            channel_name = chat.title
            btn.append([InlineKeyboardButton(channel_name,callback_data='obuna',url=f'https://t.me/{chnl[0][1:]}')])
        btn.append([InlineKeyboardButton('✅Azo Boʻldim✅',callback_data='user obuna')])
        btn = InlineKeyboardMarkup(btn)
    bot.sendMessage(chat_id,text,reply_markup=btn)
def check(chat_id,bot,channels):
    for channel in channels:
        chan1=bot.getChatMember(channel[0],str(chat_id))['status']
        if chan1=='left':
            return False
    return True
def userfun(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot = context.bot
    b = query.data.split(' ')[1]
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    command = f"""
        SELECT kanal FROM Obuna
        """
    channel = cr.execute(command).fetchall()
    a = check(chat_id,bot, channel)
    bot.delete_message(chat_id,msg)
    if a:
        text = "Obuna mufavaqiyatli amalga oshirildi!\nBo'limlardan birini tanlang."
        btn1 = InlineKeyboardButton('Video darsliklar', callback_data='v_dars')
        btn2 = InlineKeyboardButton("Video darsliklar qo'shish", callback_data='vido +') 
        btn = InlineKeyboardMarkup([[btn1,btn2]])
        bot.sendMessage(chat_id, text, reply_markup=btn)
    else:
        bot.sendMessage(chat_id, "Obuna bo'lishda xatolik ❌")

def adminstng(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    b = query.data.split(' ')[1]
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    if b=='stc':
        command = """
        SELECT COUNT(id) FROM Users
        """
        res = cr.execute(command).fetchone()[0]
        text = f"Botdagi foydalanuvchilar umumiy soni: {res}"
        bot.sendMessage(chat_id,text) 
    elif b =='stng':
        text = "Yangi admin qo'shish uchun\n```admin+user_id```\n\nAdmin o'chirish uchun\n```admin-user_id``"
        bot.sendMessage(chat_id,text)
    elif b == 'obuna':
        text = "Majburiy obuna qo'shish uchun avval botni kanal(guruh)ga to'liq admin qilasiz va quyidagicha ulaysiz:\n```obuna+@username```"
        bot.sendMessage(chat_id,text,parse_mode=ParseMode.MARKDOWN)
    else:
        text = "Foydalanuvchilarga xabar jo'natish uchun yubormoqchi bo'lgan xabaringizga *send* so'zini reply qilib yozing"
        bot.sendMessage(chat_id,text,parse_mode=ParseMode.MARKDOWN)   
def addadmin(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    chat_id = update.message.chat_id
    command = f"""
        SELECT * FROM Admins WHERE chat_id = "{chat_id}"
    """
    admin = cr.execute(command).fetchall()
    if admin or str(chat_id)=='6527423854':
        user_id = update.message.text[6:]
        command = f"""
        INSERT INTO Admins (chat_id) VALUES ("{user_id}")
        """
        cr.execute(command)
        cnt.commit()
        bot.send_message(chat_id,'✅')
def deladmin(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    chat_id = update.message.chat_id
    command = f"""
        SELECT * FROM Admins WHERE chat_id = "{chat_id}"
    """
    admin = cr.execute(command).fetchall()
    if admin or str(chat_id)=='6527423854':
        user_id = update.message.text[6:]
        try:
            a=cr.execute(f'DELETE FROM Admins WHERE chat_id = "{user_id}"').fetchall()
            cnt.commit()
            bot.sendMessage(chat_id,'☑️')
        except:
            bot.sendMessage(chat_id,'Qandaydir xatolik')
def addobuna(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    chat_id = update.message.chat_id
    command = f"""
        SELECT * FROM Admins WHERE chat_id = "{chat_id}"
    """
    admin = cr.execute(command).fetchall()
    if admin or str(chat_id)=='6527423854':
        channel = update.message.text[6:]
        try:
            a = bot.get_chat_member(channel,chat_id)['status']
            command = f"""
                INSERT INTO Obuna (kanal) VALUES ("{channel}")
            """
            cr.execute(command)
            cnt.commit()
            bot.sendMessage(chat_id,'✅')
        except:
            bot.sendMessage(chat_id,'Qandaydir xatolik')

def reklama(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    original_message = update.message.reply_to_message
    text = update.message.text
    
    chat_id = update.message.chat_id
    command0 = f"""
     SELECT chat_id FROM Users
    """
    command = f"""
        SELECT * FROM Admins WHERE chat_id = "{chat_id}"
    """
    admin = cr.execute(command).fetchall()
    if admin or str(chat_id)=='6527423854':
        if text=='send':
            users = cr.execute(command0).fetchall()
            i=0
            for user in users:
                try:
                    context.bot.forward_message(chat_id=user[0], from_chat_id=original_message.chat_id, message_id=original_message.message_id)
                    i+=1
                except:
                    pass
            bot.send_message(chat_id,f'{i} ta foydalanuvchiga xabar yuborildi')
