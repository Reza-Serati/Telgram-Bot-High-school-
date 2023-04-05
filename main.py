import html
import json
import logging
import traceback

from telegram import Bot
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ParseMode
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Updater


# @mehregan_shcool_bot 
TOKEN = '1183914796:AAF_A8js1y44v2CWcG8pHU4NSg8tf5M0iZo'
# mehregan_chnnael
CHANNEL_ID = '@mehreeeeegan'
CHANNEL_ID = -1001369818361


logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TWELVE, ELEVEN, TEN, NINE, EIGHT, SEVEN = map(chr, range(6))
GRADE, CHOICE = map(chr, range(6, 8))
YES, NO = map(chr, range(8, 10))
ELEMENTARY, HIGHSCHOOL = map(chr, range(10, 12))

JOZVE, SOAL, VIDEO, KETAB, NAZARI, KARODANESH, NAZARI_KARODANESH = map(chr, range(12, 19))


ARABI_7_8_9, FARHANG_O_HONAR_7_8_9, FARSI_7_8_9, OLOOM_7_8_9,  \
ZABAN_7_8_9, MOTALEAT_7_8_9, KAR_O_FANAVARI_7_8_9, \
PAYAMYAYE_ASEMANI_7_8_9, RIAZI_7_8_9, TAFAKOR_7_8_9, QURAN_7_8_9, NEGARESH_7_8_9, \
DEFAEE_9 = map(chr, range(19,32))

def reset_user_data(context, grade=True, choice=True, lesson=True, 
	nazari_karodanesh=True, elementary=True, highschool=True):
	
	if grade:
		context.user_data['GRADE'] = False
	if choice:
		context.user_data['CHOICE'] = False
	if lesson:
		context.user_data['LESSON'] = False
	if nazari_karodanesh:
		context.user_data['NAZARI_KARODANESH'] = False
	if elementary:
		context.user_data['ELEMENTARY'] = False
	if highschool:
		context.user_data['HIGHSCHOOL'] = False


def error_handler(update: Update, context: CallbackContext):
	logger.error(msg="Exception while handling an update:", exc_info=context.error)	

	tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
	tb = ''.join(tb_list)

	message = (
			"An exception was raised while handlign an update\n"
			# "<pre>update = {}</pre>\n\n"
			# "<pre>context.chat_data = {}</pre>\n\n"
			# "<pre>context.user_data = {}</pre>\n\n"
			"<pre>{}</pre>"
		).format(
			# html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
			# html.escape(str(context.chat_data)),
			# html.escape(str(context.user_data)),
			html.escape(tb)
		)

	context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)

def start(update:Update, context:CallbackContext):

	logger.info('Start')
	text = "لطفا مقطع تحصیلی خود را انتخاب کنید"
	buttons=[[
		InlineKeyboardButton(text='ﯾﺎﺯﺩﻫﻢ', callback_data=str(ELEVEN)),
		InlineKeyboardButton(text='ﺩﻭاﺯﺩﻫﻢ', callback_data=str(TWELVE)),
	], [
		InlineKeyboardButton(text='ﻧﻬﻢ', callback_data=str(NINE)),
		InlineKeyboardButton(text='ﺩﻫﻢ', callback_data=str(TEN)),
	],[
		InlineKeyboardButton(text='ﻫﻔﺘﻢ', callback_data=str(SEVEN)),
		InlineKeyboardButton(text='ﻫﺸﺘﻢ', callback_data=str(EIGHT)),
		
	]]
	keyboard = InlineKeyboardMarkup(buttons)
	update.message.reply_text(text=text, reply_markup=keyboard)

	reset_user_data(context)

	return GRADE

def to_string_grade(grade):
	text = 'مقطع: '
	if grade == 7:
		text += 'هفتم 7️⃣'
	elif grade == 8:
		text += 'هشتم 8️⃣'
	elif grade == 9:
		text += 'نهم 9️⃣'
	elif grade == 10:
		text += 'دهم 0️⃣1️⃣'
	elif grade == 11:
		text += 'یازدهم 1️⃣1️⃣'
	elif grade == 12:
		text += 'دوازدهم 2️⃣1️⃣'
	else:
		text += 'ناموجود'

	return text
