from data import *
from functions import *

def adresse(update, contexte):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    update.message.reply_text(ask_adresse[RUE], reply_markup=ReplyKeyboardRemove())
    return RUE

def rue(update, context):
    #récupère l'adresse qu'on aura demandé dans commande.py
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    if user_input == "":
        update.message.reply_text(invalid_input)
        return RUE

    context.bot_data["users"][user_id]["rue"] = user_input
    update.message.reply_text(ask_adresse[CP], reply_markup=ReplyKeyboardRemove())
    return CP

def code_postal(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    if user_input == "":
        update.message.reply_text(invalid_input)
        return CP

    context.bot_data["users"][user_id]["code_postal"] = user_input
    update.message.reply_text(ask_adresse[VILLE], reply_markup=ReplyKeyboardRemove())
    return VILLE

def ville(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    if user_input == "":
        update.message.reply_text(invalid_input)
        return VILLE

    context.bot_data["users"][user_id]["ville"] = user_input
    update.message.reply_text(ask_adresse[COMP], reply_markup=ReplyKeyboardRemove())
    return COMP

def complements(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    context.bot_data["users"][user_id]["compléments"] = user_input

    update.message.reply_text(ask_adresse[NUM], reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def numero(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    if user_input == "":
        update.message.reply_text(invalid_input)
        return NUM

    context.bot_data["users"][user_id]["téléphone"] = user_input
    update.message.reply_text(ask_adresse[NOTE], reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(adresse_to_string(context.bot_data["users"][user_id]), reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(chgmt_adresse, reply_markup=ReplyKeyboardRemove())
    return VILLE
