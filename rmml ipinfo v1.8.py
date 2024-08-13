import tkinter as tk
from tkinter import messagebox
import webbrowser
import requests
from concurrent.futures import ThreadPoolExecutor
from queue import Queue 
import os

os.system("Title Project rmml")

def fetch_ip_info(ip_address, result_queue):
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        response = requests.get(url)
        data = response.json()

        if data["status"] == "success":
            info_text = ""
            for key, value in data.items():
                if key in ["query", "country", "city", "regionName", "zip", "isp", "org", "lat", "lon", "timezone"]:
                    info_text += f"{key.capitalize()}: {value}\n"
            device_name = data.get('username', 'N/A')
            info_text += f"Nom appareil: {device_name}\n"
            result_queue.put(info_text)
        else:
            result_queue.put(None)
    except requests.exceptions.RequestException as e:
        result_queue.put(e)

def fetch_google_maps(ip_address, result_queue):
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        response = requests.get(url)
        data = response.json()

        if data["status"] == "success":
            latitude = data['lat']
            longitude = data['lon']
            base_url = "https://www.google.com/maps/search/?api=1"
            query = f"{latitude},{longitude}"
            url = f"{base_url}&query={query}"
            webbrowser.open_new_tab(url)
            result_queue.put(True)
        else:
            result_queue.put(None)
    except requests.exceptions.RequestException as e:
        result_queue.put(e)

def handle_result(result):
    if isinstance(result, str):
        messagebox.showinfo("Informations IP", result)
    elif result is None:
        messagebox.showerror("Erreur", "Impossible de trouver des informations pour cette adresse IP.")
    else:
        messagebox.showerror("Erreur de Connexion", f"Erreur de connexion: {result}")

def check_result(result_queue):
    if not result_queue.empty():
        result = result_queue.get()
        handle_result(result)
    else:
        root.after(100, check_result, result_queue)

def get_ip_info():
    ip_address = ip_entry.get()
    if not ip_address:
        messagebox.showerror("Erreur", "Veuillez entrer une adresse IP valide.")
        return

    result_queue = Queue()
    with ThreadPoolExecutor() as executor:
        executor.submit(fetch_ip_info, ip_address, result_queue)
    root.after(100, check_result, result_queue)

def open_google_maps():
    ip_address = ip_entry.get()
    if not ip_address:
        messagebox.showerror("Erreur", "Veuillez entrer une adresse IP valide.")
        return

    result_queue = Queue()
    with ThreadPoolExecutor() as executor:
        executor.submit(fetch_google_maps, ip_address, result_queue)
    root.after(100, check_result, result_queue)

root = tk.Tk()
root.title("Projet RMML")

ip_label = tk.Label(root, text="Adresse IP:")
ip_label.grid(row=1, column=0, padx=10, pady=10)

ip_entry = tk.Entry(root)
ip_entry.grid(row=1, column=1, padx=10, pady=10)

info_button = tk.Button(root, text="Obtenir Infos", command=get_ip_info)
info_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

maps_button = tk.Button(root, text="Ouvrir Google Maps", command=open_google_maps)
maps_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

root.mainloop()