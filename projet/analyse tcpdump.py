import os
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import pandas as pd
import webbrowser

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

        csv_file = os.path.splitext(file_path)[0] + "_analyse.csv"
        try:
            self.process_txt_to_csv(file_path, csv_file)
            self.open_csv_file(csv_file)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

    def process_txt_to_csv(self, txt_file, csv_file):
        data = []
        with open(txt_file, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 5:  # Supposons que chaque ligne contient au moins 5 colonnes
                    frame, src_ip, dst_ip, timestamp, length = parts[:5]
                    # Validation pour les longueurs
                    try:
                        length = int(length)
                        # Critères pour identifier les activités suspectes
                        if (length > 9000 or  # Taille supérieure à 9000 octets
                            (src_ip.startswith("192.168") and dst_ip.startswith("10.")) or  # Communication interne-externe
                            dst_ip.endswith(".255")):  # Trafic broadcast
                            data.append([frame, src_ip, dst_ip, timestamp, length])
                    except ValueError:
                        continue  # Ignorer les lignes avec des longueurs non valides

        # Conversion des données en DataFrame
        df = pd.DataFrame(data, columns=["Trame", "IP Source", "IP Destination", "Horodatage", "Longueur"])
        df.to_csv(csv_file, index=False)

    def open_csv_file(self, csv_file):
        webbrowser.open(csv_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalyseurTCPDump(root)
    root.mainloop()