def to_string_choice2(choice):
	text = ' - '
	if choice == 'Nazari':
		text += 'نظری 👨‍🎓'
	elif choice == 'Karodanesh':
		text += 'کارودانش 👨‍🏫'
	else:
		text += 'ناموجود'
	return text	
def to_string_choice(choice):
	text = '\nدرخواست: '
	if choice == 'Jozve':
		text += 'جزوه📘'
	elif choice == 'Ketab':
		text += 'کتاب📕'
	elif choice == 'Video':
		text += 'ویدئو🎦'
	elif choice == 'Soal':
		text += 'نمونه سوال📝'
	else:
		text += 'ناموجود'
	text += '\n'
	return text


def pretty_print(context):
	# logger.info(context.user_data)
	text = to_string_grade(context.user_data['GRADE'])
	if context.user_data['HIGHSCHOOL']:
		text += to_string_choice2(context.user_data['NAZARI_KARODANESH'])

	
	text += to_string_choice(context.user_data['CHOICE'])
	
	return text

def fetch_user_grade(context):
	str_ = context.match.string
	grade = 0
	# these conditions are, location of the selected item in 
	# 	inline keboard
	if str_ == '\x00':
		grade = 12
	elif str_ == '\x01':
		grade = 11
	elif str_ == '\x02':
		grade = 10
	elif str_ == '\x03':
		grade = 9
	elif str_ == '\x04':
		grade = 8
	elif str_ == '\x05':
		grade = 7

	reset_user_data(context, grade=False)
	if context.user_data['GRADE'] == False:
		context.user_data['GRADE'] = grade

def get_user_grade(update:Update, context:CallbackContext):

	context.user_data['ELEMENTARY'] = False
	if context.user_data['NAZARI_KARODANESH'] == False:
		fetch_user_grade(context)
		context.user_data['HIGHSCHOOL'] = False


	# logger.info("user's grade: {}".format(context.user_data['GRADE']))
	text = to_string_grade(context.user_data['GRADE'])
	if context.user_data['NAZARI_KARODANESH'] != False: 
		text += to_string_choice2(context.user_data['NAZARI_KARODANESH'])
		text += '\n'
		
	else:
		text += '\n'
		
	

	if context.user_data['GRADE'] >  9 and context.user_data['NAZARI_KARODANESH'] == False:
		context.user_data['HIGHSCHOOL'] = True
		context.user_data['NAZARI_KARODANESH'] = False
		text += "لطفا گرایش خود را انتخاب کنید"
		buttons=[[
			InlineKeyboardButton(text='نظری', callback_data=str(NAZARI)),
			InlineKeyboardButton(text='کارودانش', callback_data=str(KARODANESH)),
		]]

	else:
		if context.user_data['NAZARI_KARODANESH'] == False:
			context.user_data['ELEMENTARY'] = True
		text += "لطفا درخواست خود را انتخاب کنید"
		buttons=[[
			InlineKeyboardButton(text='نمونه سوال', callback_data=str(SOAL)),
			InlineKeyboardButton(text='جزوه', callback_data=str(JOZVE)),
		], [
			InlineKeyboardButton(text='کتاب', callback_data=str(KETAB)),
			InlineKeyboardButton(text='ویدئو', callback_data=str(VIDEO)),
		]]
		
	keyboard = InlineKeyboardMarkup(buttons)

	
	update.callback_query.answer()
	update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

	return CHOICE
		
def fetch_user_choice(context):
	str_ = context.match.string
	choice = ''
	# these conditions are, location of the selected item in 
	# 			inline keboard
	if(context.user_data['HIGHSCHOOL']):
		if context.user_data['NAZARI_KARODANESH'] != False:
			if str_ == '\x0c':
				choice = 'Jozve'
			elif str_ == '\r':
				choice = 'Soal'
			elif str_ == '\x0e':
				choice = 'Video'
			elif str_ == '\x0f':
				choice = 'Ketab'
		else:
			if str_ == '\x11':
				choice = 'Karodanesh'
			elif str_ == '\x10':
				choice = 'Nazari'
			context.user_data['NAZARI_KARODANESH'] = choice
			return
			
	if(context.user_data['ELEMENTARY']):
		if str_ == '\x0c':
			choice = 'Jozve'
		elif str_ == '\r':
			choice = 'Soal'
		elif str_ == '\x0e':
			choice = 'Video'
		elif str_ == '\x0f':
			choice = 'Ketab'
			
	if context.user_data['CHOICE'] == False:
		context.user_data['CHOICE'] = choice
