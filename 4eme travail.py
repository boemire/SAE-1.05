from datetime import datetime
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, save
from bokeh.io.export import export_png

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
            elif ligne.startswith("SUMMARY:"):
                evenement['resume'] = ligne.replace("SUMMARY:", "")
    
    return evenements

# Fonction pour filtrer les séances de TP pour le groupe A1
def filtrer_tp_a1(evenements):
    tp_a1 = []
    for evenement in evenements:
        resume = evenement.get('resume', "")
        if "TP" in resume and "A1" in resume:
            debut = datetime.strptime(evenement['debut'], "%Y%m%dT%H%M%SZ")
            tp_a1.append(debut)
    return tp_a1

# Fonction pour compter les séances par mois
def compter_seances_par_mois(seances):
    compte = {"Septembre": 0, "Octobre": 0, "Novembre": 0, "Décembre": 0}
    mois_mapping = {9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"}
    
    for seance in seances:
        mois = seance.month
        if mois in mois_mapping:
            compte[mois_mapping[mois]] += 1
    
    return compte

# Fonction pour créer un graphique en bâtons
def creer_graphe_seances(compte):
    # Création du graphique avec matplotlib
    mois = list(compte.keys())
    valeurs = list(compte.values())
    
    plt.bar(mois, valeurs, color=['blue', 'orange', 'green', 'red'])
    plt.title("Nombre de séances de TP du groupe A1 par mois")
    plt.xlabel("Mois")
    plt.ylabel("Nombre de séances")
    plt.savefig("graphe_seances_matplotlib.png")  # Export PNG avec matplotlib
    plt.show()
    
    # Création et exportation du graphique avec Bokeh
    p = figure(x_range=mois, title="Nombre de séances de TP du groupe A1 par mois",
               x_axis_label="Mois", y_axis_label="Nombre de séances", toolbar_location=None)
    p.vbar(x=mois, top=valeurs, width=0.5, color=["blue", "orange", "green", "red"])
    
    export_png(p, filename="graphe_seances_bokeh.png")
    print("Graphique exporté en format PNG sous le nom 'graphe_seances_bokeh.png'.")

# Exemple d'utilisation
fichier_ics = r"C:\Users\marti\Documents\cour\SAE-1.05\ADE_RT1_Septembre2023_Decembre2023.ics"
evenements = lire_ics(fichier_ics)
tp_a1 = filtrer_tp_a1(evenements)
compte_seances = compter_seances_par_mois(tp_a1)
creer_graphe_seances(compte_seances)
