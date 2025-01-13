import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

class AnalyseurTCPDump:
    def __init__(self, root):
        self.root = root
        self.root.title("Analyseur TCPDump")
        
        self.file_path = tk.StringVar()
        
        tk.Label(root, text="Sélectionnez le fichier texte TCPDump :").pack(pady=5)
        tk.Entry(root, textvariable=self.file_path, width=50).pack(pady=5)
        tk.Button(root, text="Parcourir", command=self.browse_file).pack(pady=5)
        tk.Button(root, text="Analyser", command=self.analyze_file).pack(pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
        if file_path:
            self.file_path.set(file_path)

    def analyze_file(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier.")
            return

        try:
            self.process_and_plot(file_path)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

    def process_and_plot(self, txt_file):
        ip_counts = {}

        with open(txt_file, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 3:  # Supposons que la source et destination IP sont présentes
                    src_ip = parts[1]  # Exemple : colonne de l'IP source
                    dst_ip = parts[2]  # Exemple : colonne de l'IP destination

                    # Comptabiliser les occurrences des IP
                    ip_counts[src_ip] = ip_counts.get(src_ip, 0) + 1
                    ip_counts[dst_ip] = ip_counts.get(dst_ip, 0) + 1

        # Transformer les données en DataFrame
        df = pd.DataFrame(list(ip_counts.items()), columns=["Adresse IP", "Occurrences"])
        total_occurrences = df["Occurrences"].sum()

        # Calculer le pourcentage des occurrences
        df["Pourcentage"] = (df["Occurrences"] / total_occurrences) * 100

        # Filtrer les adresses IP avec un pourcentage > 1%
        filtered_df = df[df["Pourcentage"] > 1]

        # Création du graphique en camembert
        plt.figure(figsize=(10, 10))
        plt.pie(
            filtered_df["Pourcentage"],
            labels=filtered_df["Adresse IP"],
            autopct="%1.1f%%",
            startangle=140,
            colors=plt.cm.tab20.colors
        )
        plt.title("Répartition des adresses IP (> 1% d'apparition)")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalyseurTCPDump(root)
    root.mainloop()




