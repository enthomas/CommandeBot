from data import *
from copy import deepcopy
from datetime import date
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import *
import time
from functions import *

def start(update, context):
    #initialise l'enregistrement de l'utilisateur
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if "users" in context.bot_data:
        if user_id not in context.bot_data["users"]:
            # logger.info("[/start] New user registering")
            context.bot_data["users"][user_id] = deepcopy(empty_user)
        else :
            context.bot.send_message(chat_id=chat_id, text=already_started)
            return ConversationHandler.END
    else:
        # logger.info("[/start] First user registered")
        context.bot_data["users"] = {user_id: deepcopy(empty_user)}
        context.bot_data["date"] = date.today().day
        context.bot_data["registration_open"] = True

    context.bot.send_message(chat_id=chat_id, text=intro)
    context.bot_data["users"][user_id]["nom"] = update.effective_user.name

    return update_id(update, context, first_time=True)

def update_id(update, context, first_time=False):
    #demande prénom
    update.message.reply_text(ask_data + ("\n"+inform_stop if not first_time else ""), reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(ask[PRENOM])
    return PRENOM

def prenom(update, context):
    #reçoit le prénom et demande le nom
    user_id = update.effective_user.id
    user_input = update.message.text[:30].strip().replace("\n", " ")

    if user_input == "":
        update.message.reply_text(invalid_input)
        return PRENOM

    context.bot_data["users"][user_id]["prénom"] = user_input
    update.message.reply_text(ask[NOM])
    return NOM

def nom(update, context):
    #reçoit le nom et demande la promo
    user_id = update.effective_user.id
    user_input = update.message.text[:30].strip().replace("\n", " ")

    if user_input == "":
        update.message.reply_text(invalid_input)
        return NOM

    context.bot_data["users"][user_id]["nom"] = user_input
    keyboard = [[KeyboardButton(prom)] for prom in promos]
    update.message.reply_text(ask[PROMO], reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return PROMO

def promo(update, context):
    #reçoit promo et demande pseudo
    user_id = update.effective_user.id
    user_input = update.message.text[:30].strip().replace("\n", " ")

    if user_input not in promos:
        update.message.reply_text(invalid_input)
        return PROMO
    context.bot_data["users"][user_id]["promo"] = user_input
    update.message.reply_text(ask[FIN])
    context.bot_data["users"][user_id]["enregistrement"] = time.time()
    context.bot_data["users"][user_id]["fin"] = time.time()-2

    user_str = user_id_str(context.bot_data["users"][user_id])
    update.message.reply_text(recap_data + "\n" + user_str + "\n" + incorrect_data)
    update.message.reply_text(finish_start)
    print(context.bot_data["users"][user_id]["prénom"] + ' ' + context.bot_data["users"][user_id]["nom"] + " s'est inscrit.\n")
    #context.bot.send_message(chat_id=id_BDAmour, text=context.bot_data["users"][user_id]["prénom"] + ' ' + context.bot_data["users"][user_id]["nom"] + " s'est inscrit.")

    return ConversationHandler.END
