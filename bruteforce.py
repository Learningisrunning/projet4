import json
from itertools import combinations


class RecuperationDesData:
    def __init__(self, fichier: json) -> None:
        self.fichier = fichier

    def lecture_du_fichier(self):
        """Lecture des du fichier Json
            Dict creer"""
        with open(self.fichier, "r") as fichier_json:
            dict_data = json.load(fichier_json)

        return dict_data


class test_des_differentes_combinaison:
    def __init__(self, data, valeur_client) -> None:
        self.data = data
        self.valeur_client = valeur_client
        self.valeur_la_moins_cher = ""

    def obtention_du_nombre_de_la_taille_des_combi(self):
        """Estimation de la taille minimal et maximal des combinaisons"""
        liste_des_valeurs = []
        addition = 0
        nb_valeur_max = 0
        nb_valeur_min = 0
        for nb_action in range(len(self.data["ListeDesActions"])):
            liste_des_valeurs.append(data["ListeDesActions"]
                                     ["Action-" + str(nb_action+1)]
                                     ["cout_de_laction"])

        liste_des_valeurs.sort(reverse=True)

        """Calcule du nombre max de valeurs dans un portefeuille"""
        while (addition + liste_des_valeurs[nb_valeur_max + 1] <
                self.valeur_client):

            addition = addition + liste_des_valeurs[nb_valeur_max]
            nb_valeur_max = nb_valeur_max + 1
        print(nb_valeur_max)

        liste_des_valeurs.sort()
        addition = 0

        """Calcule du nombre min de valeurs dans un portefeuille"""
        while (addition + liste_des_valeurs[nb_valeur_min + 1] <
                self.valeur_client):

            addition = addition + liste_des_valeurs[nb_valeur_min]
            nb_valeur_min = nb_valeur_min + 1
        print(nb_valeur_min)

        return nb_valeur_min, nb_valeur_max

    def obtention_des_combinaison_possible(self, valeur_min, valeur_max):
        """determination de toutes les combinaisons"""
        liste_des_combinaisons_possibles = []
        liste_des_actions = []

        for action in self.data["ListeDesActions"]:
            liste_des_actions.append(action)

        for taille_combinaison in range(valeur_min, valeur_max+1):
            combinaison = combinations(liste_des_actions, taille_combinaison)
            for combi in list(combinaison):
                liste_des_combinaisons_possibles.append(combi)
        print(liste_des_combinaisons_possibles)

        return liste_des_combinaisons_possibles

    def choix_de_la_meilleure_combinaison(self, liste_des_combinaison_possible):
        """Determination de la meilleure combinaison
            celon les criteres fournis"""

        portefeuille = {
            "liste_action_achetées": "",
            "valeur_portefeuille": 0,
            "perf_portefeuille": 0
         }

        valeur_combinaison = 0
        perf_combinaison = 0

        for combinaison in liste_des_combinaison_possible:
            liste_valeur_action = []
            liste_perf_combinaison = []
            liste_perf_valeur_monetaire = []

            for action in combinaison:
                liste_valeur_action.append(data["ListeDesActions"]
                                           [action]
                                           ["cout_de_laction"])

                liste_perf_combinaison.append(data["ListeDesActions"]
                                              [action]
                                              ["perf"])

                liste_perf_valeur_monetaire.append(data["ListeDesActions"]
                                                   [action]
                                                   ["cout_de_laction"] *
                                                   data["ListeDesActions"]
                                                   [action]
                                                   ["perf"])

            valeur_combinaison = sum(liste_valeur_action)
            perf_combinaison = sum(liste_perf_valeur_monetaire)

            if (valeur_combinaison < self.valeur_client and
                    perf_combinaison > portefeuille["perf_portefeuille"] and
                    valeur_combinaison >= portefeuille["valeur_portefeuille"]):

                portefeuille["liste_action_achetées"] = combinaison
                portefeuille["valeur_portefeuille"] = valeur_combinaison
                portefeuille["perf_portefeuille"] = perf_combinaison

        print(portefeuille)


data = RecuperationDesData("donnees.json").lecture_du_fichier()
nb_valeur_max, nb_valeur_min = (test_des_differentes_combinaison(data, 500).
                                obtention_du_nombre_de_la_taille_des_combi())

liste_combinaison = (test_des_differentes_combinaison(data, 500).
                     obtention_des_combinaison_possible(nb_valeur_min,
                                                        nb_valeur_max))

(test_des_differentes_combinaison(data, 500).
    choix_de_la_meilleure_combinaison(liste_combinaison))
