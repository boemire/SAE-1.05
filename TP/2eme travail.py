from prettytable import PrettyTable
from datetime import datetime
from pathlib import Path

# Fonction pour lire un fichier ICS et extraire les événements
def lire_ics(fichier):
    evenements = []
    evenement = {}
    
    with open(fichier, 'r', encoding='utf-8') as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne.startswith("BEGIN:VEVENT"):
                evenement = {}
            elif ligne.startswith("END:VEVENT"):
                evenements.append(evenement)
            elif ligne.startswith("DTSTART:"):
                evenement['debut'] = ligne.replace("DTSTART:", "")
            elif ligne.startswith("DTEND:"):
                evenement['fin'] = ligne.replace("DTEND:", "")
            elif ligne.startswith("SUMMARY:"):
                evenement['resume'] = ligne.replace("SUMMARY:", "")
            elif ligne.startswith("LOCATION:"):
                evenement['lieu'] = ligne.replace("LOCATION:", "")
            elif ligne.startswith("DESCRIPTION:"):
                description = ligne.replace("DESCRIPTION:", "")
                professeurs = extraire_professeurs(description)
                evenement['professeurs'] = professeurs if professeurs else ["vide"]
    
    return evenements

# Fonction pour extraire les professeurs de la description
def extraire_professeurs(description):
    lignes = description.split("\\n")
    professeurs = [ligne for ligne in lignes if ligne.strip() and "Exporté le" not in ligne]
    return professeurs

# Fonction pour convertir une date ICS en format lisible
def formater_date(date_ics):
    return datetime.strptime(date_ics, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d %H:%M")

# Fonction principale pour afficher les événements sous forme de tableau
def afficher_tableau(fichier_ics):
    evenements = lire_ics(fichier_ics)
    
    # Création du tableau
    table = PrettyTable()
    table.field_names = ["Résumé", "Début", "Fin", "Lieu", "Professeurs"]
    
    for evenement in evenements:
        debut = formater_date(evenement.get('debut', '')) if 'debut' in evenement else "vide"
        fin = formater_date(evenement.get('fin', '')) if 'fin' in evenement else "vide"
        resume = evenement.get('resume', "vide")
        lieu = evenement.get('lieu', "vide")
        professeurs = ", ".join(evenement.get('professeurs', ["vide"]))
        
        table.add_row([resume, debut, fin, lieu, professeurs])
    
    print(table)

# Exemple d'utilisation
fichier_ics = r"C:\Users\marti\Documents\cour\SAE-1.05\ADE_RT1_Septembre2023_Decembre2023.ics"
afficher_tableau(fichier_ics)

