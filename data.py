intro = "Salut toi ! Tu viens commander un goûter c'est ça ?\nEt beh ça tombe bien t'es au bon endroit."
already_started = "Je vois que tu es déjà inscrit, utilises plutôt la commande /start_again si tu t'es trompé ☺️"
ask_data = "Avant de commencer on a besoin de savoir qui tu es ! 😉"
recap_data = "On récapitule :"
incorrect_data = "Tu peux recommencer avec la commande /start_again s'il y a une erreur."
finish_start = "Merci de t'être inscrit à ce nouveau bot !\nOn est heureux de vous proposer ces livraisons de crêpes, ça permettra à nous comme à vous de voir du monde et je pense que ça fait de mal à personne 😊\nAlors ce qu'il y a à savoir :\n-> 0.50€ la crêpe\n-> une crêpe offerte par commande 🥳\n-> entre 2 et 5 crêpes par personne en comptant la crêpe gratuite\n-> paiment sur place par Lydia en priorité ou en espèce à condition que vous ayez la monnaie\n-> on a pas de voiture donc on a établit une zone où on peut livrer (/carte), si vous êtes en dehors il faudra vous déplacer pour qu'on fasse moit moit pour le chemin (le préciser dans la partie compléments au moment de la commande)\n-> le BDA est heureux de vous retrouver même brièvement 🥰\n-> /help pour avoir la liste des commandes du bot"
success_stop = "Ok on fait une pause. "
invalid_input = "Je n'ai pas compris, essaie encore."
inform_stop = "Tu peux annuler à tout moment avec la commande /stop"
ask_mdp = "Quel est le mot de passe ?"
mdp = "Joseph"
termine = "C'est bon ta commande est passée ! Si t'as un soucis hésites pas à faire /sos"
already_commande = "Tu as déjà commandé une première fois, donc tu ne peux pas retenter l'expérience. 😕\nIl faut en laisser pour les autres je suis sûr que tu peux comprendre ça ☺️\nEn tout cas merci d'avoir commandé ! 😍"
too_much = "Oh noon on a dépassé le nombre de crêpes limites ! 😭\nDésolé que tu ne puisses pas commander, on t'envoies une photo de nous en échange 😘"
aide_commande = "Alors, alors, alors\nC'est pas compliqué, si tu veux passer commande tu fais /commander, pour annuler ta commande /annuler (easy)\nPour voir la zone où on livre c'est /carte, et la commande /sos te dira quoi faire si tu es en PLS\nEt /stop évidemment si tu veux arrêter ce que tu fais (ne pas hésiter à l'utiliser si tu penses que c'est buggué)\nFacile non ? 😉"
aide_livreur = "Hello toi ! Du coup c'est pas trop compliqué normalement (j'espère)\nSi tu fais /recap_team tu verras toutes le commandes de ta team qui n'ont pas encore été livrées et sur place tu pourras valider la livraison en faisont /livraison.\nSi vous avez dans votre liste une commande qui correpondrait plus à l'autre team, tu peux faire /abandonner\nEt le /stop fonctionne aussi évidemment"
tututut = "Tututut, cette commande n'est pas faite pour toi 😜\nEssaye plutôt /help pour savoir ce que tu peux faire"
lst_vide = "La liste de livraison est vide !"
mayday = "Si tu as un soucis qui ne peut pas être réglé directement grâce au bot, hésites pas à poser ta question dans la conv BDA Question, notre standardiste/RespoBot/VicePrez sera au taquet (sauf si c'est au milieu de la nuit). Ou à me MP directement sur Telgram (@ArteMyth) ou sur Messenger (Enora Thomas)"

empty_user = { "prénom" : "",
               "nom" : "",
               "promo" : "",
               "admin" : False,
               "team" : "",
               "commande" : False,
               "répartit" : False,
               "livre" : False,
               "crepes" : "",
               "nombre" : 0,
               "créneau" : "",
               "précision" : "",
               "rue" : "",
               "code_postal" : "",
               "ville" : "",
               "compléments" : "",
               "téléphone" : ""}

ask = [ "Quel est ton prénom ?",
        "Quel est ton nom ?",
        "Dans quelle promo es-tu ?",
        "Super merci ! J'arrête de t'embêter !"]

PRENOM, NOM, PROMO, FIN = range(4)

ask_adresse = [ "","","","","Ton adresse ? (numéro + nom de rue)",
                "Le code postal ?",
                "La ville ?",
                "Des compléments si besoin ? (étage, numéro d'appt...)",
                "Et un numéro de téléphone pour quand on est en bas de chez toi (promis on les garde pas) ?",
                "Parfait je note tout ça !"]

promos = [ "1A", "2A", "3A"]
teams = ["Team Bordeaux", "Team Talence"]
possibilités = ["Crêpes au chocolat 🍫", "Crêpes au sucre 🍭", "Crêpes à la confiture 🍑", "Crêpes au miel 🍯", "Crêpes natures 😇"]
creneaux = ["13h-15h30", "15h30-17h30"]
prix = 0.5
max_crepes = 200
photo_team = "AgACAgQAAxkBAAIiVmAMLB2gt6IOqmW8XfUNI4PqFE8PAAJ2tDEbc2JhUEsbyuV3jFV9Q5f8KF0AAwEAAwIAA3kAA7TyAgABHgQ"
map = "AgACAgQAAxkBAAIka2AMnsZffvYfTt9TeyM6qg_w6aDTAALvtDEbc2JhUKYUAcrWHbdnHbZJJ10AAwEAAwIAA3gAA9eJBAABHgQ"
raisons = {"Trop loin" : "Désolé nous avons du annuler ta commande car tu te trouves trop loin de nous pour qu'on puisse te livrer 😞\nCependant tu peux toujours re /commander si tu es motivé pour te déplacer pour récupérer ta commande.\nMerci de ta compréhension 😊",
           "Trop tard" : "Désolé nous avons du annuler ta commande car il est trop tard et nous ne pensons pas avoir le temps de te livrer avant le couvre feu 😞",
           "Autre----" : "Désolé nous avons du annuler ta commande, hésites pas à contacter Enora si tu veux plus d'info là dessus"}
CREPES, NB, CRENEAU, PRECISION, RUE, CP, VILLE, COMP, NUM, NOTE = range(10)

id_BDAmour = -430587684
ADMIN, ADMIN2 = range(2)
ANNULE, ANNULE2, ANNULE3 = range(3)

LIVB, LIVT, CONFB, CONFT = range(4)
