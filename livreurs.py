from telegram.ext import *
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import time

from data import *
from functions import *

def livraison(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if not context.bot_data["users"][user_id]["admin"] :
        update.message.reply_text("Tututut, cette commande n'est pas faite pour toi 😜\nEssaye plutôt \help pour savoir ce que tu peux faire")
    elif context.bot_data["users"][user_id]["team"] == "Team Bordeaux" :
        keyboard = [[KeyboardButton(livraison_to_string(id, context))] for id in context.bot_data["attribuees_teamB"]]
        update.message.reply_text("Qui as-tu livré ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        return LIVB
    else :
        keyboard = [[KeyboardButton(livraison_to_string(id, context))] for id in context.bot_data["attribuees_teamT"]]
        update.message.reply_text("Qui as-tu livré ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        return LIVT

def livB(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    lst = [livraison_to_string(id, context) for id in context.bot_data["attribuees_teamB"]]
    if not user_input in lst :
        update.message.reply_text(invalid_input)
        return LIVB
    ind = lst.index(user_input)
    id_user = context.bot_data["attribuees_teamB"][ind]

    update.message.reply_text(commande_to_string(context.bot_data["users"][id_user]))
    keyboard = [[KeyboardButton(choix)] for choix in ["Oui ({})".format(id_user), "Non ({})".format(id_user)]]
    update.message.reply_text("C'est bien cette commande ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return CONFB

def confB(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    if user_input[:3] not in ["Oui", "Non"] :
        update.message.reply_text(invalid_input)
        return CONFB
    id_user = int(user_input[5:-1])

    if user_input[:3] == "Oui" :
        context.bot_data["attribuees_teamB"].remove(id_user)
        context.bot_data["livrees"].append(id_user)
        context.bot_data["users"][id_user]["livre"] = True
        update.message.reply_text("Nickel c'est noté !")
        return ConversationHandler.END
    else :
        return livraison(update, context)

def livT(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    lst = [livraison_to_string(id, context) for id in context.bot_data["attribuees_teamT"]]
    if not user_input in lst :
        update.message.reply_text(invalid_input)
        return LIVT
    ind = lst.index(user_input)
    id_user = context.bot_data["attribuees_teamT"][ind]

    update.message.reply_text(commande_to_string(context.bot_data["users"][id_user]))
    keyboard = [[KeyboardButton(choix)] for choix in ["Oui ({})".format(id_user), "Non ({})".format(id_user)]]
    update.message.reply_text("C'est bien cette commande ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return CONFT

def confT(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    if user_input[:3] not in ["Oui", "Non"] :
        update.message.reply_text(invalid_input)
        return CONFT
    id_user = int(user_input[5:-1])

    if user_input[:3] == "Oui" :
        context.bot_data["attribuees_teamT"].remove(id_user)
        context.bot_data["livrees"].append(id_user)
        context.bot_data["users"][id_user]["livre"] = True
        update.message.reply_text("Nickel c'est noté !")
        return ConversationHandler.END
    else :
        return LIVT

def recap_team(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if not context.bot_data["users"][user_id]["admin"] :
        update.message.reply_text("Tututut, cette commande n'est pas faite pour toi 😜\nEssaye plutôt \help pour savoir ce que tu peux faire")
    elif context.bot_data["users"][user_id]["team"] == "Team Bordeaux" :
        message = ""
        for id in context.bot_data["attribuees_teamB"] :
            message += commande_to_string(context.bot_data["users"][id])
            message += "\n\n-----------\n\n"
        update.message.reply_text(message)
    else :
        message = ""
        for id in context.bot_data["attribuees_teamT"] :
            message += commande_to_string(context.bot_data["users"][id])
            message += "\n\n-----------\n\n"
        update.message.reply_text(message)
    return ConversationHandler.END
