from telegram.ext import *
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import time

from data import *
from functions import *
from adresse import *

def commander(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    keyboard = [[KeyboardButton(choix)] for choix in possibilités]
    update.message.reply_text("Quelles crêpes veux tu ? 😀", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return CREPES

def crepes(update, context):
    user_id = update.effective_user.id
    user_input = update.message.text[:30].strip().replace("\n", " ")

    if user_input not in possibilités :
        update.message.reply_text(invalid_input)
        return CREPES
    context.bot_data["users"][user_id]["crepes"] = user_input

    keyboard = [[KeyboardButton(nb)] for nb in range(2,6)]
    update.message.reply_text("Combien ? (En comptant la crêpe gratuite 😉)", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return NB

def quantite(update, context):
    user_id = update.effective_user.id
    user_input = int(update.message.text[:30].strip().replace("\n", " "))

    if user_input<2 or user_input>5 :
        update.message.reply_text(invalid_input)
        return NB
    context.bot_data["users"][user_id]["nombre"] = user_input
    update.message.reply_text("Ca fera " + str((user_input-1)*prix) + "€ à régler au moment de la livraison 😊", reply_markup=ReplyKeyboardRemove))

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
