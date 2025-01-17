import tkinter as tk
from tkinter import filedialog, messagebox
import re
import csv
from collections import Counter, defaultdict
import webbrowser
from datetime import datetime

def parse_tcpdump(filename):
    packets = []
    with open(filename, 'r') as file:
        for line in file:
            match = re.search(r'(\S+) IP (\S+)[.:](\d+) [>-] (\S+)[.:](\d+).*', line)
            if match:
                timestamp, src_ip, src_port, dst_ip, dst_port = match.groups()
                protocol = 'TCP' if 'TCP' in line else 'UDP' if 'UDP' in line else 'Unknown'
                packets.append({
                    'timestamp': timestamp,
                    'src_ip': src_ip,
                    'src_port': int(src_port),
                    'dst_ip': dst_ip,
                    'dst_port': int(dst_port),
                    'protocol': protocol
                })
    return packets

def analyze_packets(packets):
    src_ips = Counter(p['src_ip'] for p in packets)
    dst_ips = Counter(p['dst_ip'] for p in packets)
    connections = Counter((p['src_ip'], p['dst_ip']) for p in packets)
    
    port_scans = defaultdict(set)
    for p in packets:
        port_scans[(p['src_ip'], p['dst_ip'])].add(p['dst_port'])
    
    udp_traffic = Counter((p['src_ip'], p['dst_ip']) for p in packets if p['protocol'] == 'UDP')
    
    ssh_attempts = Counter((p['src_ip'], p['dst_ip']) for p in packets if p['dst_port'] == 22)
    
    hourly_activity = defaultdict(int)
    for p in packets:
        hour = datetime.strptime(p['timestamp'], '%H:%M:%S.%f').hour
        hourly_activity[hour] += 1
    
    return src_ips, dst_ips, connections, port_scans, udp_traffic, ssh_attempts, hourly_activity

def generate_csv(packets, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'src_ip', 'src_port', 'dst_ip', 'dst_port', 'protocol']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for packet in packets:
            writer.writerow(packet)

def generate_report(src_ips, dst_ips, connections, port_scans, udp_traffic, ssh_attempts, hourly_activity):
    report = "# Rapport d'analyse réseau\n\n"
    
    report += "## IP sources les plus fréquentes\n"
    for ip, count in src_ips.most_common(10):
        report += f"- {ip}: {count}\n"
    
    report += "\n## IP destinations les plus fréquentes\n"
    for ip, count in dst_ips.most_common(10):
        report += f"- {ip}: {count}\n"
    
    report += "\n## Connexions les plus fréquentes\n"
    for (src, dst), count in connections.most_common(10):
        report += f"- {src} -> {dst}: {count}\n"
    
    report += "\n## Scans de ports potentiels\n"
    for (src, dst), ports in port_scans.items():
        if len(ports) > 10:
            report += f"- {src} a scanné {len(ports)} ports sur {dst}\n"
    
    report += "\n## Trafic UDP suspect\n"
    for (src, dst), count in udp_traffic.most_common(5):
        report += f"- {src} -> {dst}: {count} paquets UDP\n"
    
    report += "\n## Tentatives de connexion SSH\n"
    for (src, dst), count in ssh_attempts.most_common(5):
        report += f"- {src} -> {dst}: {count} tentatives\n"
    
    report += "\n## Activité par heure\n"
    for hour, count in sorted(hourly_activity.items()):
        report += f"- {hour}h: {count} paquets\n"
    
    return report

class TcpdumpAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analyseur de fichier tcpdump")
        self.geometry("400x300")

        self.file_path = tk.StringVar()
        
        tk.Label(self, text="Fichier tcpdump:").pack(pady=10)
        tk.Entry(self, textvariable=self.file_path, width=50).pack()
        tk.Button(self, text="Parcourir", command=self.browse_file).pack(pady=5)
        
        tk.Button(self, text="Analyser", command=self.analyze).pack(pady=20)
        tk.Button(self, text="Voir le rapport", command=self.view_report).pack()
        tk.Button(self, text="Ouvrir CSV", command=self.open_csv).pack(pady=5)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
        self.file_path.set(filename)

    def analyze(self):
        if not self.file_path.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier tcpdump")
            return

        try:
            packets = parse_tcpdump(self.file_path.get())
            src_ips, dst_ips, connections, port_scans, udp_traffic, ssh_attempts, hourly_activity = analyze_packets(packets)
            
            report = generate_report(src_ips, dst_ips, connections, port_scans, udp_traffic, ssh_attempts, hourly_activity)
            with open('rapport.md', 'w') as f:
                f.write(report)
            
            generate_csv(packets, 'packets.csv')
            
            messagebox.showinfo("Succès", "Analyse terminée. Rapport et CSV générés.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def view_report(self):
        try:
            webbrowser.open('rapport.md')
        except:
            messagebox.showerror("Erreur", "Impossible d'ouvrir le rapport")

    def open_csv(self):
        try:
            webbrowser.open('packets.csv')
        except:
            messagebox.showerror("Erreur", "Impossible d'ouvrir le fichier CSV")

if __name__ == "__main__":
    app = TcpdumpAnalyzer()
    app.mainloop()
