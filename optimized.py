import json
import pandas as pd
import csv


class RecuperationDesDataJson:
    def __init__(self, fichier: json) -> None:
        self.fichier = fichier

    def lecture_du_fichier(self):
        """lecture d'un fichier Json et sorti d'un dict"""
        with open(self.fichier, "r") as fichier_json:
            dict_data = json.load(fichier_json)

        return dict_data


class RecuperationDesDataCsv:
    def __init__(self, fichier: csv) -> None:
        self.fichier = fichier

    def lecture_du_fichier_csv(self):
        """Lecture du fichier csv et creation d'un dict"""
        dict_data_vf = {}
        liste_des_action = {}
        dict_data_csv = pd.read_csv(self.fichier)

        for nb_data in range(len(dict_data_csv)):
            dict_data_vf[dict_data_csv["name"][nb_data]] = (
                {"cout_de_laction": dict_data_csv["price"][nb_data],
                 "perf": (dict_data_csv["profit"][nb_data]/100)})

        liste_des_action["ListeDesActions"] = dict_data_vf

        return (liste_des_action)


class RecuperationMeilleureCombinaisonOpti:
    def __init__(self, data, valeur_client) -> None:
        self.data = data
        self.valeur_client = valeur_client

    def classement_des_actions_perf_prix(self):
        """estimation des meilleurs rapport prix/perf"""

        dict_rapport_perf_prix = {}
        for actions in data["ListeDesActions"]:
            if data["ListeDesActions"][actions]["cout_de_laction"] > 0:
                rapport_perf_prix = ((data["ListeDesActions"][actions]["perf"] *
                                     data["ListeDesActions"][actions]["cout_de_laction"]) /
                                     data["ListeDesActions"][actions]["cout_de_laction"])
                dict_rapport_perf_prix[actions] = rapport_perf_prix

        dict_rapport_perf_prix_trie = dict(sorted(dict_rapport_perf_prix.items(),
                                                  reverse=True,
                                                  key=lambda
                                                  dict_rapport_perf_prix: dict_rapport_perf_prix[1]))

        return dict_rapport_perf_prix_trie

    def recuperation_liste_keys_dict_trie(self, dict_trie):
        keys = dict_trie.keys()
        liste_cles_dict_trie = []
        for key in keys:
            liste_cles_dict_trie.append(key)

        return liste_cles_dict_trie

    def portefeuille_meilleure_perf(self, liste_cles_dict_trie):
        """estimation du protefeuille avec la meilleure performance"""
        portefeuille = {
            "liste_des_actions_a_acheter": "",
            "valeur_portefeuille": 0,
            "perf_portefeuille": 0
        }

        liste_des_action_a_acheter = []
        liste_des_valeur_des_actions_a_acheter = []
        liste_perf_des_actions_a_acheter = []
        perf_en_valeur_monetaire = []

        liste_de_comparaison_des_valeur_des_actions_a_acheter = []
        perf_de_comparaison_en_valeur_monetaire = []
        valo_total_portefeuille = 0
        prochaine_action_valeur = 0

        for action in range(len(liste_cles_dict_trie)):
            if (valo_total_portefeuille +
                    prochaine_action_valeur < self.valeur_client):

                """Ajout de l'action au portefeuille
                   Tant que valo port < valo client"""

                liste_des_action_a_acheter.append(liste_cles_dict_trie[action])
                (liste_des_valeur_des_actions_a_acheter.
                    append(self.data["ListeDesActions"]
                           [liste_cles_dict_trie[action]]["cout_de_laction"]))

                (liste_perf_des_actions_a_acheter.
                    append(self.data["ListeDesActions"]
                           [liste_cles_dict_trie[action]]["perf"]))

                perf_en_valeur_monetaire.append(self.data["ListeDesActions"]
                                                [liste_cles_dict_trie[action]]
                                                ["perf"] *
                                                self.data["ListeDesActions"]
                                                [liste_cles_dict_trie[action]]
                                                ["cout_de_laction"])

                valo_total_portefeuille = sum(
                    liste_des_valeur_des_actions_a_acheter)

                try:
                    prochaine_action_valeur = (self.data["ListeDesActions"]
                                               [liste_cles_dict_trie[action + 1]]
                                               ["cout_de_laction"])
                except:
                    None
            else:
                """On enlève la dernière valeur ajoutée
                   On la remplace par le prochaine.
                   On voit si les perfs sont meilleures"""
                try:

                    liste_de_comparaison_des_valeur_des_actions_a_acheter = []
                    perf_de_comparaison_en_valeur_monetaire = []
                    nouvelle_valo = 0
                    for valeurs in liste_des_valeur_des_actions_a_acheter:
                        liste_de_comparaison_des_valeur_des_actions_a_acheter.append(valeurs)
                    liste_de_comparaison_des_valeur_des_actions_a_acheter[-1] = (
                        self.data["ListeDesActions"]
                        [liste_cles_dict_trie[action]]
                        ["cout_de_laction"])

                    for perfs in perf_en_valeur_monetaire:
                        perf_de_comparaison_en_valeur_monetaire.append(perfs)
                    perf_de_comparaison_en_valeur_monetaire[-1] = (
                        self.data["ListeDesActions"]
                        [liste_cles_dict_trie[action]]
                        ["perf"] *
                        self.data["ListeDesActions"]
                        [liste_cles_dict_trie[action]]
                        ["cout_de_laction"])

                    nouvelle_valo = sum(
                        liste_de_comparaison_des_valeur_des_actions_a_acheter)

                    perf_valeur_initial = (
                        self.data["ListeDesActions"]
                        [liste_des_action_a_acheter[-1]]
                        ["perf"])

                    perf_valeur_concurente = (
                        self.data["ListeDesActions"]
                        [liste_cles_dict_trie[action]]
                        ["perf"])

                    if (nouvelle_valo < self.valeur_client and
                        sum(perf_de_comparaison_en_valeur_monetaire) > sum(perf_en_valeur_monetaire) and
                            0.9*perf_valeur_initial < perf_valeur_concurente < 1.1*perf_valeur_initial):

                        liste_des_action_a_acheter[-1] = (
                            liste_cles_dict_trie[action])

                        liste_des_valeur_des_actions_a_acheter[-1] = (
                            self.data["ListeDesActions"]
                            [liste_cles_dict_trie[action]]
                            ["cout_de_laction"])

                        liste_perf_des_actions_a_acheter[-1] = (
                            self.data["ListeDesActions"]
                            [liste_cles_dict_trie[action]]
                            ["perf"])

                        perf_en_valeur_monetaire[-1] = (
                            self.data["ListeDesActions"]
                            [liste_cles_dict_trie[action]]
                            ["perf"]*
                            self.data["ListeDesActions"]
                            [liste_cles_dict_trie[action]]
                            ["cout_de_laction"])

                        valo_total_portefeuille = (
                            sum(liste_des_valeur_des_actions_a_acheter))

                        prochaine_action_valeur = (
                            self.data["ListeDesActions"]
                            [liste_cles_dict_trie[action + 2]]
                            ["cout_de_laction"])

                except:
                    None

                valo_total_portefeuille = (
                    sum(liste_des_valeur_des_actions_a_acheter))
                try:
                    prochaine_action_valeur = (
                        self.data["ListeDesActions"]
                        [liste_cles_dict_trie[action + 1]]
                        ["cout_de_laction"])
                except:
                    None

        portefeuille["liste_des_actions_a_acheter"] = (
            liste_des_action_a_acheter)

        portefeuille["valeur_portefeuille"] = (
            sum(liste_des_valeur_des_actions_a_acheter))

        portefeuille["perf_portefeuille"] = sum(perf_en_valeur_monetaire)

        print(portefeuille)


"""#data = (RecuperationDesDataCsv("E:/Dev/Projet4/data_fournis/1.csv").
            lecture_du_fichier_csv())

    #data = (RecuperationDesDataCsv("E:/Dev/Projet4/data_fournis/2.csv").
        #lecture_du_fichier_csv())"""

data = RecuperationDesDataJson("donnees.json").lecture_du_fichier()

dict_actions_triees = (RecuperationMeilleureCombinaisonOpti(data, 500).
                       classement_des_actions_perf_prix())

liste_cles_dict_trie = (RecuperationMeilleureCombinaisonOpti(data, 500).
                        recuperation_liste_keys_dict_trie(dict_actions_triees))

(RecuperationMeilleureCombinaisonOpti(data, 500).
    portefeuille_meilleure_perf(liste_cles_dict_trie))
