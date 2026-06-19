# ⚡ DEAUTH MASTER

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.0-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Platform-Kali%20Linux-brightgreen?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

<p align="center">
  <b>🔥 Ultimate WiFi Deauthentication Attack Tool 🔥</b><br>
  <i>Gabungan 5 Tools Bawaan Kali Linux dalam 1 Tools</i>
</p>

---

## 📌 Deskripsi

**DEAUTH MASTER** adalah tools **WiFi Deauthentication Attack** yang menggabungkan **5 tools bawaan Kali Linux** dalam satu interface yang keren dan mudah digunakan.

Tools ini dirancang untuk **testing keamanan jaringan WiFi** dan **penetration testing** dengan izin.

---

## 🚀 Fitur Unggulan

| Fitur | Deskripsi |
|-------|-----------|
| 🎯 **5 Tools Dalam 1** | Airmon-ng + Airodump-ng + Aireplay-ng + MDK4 + Bettercap |
| ⚡ **3 Mode Attack** | Aireplay (Stabil) + MDK4 (Brutal) + Bettercap (Modern) |
| 🎨 **Design Keren** | Tampilan terminal interaktif dengan warna |
| 📡 **Auto Scan** | Scan otomatis AP dan client di sekitar |
| 🎯 **Target Spesifik** | Attack client tertentu atau semua client |
| 🧹 **Auto Cleanup** | Bersihkan monitor mode otomatis setelah selesai |

---

## 🛠️ Prasyarat

### Hardware
- WiFi adapter yang support **Monitor Mode** dan **Packet Injection**
- Rekomendasi: Alfa AWUS036ACH, TP-Link TL-WN722N v1, atau chipset Atheros AR9271

### Software
- Kali Linux (tools bawaan sudah tersedia)
- Python 3.x

---

## 📦 Instalasi

### 1. Install Dependencies

## clone repository
git clone https://github.com/daffazxxs/DeautherX.git

cd DeautherX

## Jalankan Tools ini
# Beri izin execute
chmod +x deauth_master.py

# Jalankan (WAJIB ROOT)
sudo python3 deauth_master.py



```bash
# Install tools yang dibutuhkan (jika belum ada)
sudo apt update
sudo apt install aircrack-ng mdk4 bettercap -y

# Install Python library
pip install colorama
