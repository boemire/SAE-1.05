from datetime import datetime, timedelta
from prettytable import PrettyTable

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
    
    return evenements

# Fonction pour convertir une date ICS en format lisible
def formater_date(date_ics):
    return datetime.strptime(date_ics, "%Y%m%dT%H%M%SZ")

# Fonction pour calculer la durée en heures
def calculer_duree(debut, fin):
    delta = fin - debut
    return delta.total_seconds() / 3600

# Fonction pour extraire le type de séance
def extraire_type_seance(resume):
    if "CM" in resume:
        return "CM"
    elif "TD" in resume:
        return "TD"
    elif "TP" in resume:
        return "TP"
    return "Inconnu"

# Fonction principale pour extraire les séances de R1.07 (TP)
def extraire_seances_r107(fichier_ics):
    evenements = lire_ics(fichier_ics)
    seances_r107 = []
    
    for evenement in evenements:
        resume = evenement.get('resume', "")
        if "R1.07" in resume and "TP" in resume:
            debut = formater_date(evenement['debut'])
            fin = formater_date(evenement['fin'])
            duree = calculer_duree(debut, fin)
            type_seance = extraire_type_seance(resume)
            
            seances_r107.append({
                "date": debut.strftime("%Y-%m-%d %H:%M"),
                "duree": f"{duree:.1f} heures",
                "type": type_seance
            })
    
    return seances_r107

# Fonction pour afficher le tableau des séances
def afficher_tableau_seances(seances):
    table = PrettyTable()
    table.field_names = ["Date de la séance", "Durée", "Type de séance"]
    
    for seance in seances:
        table.add_row([seance["date"], seance["duree"], seance["type"]])
    
    print(table)

# Exemple d'utilisation
fichier_ics = r"C:\Users\marti\Documents\cour\SAE-1.05\ADE_RT1_Septembre2023_Decembre2023.ics"
seances_r107 = extraire_seances_r107(fichier_ics)
afficher_tableau_seances(seances_r107)
