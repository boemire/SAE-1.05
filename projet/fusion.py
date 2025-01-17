import tkinter as tk
from tkinter import filedialog, messagebox
import re
import csv
from collections import Counter, defaultdict
import webbrowser
from datetime import datetime
import matplotlib.pyplot as plt

def parse_tcpdump(filename):
    packets = []
    with open(filename, 'r') as file:
        for line in file:
            match = re.search(r'(?P<timestamp>\S+) IP (?P<src_ip>\S+)[.:](?P<src_port>\d+) [>-] (?P<dst_ip>\S+)[.:](?P<dst_port>\d+).*', line)
            if match:
                protocol = 'TCP' if 'TCP' in line else 'UDP' if 'UDP' in line else 'Unknown'
                packets.append({
                    'timestamp': match.group('timestamp'),
                    'src_ip': match.group('src_ip'),
                    'src_port': int(match.group('src_port')),
                    'dst_ip': match.group('dst_ip'),
                    'dst_port': int(match.group('dst_port')),
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

def generate_pie_chart(src_ips):
    top_ips = src_ips.most_common(5)
    labels = [ip for ip, _ in top_ips]
    sizes = [count for _, count in top_ips]

    other_ips = sum(src_ips.values()) - sum(sizes)
    if other_ips > 0:
        labels.append('Autres')
        sizes.append(other_ips)

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab10.colors)
    plt.title("Top 5 IP sources les plus fréquentes")
    plt.axis('equal')
    plt.savefig("top_ips_pie_chart.png")
    plt.show()

class TcpdumpAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analyseur de fichier tcpdump")
        self.geometry("400x400")

        self.file_path = tk.StringVar()

        tk.Label(self, text="Fichier tcpdump:").pack(pady=10)
        tk.Entry(self, textvariable=self.file_path, width=50).pack()
        tk.Button(self, text="Parcourir", command=self.browse_file).pack(pady=5)

        tk.Button(self, text="Analyser", command=self.analyze).pack(pady=20)
        tk.Button(self, text="Voir le rapport", command=self.view_report).pack()
        tk.Button(self, text="Ouvrir CSV", command=self.open_csv).pack(pady=5)
        tk.Button(self, text="Générer un graphique", command=self.generate_chart).pack(pady=5)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
        self.file_path.set(filename)

    def analyze(self):
        if not self.file_path.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier tcpdump")
            return

        try:
            self.packets = parse_tcpdump(self.file_path.get())
            self.src_ips, self.dst_ips, self.connections, self.port_scans, self.udp_traffic, self.ssh_attempts, self.hourly_activity = analyze_packets(self.packets)

            report = generate_report(self.src_ips, self.dst_ips, self.connections, self.port_scans, self.udp_traffic, self.ssh_attempts, self.hourly_activity)
            with open('rapport.md', 'w') as f:
                f.write(report)

            generate_csv(self.packets, 'packets.csv')

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

    def generate_chart(self):
        if hasattr(self, 'src_ips'):
            generate_pie_chart(self.src_ips)
        else:
            messagebox.showerror("Erreur", "Veuillez d'abord analyser un fichier tcpdump")

if __name__ == "__main__":
    app = TcpdumpAnalyzer()
    app.mainloop()


