import argparse
import json
import requests
from datetime import datetime, date

class ErreurDate(Exception):
    pass

class Bourse:
    def __init__(self):
        pass

    def analyser_commande(self):
        parser = argparse.ArgumentParser(description='Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.')
        parser.add_argument('symboles', nargs='+', help="Nom d'un symbole boursier")
        parser.add_argument('-d', '--début', type=str, help='Date recherchée la plus ancienne (format: AAAA-MM-JJ)')
        parser.add_argument('-f', '--fin', type=str, help='Date recherchée la plus récente (format: AAAA-MM-JJ)')
        parser.add_argument('-v', '--valeur_type', choices=['fermeture', 'ouverture', 'min', 'max', 'volume'], default="fermeture", help='La valeur désirée (par défaut: fermeture)')
        return parser.parse_args()

    def _produire_historique(self, symbole, début, fin, valeur):
        symbole = {symbole}
        url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
        params = {'début': début, 'fin': fin}
        réponse = requests.get(url=url, params=params)

        if réponse.status_code == 200:
            réponse = json.loads(réponse.text)
            
            for clé in réponse.keys():
                print(clé)
            
            historique = réponse['historique']
            resultat = [(datetime.strptime(date, '%Y-%m-%d').date(), valeur[valeur]) for date, valeur in historique.items()]
            return resultat
        else:
            print(f"Erreur: {réponse.json().get('message', 'Erreur inconnue')}")
            return []

    def _afficher_resultat(self, symbole, début, fin, valeur, historique):
        print(f"symbole={symbole}, début={début}, fin={fin}, valeur={valeur}")
        print(historique)

    def prix(self, symbole, date):
        début = date.strftime('%Y-%m-%d')
        fin = date.strftime('%Y-%m-%d')

        historique = self._produire_historique(symbole, début, fin, 'fermeture')

        if not historique:
            raise ErreurDate(f"Aucune donnée disponible pour la date {date}")

        prix_date = None

        for h_date, prix in historique:
            if h_date <= date:
                prix_date = prix
            else:
                break

        if prix_date is None:
            raise ErreurDate(f"Aucune donnée disponible pour la date {date}")

        return prix_date

    def executer(self):
        try:
            args = self.analyser_commande()

            for symbole in args.symboles:
                date_début = datetime.strptime(args.début, '%Y-%m-%d').date() if args.début else date.today()  # Correction ici
                
                try:
                    prix_date = self.prix(symbole, date_début)
                    self._afficher_resultat(symbole, date_début, date_début, args.valeur_type, [(date_début, prix_date)])
                except ErreurDate as erreur:
                    print(f"Erreur lors de la récupération du prix : {erreur}")

        except argparse.ArgumentError as erreur:
            print(f"Erreur lors de l'analyse des arguments : {erreur}")
        except SystemExit as erreur:
            print(f"Erreur système : {erreur}")

if __name__ == "__main__":
    bourse = Bourse()
    bourse.executer()