def get_user_choice(update:Update, context:CallbackContext):
	fetch_user_choice(context)

	if context.user_data['HIGHSCHOOL']:
	 	if context.user_data['NAZARI_KARODANESH'] != False:
	 		if context.user_data['CHOICE'] == False:
	 			get_user_grade(update, context)
	 			return

	show_lesson(update, context)

def fetch_continue_asking(update:Update, context:CallbackContext):
	str_ = context.match.string
	if str_ == '\x08': #yes
		# get_user_choice(update, context)
		get_user_grade(update, context)
	elif str_ == '\t':
		update.callback_query.answer()
		update.callback_query.edit_message_text(text='موفق باشید\n/start')
def continue_asking(update:Update, context:CallbackContext, count):
	text ='{} مورد یافت شد'.format(count)
	text += '\nآیا درخواست دیگری دارید؟'
	buttons=[[
		InlineKeyboardButton(text='خیر', callback_data=str(NO)),
		InlineKeyboardButton(text='بلی' , callback_data=str(YES)),
	]]

	keyboard = InlineKeyboardMarkup(buttons)
	# update.message.reply_text(text=text, reply_markup=keyboard)
	context.bot.send_message(chat_id=update.effective_chat.id, text=text, 
		reply_markup=keyboard)
	# update.callback_query.answer()
	# update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
	# return YES_NO

def return_user_file(update:Update, context:CallbackContext):
	
	grade = context.user_data['GRADE']
	choice = context.user_data['CHOICE']
	choice2 = context.user_data['NAZARI_KARODANESH']
	lesson = context.user_data['LESSON']
	chat_id = update.effective_chat.id
	bot = Bot(token=TOKEN)


	if context.user_data['ELEMENTARY']:
		path = 'Files/{}/{}/{}/list.txt'.format(grade, choice, lesson)
	elif context.user_data['HIGHSCHOOL']:
		path = 'Files/{}/{}/{}/{}/list.txt'.format(grade, choice2, choice, lesson)
	# logger.info(path)
	f = open(path, "r")
	list=[]
	for x in f.readlines():
		list.append(int(x))
	# logger.info(list)
	count = 0
	if not list:
		context.bot.send_message(chat_id= chat_id, text='برای درخواست شما، فایلی پیدا نشد')
	else:
		for x in list:
			count = count+1
			bot.forward_message(chat_id= chat_id, from_chat_id= CHANNEL_ID,  message_id =x)
	

	update.callback_query.answer()

	continue_asking(update, context, count)

def fetch_elementary(update:Update, context:CallbackContext):
	str_ = context.match.string
	# logger.info(context.match)
	lesson = None
	
	if str_ == '\x13':
		lesson = 'Arabi'
	elif str_ == '\x14':
		lesson = 'Farhang_o_honar'
	elif str_ == '\x15':
		lesson = 'Farsi'
	elif str_ == '\x16':
		lesson = 'Oloom'
	elif str_ == '\x17':
		lesson = 'Zaban'
	elif str_ == '\x18':
		lesson = 'Motaleat'
	elif str_ == '\x1a':
		lesson = 'Payamhaye_asemani'
	elif str_ == '\x1b':
		lesson = 'Riazi'
	elif str_ == '\x1c':
		lesson = 'Tafakor_va_sabke_zendegi'
	elif str_ == '\x19':
		lesson = 'Kar_o_fanavaro'
	elif str_ == '\x1d':
		lesson = 'Qoran'
	elif str_ == '\x1e':
		lesson = 'Negaresh'
	elif str_ == '\x1f':
		lesson = 'Defaee'

	context.user_data['LESSON'] = lesson
	
	return_user_file(update, context)
