from telegram.ext import *
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import time

from data import *
from functions import *

def commander(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if context.bot_data["nb_commandes"] > max_crepes :
        update.message.reply_text(too_much)
        context.bot.send_photo(chat_id=chat_id, photo=photo_team)
    elif not context.bot_data["users"][user_id]["commande"] :
        keyboard = [[KeyboardButton(choix)] for choix in possibilités]
        update.message.reply_text("Quelles crêpes veux-tu ? 😀", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        return CREPES
    else :
        update.message.reply_text(already_commande)
        return ConversationHandler.END

def crepes(update, context):
    user_id = update.effective_user.id
    user_input = update.message.text.strip().replace("\n", " ")

    if user_input not in possibilités :
        update.message.reply_text(invalid_input)
        return CREPES
    context.bot_data["users"][user_id]["crepes"] = user_input

    keyboard = [[KeyboardButton(nb)] for nb in range(2,11)]
    update.message.reply_text("Combien ? (En comptant la crêpe gratuite 😉)", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return NB

def quantite(update, context):
    user_id = update.effective_user.id
    user_input = int(update.message.text[:30].strip().replace("\n", " "))

    if user_input<2 or user_input>10 :
        update.message.reply_text(invalid_input)
        return NB
    context.bot_data["users"][user_id]["nombre"] = user_input
    update.message.reply_text("Ca fera " + str((user_input-1)*prix) + "€ à régler au moment de la livraison 😊")

    keyboard = [[KeyboardButton(creno)] for creno in creneaux]
    update.message.reply_text("Quand est ce que tu veux qu'on te livre ? (on fera au mieux)", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return CRENEAU

def moment(update, context):
    user_id = update.effective_user.id
    user_input = update.message.text[:30].strip().replace("\n", " ")

    if user_input not in creneaux :
        update.message.reply_text(invalid_input)
        return CRENEAU
    context.bot_data["users"][user_id]["créneau"] = user_input

    update.message.reply_text("As-tu une précision à nous faire sur cette commande ?", reply_markup=ReplyKeyboardRemove())
    return PRECISION

def precision(update, context):
    user_id = update.effective_user.id
    user_input = update.message.text.strip().replace("\n", " ")

    context.bot_data["users"][user_id]["précision"] = user_input

    update.message.reply_text("Maintenant on a besoin de savoir où livrer.")
    update.message.reply_text(ask_adresse[RUE])
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
    return NUM

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

    context.bot_data["users"][user_id]["commande"] = True
    context.bot_data["commandes"].append(user_id)
    context.bot_data["non_attribuees"].append(user_id)
    context.bot_data["nb_commandes"] += context.bot_data["users"][user_id]["nombre"]

    missive = repart_to_string(context.bot_data["users"][user_id])
    #affiche des boutons sous la photo sur lesquels on peut cliquer
    keyboard = [[InlineKeyboardButton("Prendre pour ma team", callback_data="OK_" + str(user_id))]]
    context.bot.send_message(chat_id=id_BDAmour, text=missive, reply_markup=InlineKeyboardMarkup(keyboard))

    update.message.reply_text(termine, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def validation(update, context):
    user_id = update.effective_user.id
    query = update.callback_query
    bot = update.callback_query.bot
    valeur = query.data
    id_user = int(valeur[3:])

    if user_id in context.bot_data["users"]:
        if id_user not in context.bot_data["attribuees_teamB"] and id_user not in context.bot_data["attribuees_teamT"] :
            if context.bot_data["users"][user_id]["admin"] and context.bot_data["users"][user_id]["team"] == "Team Bordeaux" :
                query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
                context.bot.send_message(chat_id=id_BDAmour, text="La team Bordeaux s'occupe de cette commande")
                if context.bot_data["users"][id_user]["créneau"] == creneaux[-1] :
                    context.bot_data["attribuees_teamB"].append(id_user)
                else :
                    context.bot_data["attribuees_teamB"].insert(0, id_user)
                context.bot_data["non_attribuees"].remove(id_user)
                context.bot_data["users"][id_user]["répartit"] = True
            elif context.bot_data["users"][user_id]["admin"] and context.bot_data["users"][user_id]["team"] == "Team Talence" :
                query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
                context.bot.send_message(chat_id=id_BDAmour, text="La team Talence s'occupe de cette commande")
                if context.bot_data["users"][id_user]["créneau"] == creneaux[-1] :
                    context.bot_data["attribuees_teamT"].append(id_user)
                else :
                    context.bot_data["attribuees_teamT"].insert(0, id_user)
                context.bot_data["non_attribuees"].remove(id_user)
                context.bot_data["users"][id_user]["répartit"] = True
        else :
            query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))

def button(update, context):
    query = update.callback_query
    valeur = query.data
    query.answer() # avoid hogging the client
    return validation(update, context)

def annuler(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if context.bot_data["users"][user_id]["commande"] and not context.bot_data["users"][user_id]["livre"] :
        update.message.reply_text("Voilà ta commande :\n" + commande_to_string(context.bot_data["users"][user_id]), reply_markup=ReplyKeyboardRemove())

        keyboard = [[KeyboardButton(choix)] for choix in ["Oui", "Non"]]
        update.message.reply_text("Es-tu sûr de vouloir annuler ta commande ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        return ANNULE
    else :
        update.message.reply_text("Tu n'as rien à annuler 😮", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

def annule(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_input = update.message.text.strip().replace("\n", " ")

    if user_input not in ["Oui", "Non"] :
        update.message.reply_text(invalid_input)
        return ANNULE

    if user_input == "Oui" :
        context.bot_data["users"][user_id]["commande"] = False
        context.bot_data["users"][user_id]["répartit"] = False
        context.bot_data["commandes"].remove(user_id)
        if user_id in context.bot_data["non_attribuees"]:
            context.bot_data["non_attribuees"].remove(user_id)
        if user_id in context.bot_data["attribuees_teamB"] :
            context.bot_data["attribuees_teamB"].remove(user_id)
        if user_id in context.bot_data["attribuees_teamT"] :
            context.bot_data["attribuees_teamT"].remove(user_id)
        update.message.reply_text("C'est bon ta commande est annulée")
        context.bot_data["nb_commandes"] -= context.bot_data["users"][user_id]["nombre"]
        context.bot.send_message(chat_id=id_BDAmour, text=annulation_to_string(context.bot_data["users"][user_id]), reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else :
        update.message.reply_text("Ok on touche à rien")
        return ConversationHandler.END
