import telegram
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request
import os
import sys
from threading import Thread

from data import *
from registration import *
from functions import *
from commande import *
from adresse import *

# Slightly modify the Bot class to use a MessageQueue in order to avoid
# Telegram's flood limits (30 msg/sec)
class MQBot(telegram.bot.Bot):
    """A subclass of Bot which delegates send method handling to MessageQueue"""
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()
    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        """Wrapped method would accept new `queued` and `isgroup` OPTIONAL arguments"""
        return super(MQBot, self).send_message(*args, **kwargs)


# Limit global throughput to 25 messages per second
q = mq.MessageQueue(all_burst_limit=25, all_time_limit_ms=1000)
# Set connection pool size for bot
request = Request(con_pool_size=8)

def readToken():
    tokfile = open('BOT_TOKEN', 'r')
    token = tokfile.read()[:-1]
    tokfile.close()
    return token

token = readToken()

tgbot = MQBot(token, request=request, mqueue=q)

persistence = telegram.ext.PicklePersistence(filename='bot_data_pickle')

updater = telegram.ext.updater.Updater(bot=tgbot, persistence=persistence, use_context=True)
dispatcher = updater.dispatcher


#début des composants propres à ce bot
stop_handler = CommandHandler("stop", stop)

start_handler = ConversationHandler(
    entry_points = [CommandHandler("start", start),
                    CommandHandler("start_again", update_id)],
    states = {PRENOM: [stop_handler, MessageHandler(Filters.text, prenom)],
              NOM: [stop_handler, MessageHandler(Filters.text, nom)],
              PROMO: [stop_handler, MessageHandler(Filters.text, promo)]},
    fallbacks = [stop_handler],
    name = "start_handler",
    persistent = True)

dispatcher.add_handler(start_handler)

adresse_handler = ConversationHandler(
    entry_points = [CommandHandler("adresse", adresse)],
    states = {RUE : [stop_handler, MessageHandler(Filters.text, rue)],
              CP : [stop_handler, MessageHandler(Filters.text, code_postal)],
              VILLE : [stop_handler, MessageHandler(Filters.text, ville)],
              COMP : [stop_handler, MessageHandler(Filters.text, complements)],
              NUM : [stop_handler, MessageHandler(Filters.text, numero)]},
    fallbacks = [stop_handler],
    name = "adresse_handler",
    persistent = True)

dispatcher.add_handler(adresse_handler)

admin_handler = ConversationHandler(
    entry_points = [CommandHandler("admin", admin)],
    states = {ADMIN : [stop_handler, MessageHandler(Filters.text, rep_admin)],
              ADMIN2 : [stop_handler, MessageHandler(Filters.text, rep2_admin)]},
    fallbacks = [stop_handler],
    name = "admin_handler",
    persistent = True)

dispatcher.add_handler(admin_handler)

#autres éléments communs à tous les bots
updater.start_polling()
updater.idle()
#############

today_handler = ConversationHandler(
    entry_points = [CommandHandler("today", today)],
    states = {ANECDOTE : [stop_handler, MessageHandler(Filters.text, anecdote)],
              LIVRE : [stop_handler, MessageHandler(Filters.text, livre)],
              FILM : [stop_handler, MessageHandler(Filters.text, film)],
              ENIGME : [stop_handler, MessageHandler(Filters.text, enigme)],
              SOLUTION : [stop_handler, MessageHandler(Filters.text, solution)],
              CHALLENGE : [stop_handler, MessageHandler(Filters.text, challenge)],
              ENVOIP : [stop_handler, MessageHandler(Filters.photo, envoip)],
              ENVOIV : [stop_handler, MessageHandler(Filters.video, envoiv)],
              ENVOIT : [stop_handler, MessageHandler(Filters.text, envoit)]},
    fallbacks = [stop_handler],
    name = "today_handler",
    persistent = True)

dispatcher.add_handler(today_handler)

dispatcher.add_handler(CallbackQueryHandler(button))

dispatcher.add_handler(CommandHandler("recap", recap))
dispatcher.add_handler(CommandHandler("game_recap", game_recap))
dispatcher.add_handler(CommandHandler("game_recap2", game_recap2))
dispatcher.add_handler(CommandHandler("correction", correction))
dispatcher.add_handler(CommandHandler("pause", pause))
dispatcher.add_handler(CommandHandler("resultats", resultats))

seeuser_handler = ConversationHandler(
    entry_points = [CommandHandler("see_user", see_user)],
    states = {SEENU: [stop_handler, MessageHandler(Filters.text, seen_user)]},
    fallbacks = [stop_handler],
    name = "seeuser_handler",
    persistent = True)

dispatcher.add_handler(seeuser_handler)

seephoto_handler = ConversationHandler(
    entry_points = [CommandHandler("see_photo", see_photo)],
    states = {SEENP: [stop_handler, MessageHandler(Filters.text, seen_photo)]},
    fallbacks = [stop_handler],
    name = "seephoto_handler",
    persistent = True)

dispatcher.add_handler(seephoto_handler)

seevideo_handler = ConversationHandler(
    entry_points = [CommandHandler("see_video", see_video)],
    states = {SEENV: [stop_handler, MessageHandler(Filters.text, seen_video)]},
    fallbacks = [stop_handler],
    name = "seevideo_handler",
    persistent = True)

dispatcher.add_handler(seevideo_handler)


def stop_and_restart():
    """Gracefully stop the Updater and replace the current process with a new one"""
    updater.stop()
    os.execl(sys.executable, *sys.argv, *sys.argv)

def restart(update, context):
    user_id = update.effective_user.id
    if context.bot_data["users"][user_id]["admin"] :
        print("Rebooting...")
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()

dispatcher.add_handler(CommandHandler('reboot', restart))

dispatcher.add_handler(MessageHandler(Filters.photo, photoecho))
dispatcher.add_handler(MessageHandler(Filters.audio, audioecho))
dispatcher.add_handler(MessageHandler(Filters.video, videoecho))
dispatcher.add_handler(MessageHandler(Filters.text, transfer))