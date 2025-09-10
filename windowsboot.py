#!/usr/bin/env python3
import subprocess
import sys
import re
import os

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    else:
        subprocess.run(cmd, check=True)

def parse_efibootmgr():
    output = run(["efibootmgr", "-v"], capture=True)
    entries = {}
    bootorder = None

    for line in output.splitlines():
        if line.startswith("BootOrder:"):
            bootorder = line.split(":")[1].strip()
        else:
            match = re.match(r"Boot([0-9A-Fa-f]{4})\*?\s+(.*)", line)
            if match:
                bootnum = match.group(1)
                desc = match.group(2).split("HD(")[0].strip()
                entries[bootnum] = desc

    return bootorder, entries

def find_windows_bootnum(entries):
    for bootnum, desc in entries.items():
        if "Windows Boot Manager" in desc:
            return bootnum
    return None

def detect_gui_tool():
    # Prefer KDE if available
    if shutil_which("kdialog"):
        return "kdialog"
    # Else use GNOME zenity
    if shutil_which("zenity"):
        return "zenity"
    return None

def shutil_which(cmd):
    from shutil import which
    return which(cmd) is not None

def notify(message, tool):
    if tool == "kdialog":
        subprocess.run(["kdialog", "--passivepopup", message, "3"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif tool == "zenity":
        subprocess.run(["zenity", "--info", "--text", message],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print(message)

def ask_confirmation(full_message, tool):
    if sys.stdin.isatty():
        print(full_message)
        answer = input("\nConfirm (y/N): ").strip().lower()
        return answer == "y", False
    else:
        if tool == "kdialog":
            result = subprocess.run(["kdialog", "--yesno", full_message],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode == 0, True
        elif tool == "zenity":
            result = subprocess.run(["zenity", "--question", "--text", full_message],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode == 0, True
        else:
            return False, False

def main():
    bootorder, entries = parse_efibootmgr()
    if not entries or not bootorder:
        print("ERROR: No boot entries found via efibootmgr.")
        sys.exit(1)

    bootnum = find_windows_bootnum(entries)
    if not bootnum:
        print("\nERROR: Windows Boot Manager not found in efibootmgr output.")
        sys.exit(1)

    log_text = []
    log_text.append(f"Would you like to initiate a one-time boot into Windows now (Boot{bootnum} → {entries[bootnum]})?")
    log_text.append("")
    log_text.append("=== UEFI Boot Info ===")
    log_text.append("Current Boot Priority (BootOrder):")
    for idx, bnum in enumerate(bootorder.split(","), start=1):
        desc = entries.get(bnum, "Unknown")
        log_text.append(f"{idx}) Boot{bnum} → {desc}")
    full_message = "\n".join(log_text)

    gui_tool = detect_gui_tool()
    confirmed, gui_mode = ask_confirmation(full_message, gui_tool)

    if not confirmed:
        if gui_mode:
            notify("boot aborted, killing process", gui_tool)
        else:
            print("boot aborted, killing process")
        sys.exit(0)

    run(["efibootmgr", "-n", bootnum])
    run(["reboot"])

if __name__ == "__main__":
    main()
