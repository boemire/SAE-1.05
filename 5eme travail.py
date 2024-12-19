import markdown
from prettytable import PrettyTable
import matplotlib.pyplot as plt
from pathlib import Path

# Fonction pour générer un tableau HTML des séances de R1.07
def generer_tableau_r107(seances):
    table = PrettyTable()
    table.field_names = ["Date de la séance", "Durée", "Type de séance"]
    
    for seance in seances:
        table.add_row([seance["date"], seance["duree"], seance["type"]])
    
    return table.get_html_string()

# Fonction pour créer un diagramme circulaire et l'enregistrer
def generer_diagramme_circulaire(compte, fichier_image):
    labels = list(compte.keys())
    valeurs = list(compte.values())
    
    plt.pie(valeurs, labels=labels, autopct='%1.1f%%', startangle=90, colors=["blue", "orange", "green", "red"])
    plt.title("Répartition des séances de TP du groupe A1 par mois")
    plt.savefig(fichier_image)
    plt.close()

# Fonction pour générer un fichier HTML
def generer_html(tableau_html, fichier_image):
    contenu_markdown = f"""
# Rapport des travaux

## Tableau des séances de R1.07
{tableau_html}

## Diagramme circulaire des séances de TP du groupe A1
![Diagramme circulaire]({fichier_image})
    """
    
    contenu_html = markdown.markdown(contenu_markdown, extensions=["tables"])
    with open("rapport.html", "w", encoding="utf-8") as f:
        f.write(contenu_html)
    
    print("Fichier HTML généré : rapport.html")

# Exemple d'utilisation
seances_r107 = [
    {"date": "2023-09-19 08:00", "duree": "2.0 heures", "type": "TP"},
    {"date": "2023-10-12 08:00", "duree": "2.0 heures", "type": "TP"},
    {"date": "2023-11-15 08:00", "duree": "2.0 heures", "type": "TP"},
    {"date": "2023-12-20 08:00", "duree": "2.0 heures", "type": "TP"}
]

compte_seances = {
    "Septembre": 1,
    "Octobre": 1,
    "Novembre": 1,
    "Décembre": 1
}

# Générer les éléments nécessaires
tableau_html = generer_tableau_r107(seances_r107)
fichier_image = "diagramme_circulaire.png"
generer_diagramme_circulaire(compte_seances, fichier_image)

# Générer le fichier HTML
generer_html(tableau_html, fichier_image)
