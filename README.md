# Homelab Hardware Development
Inventory and management of a high-powered Linux Homelab infrastructure supporting projects created by Andrew John Holland using the PMBOK project structure.
## Overview
Supports Andrew's self-study to build a high-powered Linux Homelab with a high-speed managed Unifi Network to enhance my career studies and future employment opportunities.
.
## Components
### Network Equipment
- **TOT Zyxel EX3301-T0**: ISP GPON ONT, WAN to Netgate pfSense+, LAN DHCP, confirm bridge mode.
- **Ubiquiti UniFi Switch Lite 16 PoE**: 16x GbE (8x PoE+), manages U6-Pro, G5 Flex, Synology DS1821+, DS916+ (LACP), auto-update via UDM-Pro.
- **Ubiquiti UniFi Dream Machine Pro**: 8x GbE LAN, 1x GbE WAN, 2x 10G SFP+, security, video, VPN, auto-update.
- **Ubiquiti UniFi Access Point WiFi 6 Pro**: 802.11ax, PoE+, wireless segmentation, auto-update via UDM-Pro.
- **Ubiquiti UniFi Protect Camera G5 Flex**: 2K resolution, PoE, monitoring, auto-update via UDM-Pro.
- **Netgate 1100 pfSense+**: 3x 1 GbE, firewall, VPN, intrusion detection, auto-update.
- **Proposed Secondary Switch (Ubiquiti USW-Lite-8-PoE)**: 8x GbE (4x PoE+), network expansion, auto-update.

### Hardware Equipment
Custom Server: (Fractal Define 7 XL, PVENAS1)

- Motherboard: HUANANZHI X99 F8D X99 
- Processors: Dual Intel Xeon E5-2678 v3 (24 cores / 48 threads total, 60 MB L3 cache) 
- Memory: 64GB DDR4 RAM (4*16GB RECC memory) 
- Remote Access: KVM-A8 
- Use Case: Virtualization, backups, storage (TBD) 
- Optimized for compute-intensive workloads such as virtualization, database operations, rendering, and scientific simulations 
.
- **Alienware Alpha R2 (PVEHASS)**: Mid-range CPU, 8GB RAM, virtualization, home automation.
- **ASUS ROG Strix PC (ROGStix)**: High-performance CPU, 32GB RAM, gaming GPU, tutoring, gaming, storage TBD.
- **Samsung Galaxy Book Flex**: TBD specs, management, tutoring.
- **Samsung Galaxy S23 Ultra**: High-end mobile processor, 12GB RAM, remote management.
- **Samsung SmartThings Hub**: Home automation.
  .
### Software
- **Operating Systems**: DSM, Proxmox, Windows 10, Linux, Android, auto-update.
- **Network Services**: Pi-hole 6, WireGuard, pfSense+, PiKVM, Tailscale, auto-update.
- **Applications**: Home Assistant, Emby, Hyper Backup, Docker, Traefik, auto-update.
  .
<img src="https://github.com/silicastormsiam/homelab-hardware-development/raw/main/AsusROG_1920x1080.jpg" alt="Asus ROG BG">
<a href="https://www.proxmox.com/en/"><img src="https://img.shields.io/badge/Proxmox-E754AA?logo=proxmox&style=flat-square" alt="Proxmox" style="margin-right: 5px; border: 1px solid #00BF00;"></a>
<a href="https://www.linux.org/"><img src="https://img.shields.io/badge/Linux-00BF00?logo=linux&style=flat-square" alt="Linux" style="margin-right: 5px; border: 1px solid #E754AA;"></a>
<a href="https://www.microsoft.com/en-us/windows-server"><img src="https://img.shields.io/badge/Windows_Server-2596be?logo=windows&style=flat-square" alt="Windows Server" style="border: 1px solid #E754AA;"></a>



