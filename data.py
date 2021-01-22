intro = "Salut toi ! Tu viens commander un goûter c'est ça ?\nEt beh ça tombe bien t'es au bon endroit."
already_started = "Je vois que tu es déjà inscrit, utilises plutôt la commande /start_again si tu t'es trompé ☺️"
ask_data = "Avant de commencer on a besoin de savoir qui tu es ! 😉"
recap_data = "On récapitule :"
incorrect_data = "Tu peux recommencer avec la commande /start_again s'il y a une erreur."
finish_start = ""
success_stop = "Ok on fait une pause. "
invalid_input = "Je n'ai pas compris, essaie encore."
inform_stop = "Tu peux annuler à tout moment avec la commande /stop"
ask_mdp = "Quel est le mot de passe ?"
mdp = "658390"
chgmt_adresse = "Si tu t'es trompé fais /adresse pour modifier ton adresse."

empty_user = { "prénom" : "",
               "nom" : "",
               "promo" : "",
               "admin" : False,
               "team" : "",
               "commande" : False,
               "répartit" : False,
               "livre" : True,
               "crepes" : "",
               "nombre" : 0,
               "créneau" : "",
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

ask_adresse = [ "Ton adresse ? (numéro + nom de rue)",
                "Le code postal ?",
                "La ville ?",
                "Des compléments si besoin ? (étage, numéro d'appt...)",
                "Et un numéro de téléphone pour quand on est en bas de chez toi (promis on les garde pas) ?",
                "Parfait je note tout ça !"]

RUE, CP, VILLE, COMP, NUM, NOTE = range(6)

promos = [ "1A", "2A", "3A"]
teams = ["Team Bordeaux", "Team Talence"]

id_BDAmour = -430587684
ADMIN, ADMIN2 = range(2)
