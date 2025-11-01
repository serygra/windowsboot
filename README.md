# WindowsBoot Launcher for Linux

A Python utility + desktop launcher that lets you reboot into Windows once from Linux (UEFI dual-boot systems). 
I made this tool because I primary boot Nobara (KDE) and occasionally need to switch to Windows for gaming.
I made this configurable for GNOME as well since it just seemed like a few extra steps.
Making this public because I am 90% confident this works... USE AT YOUR OWN RISK!!!!!!!!!!

This script automatically detects your desktop environment:
- KDE Plasma → uses kdialog
- GNOME → uses zenity
- Falls back to terminal if no GUI tools are available

---

## Requirements
- UEFI firmware (not legacy BIOS)
- Linux with efibootmgr installed
- Python 3
- KDE users: kdialog
- GNOME users: zenity
- Either:
  - sudo configured to allow passwordless execution of the script (recommended), or
  - pkexec for GUI password prompts

On Arch Linux:
    sudo pacman -S efibootmgr kdialog zenity

On Fedora / Nobara:
    sudo dnf install efibootmgr kdialog zenity

---

## Installation

1. Clone the repository
    git clone https://github.com/yourname/windowsboot.git
    cd windowsboot

2. Install the script
    sudo cp windowsboot.py /usr/local/bin/windowsboot
    sudo chmod +x /usr/local/bin/windowsboot

3. Configure sudoers (recommended)
    sudo visudo

Add this line at the bottom (replace yourusername):
    yourusername ALL=(ALL) NOPASSWD: /usr/local/bin/windowsboot

4. Install the launcher
    cp windowsboot.desktop ~/.local/share/applications/
    kbuildsycoca5

---

## Usage

- In terminal: sudo windowsboot
- In GUI: search for "Windows Boot" in your application menu

---

## Example Popup

Would you like to initiate a one-time boot into Windows now (Boot0000 → Windows Boot Manager)?

=== UEFI Boot Info ===
Current Boot Priority (BootOrder):
1) Boot0001 → Fedora
2) Boot0000 → Windows Boot Manager
