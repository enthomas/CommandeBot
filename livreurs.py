from telegram.ext import *
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import time

from data import *
from functions import *

def livraison(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if not context.bot_data["users"][user_id]["admin"] :
        update.message.reply_text(tututut)
        return ConversationHandler.END
    elif context.bot_data["users"][user_id]["team"] == "Team Bordeaux" :
        if len(context.bot_data["attribuees_teamB"]) > 0 :
            keyboard = [[KeyboardButton(livraison_to_string(id, context))] for id in context.bot_data["attribuees_teamB"]]
            update.message.reply_text("Qui as-tu livré ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
            return LIVB
        else :
            update.message.reply_text(lst_vide)
            return ConversationHandler.END
    else :
        if len(context.bot_data["attribuees_teamT"]) > 0 :
            keyboard = [[KeyboardButton(livraison_to_string(id, context))] for id in context.bot_data["attribuees_teamT"]]
            update.message.reply_text("Qui as-tu livré ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
            return LIVT
        else :
            update.message.reply_text(lst_vide)
            return ConversationHandler.END

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
        update.message.reply_text(tututut)
    elif context.bot_data["users"][user_id]["team"] == "Team Bordeaux" :
        if len(context.bot_data["attribuees_teamB"]) > 0 :
            message = ""
            for id in context.bot_data["attribuees_teamB"] :
                message += commande_to_string(context.bot_data["users"][id])
                message += "\n\n-----------\n\n"
            update.message.reply_text(message)
        else :
            update.message.reply_text(lst_vide)
    else :
        if len(context.bot_data["attribuees_teamT"]) > 0 :
            message = ""
            for id in context.bot_data["attribuees_teamT"] :
                message += commande_to_string(context.bot_data["users"][id])
                message += "\n\n-----------\n\n"
            update.message.reply_text(message)
        else :
            update.message.reply_text(lst_vide)
    return ConversationHandler.END

def abandonner(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if not context.bot_data["users"][user_id]["admin"] :
        update.message.reply_text(tututut)
        return ConversationHandler.END
    elif context.bot_data["users"][user_id]["team"] == "Team Bordeaux" :
        if len(context.bot_data["attribuees_teamB"])  > 0 :
            keyboard = [[KeyboardButton(livraison_to_string(id, context))] for id in context.bot_data["attribuees_teamB"]]
            update.message.reply_text("Qui veux-tu lâcher ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
            return LIVB
        else :
            update.message.reply_text(lst_vide)
            return ConversationHandler.END
    else :
        if len(context.bot_data["attribuees_teamT"]) > 0 :
            keyboard = [[KeyboardButton(livraison_to_string(id, context))] for id in context.bot_data["attribuees_teamT"]]
            update.message.reply_text("Qui veux-tu lâcher ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
            return LIVT
        else :
            update.message.reply_text(lst_vide)
            return ConversationHandler.END

def abandB(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    if user_input[:3] not in ["Oui", "Non"] :
        update.message.reply_text(invalid_input)
        return CONFB
    id_user = int(user_input[5:-1])

    if user_input[:3] == "Oui" :
        context.bot_data["attribuees_teamB"].remove(id_user)
        context.bot_data["non_attribuees"].append(id_user)
        context.bot_data["users"][id_user]["répartit"] = False
        update.message.reply_text("Ok c'est noté !")

        missive = repart_to_string(context.bot_data["users"][id_user])
        #affiche des boutons sous la photo sur lesquels on peut cliquer
        keyboard = [[InlineKeyboardButton("Prendre pour ma team", callback_data="OK_" + str(id_user))]]
        context.bot.send_message(chat_id=id_BDAmour, text=missive, reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END
    else :
        return abandonner(update, context)

def abandT(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    if user_input[:3] not in ["Oui", "Non"] :
        update.message.reply_text(invalid_input)
        return CONFT
    id_user = int(user_input[5:-1])

    if user_input[:3] == "Oui" :
        context.bot_data["attribuees_teamT"].remove(id_user)
        context.bot_data["non_attribuees"].append(id_user)
        context.bot_data["users"][id_user]["répartit"] = False
        update.message.reply_text("Ok c'est noté !")

        missive = repart_to_string(context.bot_data["users"][id_user])
        #affiche des boutons sous la photo sur lesquels on peut cliquer
        keyboard = [[InlineKeyboardButton("Prendre pour ma team", callback_data="OK_" + str(id_user))]]
        context.bot.send_message(chat_id=id_BDAmour, text=missive, reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END
    else :
        return abandonner(update, context)

def annulation(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if not context.bot_data["users"][user_id]["admin"] :
        update.message.reply_text(tututut)
        return ConversationHandler.END
    else :
        if len(context.bot_data["commandes"]) > 0 :
            keyboard = [[KeyboardButton(livraison_to_string(id, context))] for id in context.bot_data["commandes"]]
            update.message.reply_text("Quelle commande on annule ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
            return ANNULE
        else :
            update.message.reply_text(lst_vide)
            return ConversationHandler.END

def annul(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    lst = [livraison_to_string(id, context) for id in context.bot_data["commandes"]]
    if not user_input in lst :
        update.message.reply_text(invalid_input)
        return ANNULE
    ind = lst.index(user_input)
    id_user = context.bot_data["commandes"][ind]

    update.message.reply_text(commande_to_string(context.bot_data["users"][id_user]))
    keyboard = [[KeyboardButton(choix)] for choix in ["Oui ({})".format(id_user), "Non ({})".format(id_user)]]
    update.message.reply_text("C'est bien cette commande ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return ANNULE2

def annul2(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    if user_input[:3] not in ["Oui", "Non"] :
        update.message.reply_text(invalid_input)
        return ANNULE2
    id_user = int(user_input[5:-1])

    if user_input[:3] == "Oui" :
        context.bot_data["users"][id_user]["commande"] = False
        context.bot_data["users"][id_user]["répartit"] = False
        context.bot_data["commandes"].remove(id_user)
        if id_user in context.bot_data["non_attribuees"]:
            context.bot_data["non_attribuees"].remove(id_user)
        if id_user in context.bot_data["attribuees_teamB"] :
            context.bot_data["attribuees_teamB"].remove(id_user)
        if id_user in context.bot_data["attribuees_teamT"] :
            context.bot_data["attribuees_teamT"].remove(id_user)
        context.bot_data["nb_commandes"] -= context.bot_data["users"][id_user]["nombre"]
        context.bot.send_message(chat_id=id_BDAmour, text=annulation_to_string(context.bot_data["users"][id_user]))

        keyboard = [[KeyboardButton(raison + " (" + str(id_user) + ")")] for raison in raisons]
        update.message.reply_text("La raison ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        return ANNULE3
    else :
        return annulation(update, context)

def annul3(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    if user_input[:9] not in raisons :
        update.message.reply_text(invalid_input)
        return ANNULE3

    id_user = int(user_input[11:-1])
    context.bot.send_message(chat_id=id_user, text=raisons[user_input[:9]])
