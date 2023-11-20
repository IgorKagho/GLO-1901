import argparse
import json
import requests
from datetime import datetime, timedelta



def analyser_commande():
    
    """
    Générer un interpréteur de commande.

    Returns:
        Un objet Namespace tel que retourné par parser.parse_args().
        Cet objet aura l'attribut «symboles» représentant la liste des
        symboles à traiter, et les attributs «début», «fin» et «valeur»
        associés aux arguments optionnels de la ligne de commande.
    """
    
    parser = argparse.ArgumentParser(description='Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.')
    parser.add_argument('symboles', nargs = '+', help= "Nom d\'un symbole boursier")
    parser.add_argument('-d', '--début', type=str, help='Date recherchée la plus ancienne (format: AAAA-MM-JJ)')
    parser.add_argument('-f', '--fin', type=str, help='Date recherchée la plus ancienne (format: AAAA-MM-JJ)')
    parser.add_argument('-v', '--valeur_type', choices=['fermeture', 'ouverture', 'min', 'max', 'volume'], default= " Fermeture ", help='La valeur désirée (par défaut: fermeture)')
 
    return parser.parse_args()

 
def produire_historique(symbole, début, fin, valeur):
    symbole = {symbole}
    url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
    params = {'début': début, 'fin': fin}
    réponse = requests.get(url=url, params=params)
    
    if réponse.status_code == 200:
        réponse = json.loads(réponse.text)
        historique = réponse['historique']
        resultat = (datetime.strptime(date, '%Y-%m-%d').date(), valeur[valeur]), 
        for date, valeur in historique.items():
            print(resultat)
        
    else: 
        print(f"Erreur: {réponse.json().get('message', 'Erreur inconnue')}")
        return []
    
def afficher_resultat(symbole, début, fin, valeur):
    print(symbole={symbole}, début={début}, fin={fin}, valeur={valeur})
    print(historique)
    
if __name__ == "__main__":
    try:
        args = analyser_commande()
    
        for symbole in args.symboles:
            début = args.début if args.début else datetime.now().strftime('%Y-%m-%d')
            fin = args.fin if args.fin else datetime.now().strftime('%Y-%m-%d')
            historique = produire_historique(symbole, début, fin, args.valeur)
            afficher_resultat(symbole, début, fin, args.valeur, historique)
            
    except argparse.ArgumentError as erreur:
        print(f"Erreur lors de l'analyse des arguments : {erreur}")
    except SystemExit as erreur:
        print(f"Erreur système : {erreur}")
    
    
    
    

    