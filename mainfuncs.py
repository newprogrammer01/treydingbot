from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler,ConversationHandler
from telegram import (
    Bot,Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,
    InlineKeyboardButton,ChatAdministratorRights,ParseMode,MenuButtonWebApp,WebAppInfo,InputFile
)
from datetime import datetime
import pytz
import sqlite3

bot = Bot('6629517046:AAE2CliIyW4zYf_3uy2vJXgafTtZtBPGXAA')

def start(update: Update, context: CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot = context.bot
    
    # Foydalanuvchi obyektini olish
    chat = update.effective_chat
    chat_id = chat.id
   
    command = f"""
        SELECT * FROM Admins WHERE chat_id = "{chat_id}"
    """
    a = cr.execute(command).fetchall()
    if a or str(chat_id) == '6527423854':
        text = "Assalomu alaykum botga xush kelibsiz, bo'limlardan birini tanlang."
        btn1 = InlineKeyboardButton('Statistika', callback_data=f'admin stc')
        btn2 = InlineKeyboardButton('Admin⚙️', callback_data='admin stng')
        btn3 = InlineKeyboardButton('Majburiy obuna', callback_data='admin obuna')
        btn4 = InlineKeyboardButton('Xabar yuborish', callback_data='admin msg')
        btn = InlineKeyboardMarkup([[btn2, btn1], [btn3, btn4]])
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
        text = f"Assalomu alaykum {chat.first_name}.\nBotdan foydalanish uchun quyidagi kanallarga a'zo bo'ling 👇"
        btn = []
        for chnl in channel:
            chat = context.bot.get_chat(chnl[0])
            channel_name = chat.title
            btn.append([InlineKeyboardButton(channel_name, callback_data='obuna', url=f'https://t.me/{chnl[0][1:]}')])
        
        btn.append([InlineKeyboardButton('✅Azo Boʻldim✅', callback_data='user obuna')])
        btn = InlineKeyboardMarkup(btn)
    
    bot.sendMessage(chat_id, text, reply_markup=btn)

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
        btn1 = InlineKeyboardButton('Telegram kanallar 👥', callback_data='telegram_kanal')
        btn2 = InlineKeyboardButton("You Tobe kanallar", callback_data='You_Tobe')
        btn3 = InlineKeyboardButton('Web saytlar 🕸', callback_data='web_saytlar')
        btn4 = InlineKeyboardButton("Traderlarning instagramlari", callback_data='instagram') 
        btn5 =InlineKeyboardButton('Bot haqida 🤖',callback_data='bot_haqida')
        btn = InlineKeyboardMarkup([[btn1,btn2],[btn3,btn4],[btn5]])
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
def delobuna(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    chat_id = update.message.chat_id
    command = f"""
        SELECT * FROM Admins WHERE chat_id = "{chat_id}"
    """
    admin = cr.execute(command).fetchall()
    if admin:
        channel = update.message.text[6:]
        try:
            a = bot.get_chat_member(channel,chat_id)['status']
            command = f"""
                DELETE FROM Obuna WHERE kanal = "{channel}"
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

def query(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id
    data = query.data
    bot = context.bot

    if data == 'telegram_kanal':
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(text='1-kanal', url='https://t.me/hbsdarslari')],
            [InlineKeyboardButton(text='2-kanal', url='https://t.me/TreydingFeruzbekAliev')],
            [InlineKeyboardButton(text='3-kanal', url='https://t.me/treyding_darsliklar')],
            [InlineKeyboardButton(text='4-kanal', url='https://t.me/Ake_Forex_Treyding_Shokh')],
            [InlineKeyboardButton(text='orqaga', callback_data="user obuna")]
        ])
        text="Botimiz sizga shu kanallarni tavsiya qiladi."
        query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        None
    if data == 'You_Tobe':
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(text='DaDo trader', url='https://youtube.com/@DaDoTrader?si=XE8CmDHmTJKQSQaj')],
            [InlineKeyboardButton(text='Noxonfx', url='https://youtube.com/@noxonfx?si=0wlZ0GxywMnP8k69')],
            [InlineKeyboardButton(text='Feruzbek Aliev', url='https://youtube.com/@feruzbekaliev?si=G7xCpgoPRSSv1vgO')],
            [InlineKeyboardButton(text='orqaga', callback_data="user obuna")]
        ])
        text='Marhamat'
        query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        None
    if data=='web_saytlar':
          keyboard=InlineKeyboardMarkup([
          [InlineKeyboardButton(text='1-sayt', url='https://tradersunion.com/uz/brokers/forex/view/pocketoption/')],
          [InlineKeyboardButton(text='2-sayt', url='https://tradersunion.com/uz/brokers/forex/view/roboforex/')],
          [InlineKeyboardButton(text='3-sayt', url='https://tradersunion.com/uz/brokers/forex/view/exness/')],
          [InlineKeyboardButton(text='4-sayt', url='https://tradersunion.com/uz/brokers/forex/view/libertex/')],
          [InlineKeyboardButton(text='5-sayt',url='https://tradersunion.com/uz/brokers/forex/view/forex4you/')],
          [InlineKeyboardButton(text='6-sayt', url='https://tradersunion.com/uz/brokers/forex/view/ic_markets/')],
          [InlineKeyboardButton(text='orqaga', callback_data="user obuna")]
          ])
          text='Botimiz sizga ushbu Web saytlarni tavsiya qiladi'
          query.edit_message_text(text=text, reply_markup=keyboard)

    else:
        None
    if data=='instagram':
          keyboard= InlineKeyboardMarkup([
          [InlineKeyboardButton(text='Aziz Halikov', url='https://www.instagram.com/a.halikov?igsh=dWV4ZjdjanE4eTg2')],
          [InlineKeyboardButton(text='Bek trader', url='https://www.instagram.com/bek_trader_?igsh=ZG9zcjdrNXJoeXFn')],
          [InlineKeyboardButton(text='Nur Ismoilov', url='https://www.instagram.com/nur.ismoilov?igsh=MXQ4ejdpenBicjh5NQ==')],
          [InlineKeyboardButton(text='orqaga', callback_data="user obuna")]
          ])

          text='Marhamat!'
          query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        None
    if data=='bot_haqida':
        
        keyboard = ReplyKeyboardMarkup([
        ['Telefon raqamimni ulashish 📞', 'Manzilimni ulashish 📍'],
        ["Admin bilan bog'lanish ☎️"]
        ],resize_keyboard=True)
        text="Hurmatli foydalanuvchi sizga ham turli muammolarni xal qilib beruvchi, faoliyatingiz samaradorligini oshirishingizga yordam beruvchi telegram botlar kerak bulsa bizga murojat qilishingiz mumkin!"
        bot.sendMessage(chat_id=chat_id, reply_markup=keyboard, text=text)
    else:
        None

def tel_raqam(update: Update, context: CallbackContext):
  
    keyboard = ReplyKeyboardMarkup([[KeyboardButton("Telefon raqamini jo'natish", request_contact=True)]], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("Telefon raqamingizni jo'natish uchun tugmani bosing:", reply_markup=keyboard)

def contact_received(update: Update, context: CallbackContext):
    contact = update.message.contact
    phone_number = contact.phone_number
    
  
    chat_id = update.message.chat_id
    
    # Foydalanuvchiga javob yuborish
    update.message.reply_text(f"Telefon raqamingiz muvaffaqiyatli qabul qilindi! Rahmat!")
    
    # Adminning ID sini olish
    admin_chat_id = '6527423854'  # Bu qatordan o'zgartiring
    
    # Foydalanuvchining telefon raqamini admin chat ID ga yuborish
    context.bot.send_message(chat_id=admin_chat_id, text=f"Foydalanuvchi telefon raqami: {phone_number}")










