from pathlib import Path

def lire_fichier_ics(chemin_fichier):
    """Lit le contenu d'un fichier ICS et le retourne sous forme de texte."""
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()
    return contenu

def extraire_donnees_ics(contenu_ics):
    """Extrait les informations importantes d'un fichier ICS."""
    # Les lignes du fichier sont séparées par des sauts de ligne
    lignes = contenu_ics.splitlines()
    evenement = {}
    
    for ligne in lignes:
        if ligne.startswith("DTSTART:"):
            evenement["Début"] = ligne.split(":")[1]
        elif ligne.startswith("DTEND:"):
            evenement["Fin"] = ligne.split(":")[1]
        elif ligne.startswith("SUMMARY:"):
            evenement["Résumé"] = ligne.split(":", 1)[1]
        elif ligne.startswith("LOCATION:"):
            evenement["Lieu"] = ligne.split(":", 1)[1]
    
    return evenement

def convertir_en_csv(evenement):
    """Convertit un dictionnaire d'événement en pseudo-code CSV."""
    # Format CSV attendu (adapté selon les besoins)
    return f'{evenement.get("Début", "")};{evenement.get("Fin", "")};{evenement.get("Résumé", "")};{evenement.get("Lieu", "")}'

def main():
    # Remplacer 'evenementSAE_15GroupeA1.ics' par le chemin réel du fichier
    chemin_fichier = 'evenementSAE_15GroupeA1.ics'
    
    # Étapes
    chemin_fichier = Path(r"C:\Users\marti\Documents\cour\SAE-1.05\evenementSAE_15.ics")
    contenu_ics = lire_fichier_ics(chemin_fichier)
    evenement = extraire_donnees_ics(contenu_ics)
    chaine_csv = convertir_en_csv(evenement)
    
    # Afficher le résultat
    print("Pseudo-code CSV généré :")
    print(chaine_csv)

if __name__ == "__main__":
    main()
