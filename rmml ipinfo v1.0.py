import tkinter as tk
from tkinter import messagebox  # Ajoutez ceci pour importer la classe messagebox
import requests
import os

def get_ip_info():
    ip_address = ip_entry.get()
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "success":
        info_text = f"Adresse IP: {data['query']}\n"
        info_text += f"Pays: {data['country']}\n"
        info_text += f"Région: {data['regionName']}\n"
        info_text += f"Code Postal: {data['zip']}\n"
        info_text += f"Organisation: {data['org']}\n"
        messagebox.showinfo("Informations IP", info_text)
    else:
        messagebox.showerror("Erreur", "Impossible de trouver des informations pour cette adresse IP.")

root = tk.Tk()
root.title("projet rmml")

os.system("Title Project rmml")

ip_label = tk.Label(root, text="Adresse IP:")
ip_label.grid(row=0, column=0, padx=10, pady=10)

ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

info_button = tk.Button(root, text="Obtenir Infos", command=get_ip_info)
info_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
