from telegram.ext import *
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import unicodedata
import time
from data import *
from pprint import pformat


def stop(update, context):
    update.message.reply_text(success_stop, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def user_id_str(user_data):
    #affichage
    try :
        return "{} {} {} ".format(user_data["prénom"],
                                       user_data["nom"],
                                       user_data["promo"])
    except :
        return user_data["nom"]

def admin(update, context):
    user_id = update.effective_user.id
    update.message.reply_text(ask_mdp, reply_markup=ReplyKeyboardRemove())
    return ADMIN

def rep_admin(update, context):
    user_id = update.effective_user.id
    user_input = update.message.text[:30].strip().replace("\n", " ")
    if user_input == mdp :
        context.bot_data["users"][user_id]["admin"] = True

    keyboard = [[KeyboardButton(team)] for team in teams]
    update.message.reply_text("Quelle team ?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return ADMIN2

def rep2_admin(update, context):
    user_id = update.effective_user.id
    user_input = update.message.text.strip().replace("\n", " ")
    if user_input not in teams:
        update.message.reply_text(invalid_input)
        return ADMIN2
    context.bot_data["users"][user_id]["team"] = user_input
    return ConversationHandler.END

def adresse_to_string(user_date):
    try : return "{}\n{}\n{}\nCompléments : {}".format(user_data["rue"],
                                                       user_data["code_postal"],
                                                       user_data["ville"],
                                                       user_data["compléments"])
    except : return user_data["prénom"]

def init_commande(update, context):
    user_id = update.effective_user.id
    if context.bot_data["users"][user_id]["admin"] == True :
        context.bot_data["commandes"] = []
        context.bot_data["non_attribuees"] = []
        context.bot_data["attribuees_teamB"] = []
        context.bot_data["attribuees_teamT"] = []
        context.bot_data["livrees"] = []
    return ConversationHandler.END

##########################

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def user_recap(user_data) :
    #affichage recap
    try :
        str_photo = ""
        for i in range(0, len(user_data["photo_sent"])) :
            str_photo += user_data["photo_sent"][i][0] + " , " + user_data["photo_sent"][i][1] + "\n"
        str_video = ""
        for i in range(0, len(user_data["video_sent"])) :
            str_video += user_data["video_sent"][i][0] + " , " + user_data["video_sent"][i][1] + "\n"
        str_text = ""
        for i in range(0, len(user_data["text_sent"])) :
            str_text += user_data["text_sent"][i][0] + " , " + user_data["text_sent"][i][1] + "\n"
        return "{} {} ({})\nDernier passage : {}\nNb de participations : {}\nA jour ? {}\nPhotos envoyées :\n{}Vidéos envoyées :\n{}Textes envoyés :\n{}".format(user_data["prénom"],
                                         user_data["nom"],
                                         user_data["promo"],
                                         user_data["last_visit"],
                                         user_data["total"],
                                         user_data["up_to_date"],
                                         str_photo,
                                         str_video,
                                         str_text)
    except :
        return user_data["prénom"] + " erreur"

def game_recap(update, context):
    user_id = update.effective_user.id
    if context.bot_data["users"][user_id]["admin"] :
        for id in context.bot_data["users"] :
            print(str(id) + user_recap(context.bot_data["users"][id]))
        nbInscrits = "{} inscrits.".format(len(context.bot_data["users"]))
        print(nbInscrits)
        context.bot.send_message(chat_id=id_BDAmour, text=nbInscrits)
    return ConversationHandler.END

def game_recap2(update, context):
    user_id = update.effective_user.id
    if context.bot_data["users"][user_id]["admin"] :
        for id in context.bot_data["users"] :
            score = context.bot_data["users"][id]["total"]
            if context.bot_data["users"][id]["last_visit"] == "25 December 2020" and context.bot_data["users"][id]["up_to_date"]:
                score -= 1
            print(str(id) + ";" + context.bot_data["users"][id]["prénom"] + " " + context.bot_data["users"][id]["nom"] + ";" + str(score))
        nbInscrits = "{} inscrits.".format(len(context.bot_data["users"]))
        print(nbInscrits)
    return ConversationHandler.END

def resultats(update, context):
    user_id = update.effective_user.id
    if context.bot_data["users"][user_id]["admin"] :
        for id in context.bot_data["users"] :
            if id in participants :
                context.bot.send_message(chat_id=id, text=fin)
    return ConversationHandler.END

def recap(update, context):
    user_id = update.effective_user.id
    str = "Tu as ouvert les cadeaux et accomplis les challenges {} jours sur {}.\nLe dernier cadeau ouvert étant le {}.".format(context.bot_data["users"][user_id]["total"],
                                                                                                                  int(time.strftime("%d", time.localtime(time.time()))),
                                                                                                                  context.bot_data["users"][user_id]["last_visit"])
    context.bot.send_message(chat_id=user_id, text=str)
    return ConversationHandler.END

def correction(update, context):
    user_id = update.effective_user.id
    if context.bot_data["users"][user_id]["admin"] :
        context.bot_data["users"][1222732617]["up_to_date"] = True
        context.bot_data["users"][1222732617]["total"] += 1
        context.bot_data["users"][1222732617]["defi_sent"] = False
        context.bot.send_message(chat_id=1222732617, text=OK+thanks)
        print("OK")
    return ConversationHandler.END

def pause(update, context):
    user_id = update.effective_user.id
    if context.bot_data["users"][user_id]["admin"] :
        message = "Bonjour, le bot va être désactivé d'ici 1h et jusqu'à 16h environ.\nLa raison : je dois transiter d'un appart à un autre donc j'aurais plus de réseau sur mon PC. Mais don't worry je le rallume dès que je suis arrivée.\nBonne vacances à vous !"
        for id in context.bot_data["users"] :
            context.bot.send_message(chat_id=id, text=message)
    return ConversationHandler.END

def photoecho(update, context):
    """Displays infos about a received photo in the console, no user feedback"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    print("[photoecho] user {} sent a picture, which characteristics are :".format(user_id))
    fsiz = 0
    for photosiz in update.message.effective_attachment:
        #print("file size : " + str(photosiz.file_size))
        #print("file id : " + photosiz.file_id)
        if photosiz.file_size>fsiz:
            fid = photosiz.file_id
            fsiz = photosiz.file_size
    context.bot.send_message(chat_id=id_BDAmour, text=context.bot_data["users"][user_id]["prénom"]+" envoie :")
    context.bot.send_photo(chat_id=id_BDAmour, photo=fid)
    # context.bot_data["photo_file_id"] = fid
    # context.bot.send_photo(chat_id, fid)

def audioecho(update, context):
    """Displays infos about a received audio in the console, no user feedback"""

    user_id = update.effective_user.id

    print("[audioecho] user {} sent an audio, which characteristics are :".format(user_id))
    print(pformat(update.message.effective_attachment))
    print("file_id : "+update.message.effective_attachment.file_id)

def videoecho(update, context):
    """Displays infos about a received video in the console, no user feedback"""

    user_id = update.effective_user.id

    #print("[vidéoecho] user {} sent a video, which characteristics are :".format(user_id))
    #print(pformat(update.message.effective_attachment))
    #print("file_id : "+update.message.effective_attachment.file_id)
    context.bot.send_message(chat_id=id_BDAmour, text=context.bot_data["users"][user_id]["prénom"]+" envoie :")
    context.bot.send_video(chat_id=id_BDAmour, video=update.message.effective_attachment.file_id)

def transfer(update, context):
    user_id = update.effective_user.id
    user_input = update.message.text.strip().replace("\n", " ")
    context.bot.send_message(chat_id=id_BDAmour, text=context.bot_data["users"][user_id]["prénom"]+" envoie :\n"+user_input)