def show_elementary(context):
	buttons=[[
		InlineKeyboardButton(text='پیامهای آسمانی', callback_data=str(PAYAMYAYE_ASEMANI_7_8_9)),
		InlineKeyboardButton(text='تفکر و سبک زندگی', callback_data=str(TAFAKOR_7_8_9)),
	], [
		InlineKeyboardButton(text='فرهنگ و هنر', callback_data=str(FARHANG_O_HONAR_7_8_9)),
		InlineKeyboardButton(text='علوم', callback_data=str(OLOOM_7_8_9)),
	],[
		InlineKeyboardButton(text='قرآن', callback_data=str(QURAN_7_8_9)),
		InlineKeyboardButton(text='عربی', callback_data=str(ARABI_7_8_9))
	],[
		InlineKeyboardButton(text='زبان انگلیسی', callback_data=str(ZABAN_7_8_9)),
		InlineKeyboardButton(text='ریاضی', callback_data=str(RIAZI_7_8_9))
	],[
		InlineKeyboardButton(text='فارسی', callback_data=str(FARSI_7_8_9)),
		InlineKeyboardButton(text='نگارش', callback_data=str(NEGARESH_7_8_9)),
	],[
		InlineKeyboardButton(text='مطالعات اجتماعی', callback_data=str(MOTALEAT_7_8_9)),
		InlineKeyboardButton(text='کار و فناوری', callback_data=str(KAR_O_FANAVARI_7_8_9)),
	]]
	if context.user_data['GRADE'] == 9:
		buttons.append([InlineKeyboardButton(text='آمادگی دفاعی', callback_data=str(DEFAEE_9))
			])
	keyboard = InlineKeyboardMarkup(buttons)
	return keyboard

def show_lesson(update:Update, context:CallbackContext):
	text = pretty_print(context)
	# logger.info(context.user_data)
	text += 'لطفا درس مورد نظر خود را انتخاب کنید'

	keyboard = None
	if context.user_data['ELEMENTARY'] == True:
		keyboard = show_elementary(context)



	update.callback_query.answer()
	update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

def main():	
	updater = Updater(token=TOKEN, use_context=True)
	dp = updater.dispatcher


	selection_handlers=[
		CallbackQueryHandler(fetch_elementary, 
					pattern='^{}$|^{}$|^{}$|^{}$|^{}$|^{}$|^{}$|^{}$|^{}$|^{}$|^{}$|^{}$|^{}$'.format(
							str(FARHANG_O_HONAR_7_8_9), str(FARSI_7_8_9), str(OLOOM_7_8_9),
							str(ZABAN_7_8_9), str(MOTALEAT_7_8_9), str(KAR_O_FANAVARI_7_8_9), 
							str(PAYAMYAYE_ASEMANI_7_8_9), str(RIAZI_7_8_9), str(TAFAKOR_7_8_9), 
							str(QURAN_7_8_9), str(NEGARESH_7_8_9), str(ARABI_7_8_9), str(DEFAEE_9))),
		CallbackQueryHandler(get_user_choice, 
					pattern='^{}$|^{}$|^{}$|^{}$'.format(
							str(JOZVE), str(SOAL), str(KETAB), str(VIDEO))),
		CallbackQueryHandler(get_user_choice, 
					pattern='^{}$|^{}$'.format(str(KARODANESH), str(NAZARI))),
		CallbackQueryHandler(fetch_continue_asking, 
					pattern='^{}$|^{}$'.format(str(YES), str(NO))),
	]

	# show_elementary('asd')
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start)],
		states={
			# LESSON:		selection_handlers,	

			GRADE:		[CallbackQueryHandler(get_user_grade,
							pattern='^{}$|^{}$|^{}$|^{}$|^{}$|^{}$'.format(
							str(SEVEN), str(EIGHT), str(NINE), str(TEN), str(ELEVEN), str(TWELVE)),
						)],	
			CHOICE: 		selection_handlers,
			# YES_NO: 	selection_handlers,
			},
		fallbacks=[CommandHandler('start', start)]
	)

	dp.add_handler(conv_handler)
	# dp.add_error_handler(error_handler)


	logger.info("Bot Starting")
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()