from pathlib import Path

def lire_fichier_ics(chemin_fichier):
    """Lit le contenu d'un fichier ICS et le retourne sous forme de texte."""
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()
    return contenu

chemin_fichier = Path(r"C:\Users\marti\Documents\cour\sae 1.05\evenementSAE_15.ics")
contenu = lire_fichier_ics(chemin_fichier)
print(contenu)
