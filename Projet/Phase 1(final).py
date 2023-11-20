import argparse
import json
import requests
from datetime import datetime

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
    parser.add_argument('symboles', nargs='+', help="Nom d\'un symbole boursier")
    parser.add_argument('-d', '--debut', type=str, help='Date recherchée la plus ancienne (format: AAAA-MM-JJ)')
    parser.add_argument('-f', '--fin', type=str, help='Date recherchée la plus ancienne (format: AAAA-MM-JJ)')
    parser.add_argument('-v', '--valeur_type', choices=['fermeture', 'ouverture', 'min', 'max', 'volume'], default="fermeture", help='La valeur désirée (par défaut: fermeture)')

    return parser.parse_args()


def produire_historique(symbole, début, fin, valeur):
    url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
    params = {'debut': début, 'fin': fin}
    réponse = requests.get(url=url, params=params)

    if réponse.status_code == 200:
        réponse = json.loads(réponse.text)
        historique = réponse['historique']

        for date, valeurs in historique.items():
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            résultat = {
                'compagnie': réponse['compagnie'],
                'symbole': symbole,
                'période': f'du {début} au {fin}',
                'historique': {
                    date: {k: valeurs[k] for k in valeurs if k == valeur}
                }
            }
            print(json.dumps(résultat, indent=2))

    else:
        print(f"Erreur: {réponse.json().get('message', 'Erreur inconnue')}")
        return []


if __name__ == "__main__":
    try:
        args = analyser_commande()
    
    except argparse.ArgumentError as erreur:
        print(f"Erreur lors de l'analyse des arguments : {erreur}")
    except SystemExit as erreur:
        print(f"Erreur système : {erreur}")

    for symbole in args.symboles:
        début = args.debut if args.debut else (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        fin = args.fin if args.fin else datetime.now().strftime('%Y-%m-%d')

        produire_historique(symbole, début, fin, args.valeur_type)