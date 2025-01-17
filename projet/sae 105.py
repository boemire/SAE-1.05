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
        
        tk.Label(root, text="Sélectionnez le fichier TCPDump (TXT ou CSV) :").pack(pady=5)
        tk.Entry(root, textvariable=self.file_path, width=50).pack(pady=5)
        tk.Button(root, text="Parcourir", command=self.browse_file).pack(pady=5)
        tk.Button(root, text="Analyser", command=self.analyze_file).pack(pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers texte et CSV", "*.txt;*.csv"), ("Tous les fichiers", "*.*")])
        if file_path:
            self.file_path.set(file_path)

    def analyze_file(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier.")
            return

        try:
            if file_path.endswith(".csv"):
                self.process_csv(file_path)
            elif file_path.endswith(".txt"):
                self.process_txt(file_path)
            else:
                messagebox.showerror("Erreur", "Format de fichier non pris en charge.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

    def process_txt(self, txt_file):
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

        self.plot_top_ips(ip_counts)

    def process_csv(self, csv_file):
        df = pd.read_csv(csv_file)
        if "Source" not in df.columns or "Destination" not in df.columns:
            messagebox.showerror("Erreur", "Le fichier CSV doit contenir des colonnes 'Source' et 'Destination'.")
            return

        ip_counts = {}
        for src_ip, dst_ip in zip(df["Source"], df["Destination"]):
            ip_counts[src_ip] = ip_counts.get(src_ip, 0) + 1
            ip_counts[dst_ip] = ip_counts.get(dst_ip, 0) + 1

        self.plot_top_ips(ip_counts)

    def plot_top_ips(self, ip_counts):
        # Transformer les données en DataFrame
        df = pd.DataFrame(list(ip_counts.items()), columns=["Adresse IP", "Occurrences"])

        # Trier par nombre d'occurrences et sélectionner les 10 premières
        top_ips = df.sort_values(by="Occurrences", ascending=False).head(10)

        # Création du graphique en camembert
        plt.figure(figsize=(10, 10))
        plt.pie(
            top_ips["Occurrences"],
            labels=[f"{ip}" for ip in top_ips["Adresse IP"]],
            autopct="%1.1f%%",
            startangle=140,
            colors=plt.cm.tab20.colors
        )
        plt.title("Top 10 des adresses IP les plus visitées")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalyseurTCPDump(root)
    root.mainloop()

