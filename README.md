# SPYNET WiFi Jammer Tool

**SPYNET** is an advanced Python-based tool designed for educational and ethical hacking purposes. It allows users to simulate WiFi jamming attacks by sending deauthentication packets to disconnect devices from a selected WiFi network. Key features include:

### Features:
- **WiFi Network Scanning**: Automatically scans and lists nearby **WiFi networks** (SSIDs) and their **MAC addresses**.
  - Provides the ability to identify **hidden networks**.
- **Device Scanning**: Detects and lists **connected devices** (clients) on a selected network by sniffing **data frames**.
  - Displays **MAC addresses** of devices connected to the chosen network for targeting.
- **Deauthentication Attack**: Allows users to initiate a **deauthentication attack** on selected devices or networks.
  - Sends **deauth packets** to disconnect devices from their respective WiFi access points (APs).
- **Real-time Attack Status**: Provides live **status updates** and logs during the attack (e.g., packets sent, devices targeted, etc.).
  - Displays attack results and successful disconnections in a **scrollable status window**.
- **Proxy List Support**: Supports loading a **proxy list** from a file to route attack traffic through multiple IPs (helps evade IP-based blocking or detection).
  - Option to scan and load **public proxy lists** for use.
- **User-friendly GUI**: Built with **Tkinter**, providing an easy-to-use, graphical interface.
  - Features dropdowns for network selection, client targeting, and live logs for attack status.
- **Monitor Mode Interface Support**: Allows users to specify the network interface in **monitor mode** (e.g., `wlan0mon`), required for sniffing and sending raw packets.
- **Customizable Attack Settings**: Ability to adjust attack parameters like **attack duration**, **frequency of deauthentication packets**, and **number of packets to send**.
- **Cross-platform Compatibility**: Works on **Linux**, **MacOS**, and **Windows** (with the right WiFi adapter) for versatile usage.

### Important Notes:
- This tool is designed for **ethical hacking**, **penetration testing**, and **educational purposes** only. **Use responsibly** and always **obtain permission** before testing any network.
- **WiFi jamming is illegal** in many regions and can lead to **legal consequences** if used without consent.

### Installation:
To install the required dependencies, run:
```bash
pip install -r requirements.txt
```
Usage:
1. Put your WiFi interface into monitor mode.
2. Run the tool with:
```bash
python spynet_jammer.py
```
3. Follow the instructions in the GUI to scan networks, select a target device, and start the attack.
