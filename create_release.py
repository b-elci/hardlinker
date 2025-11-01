"""
HardLinker Release Package Creator
Dağıtım için gerekli dosyaları bir klasöre toplar
"""

import os
import shutil
from datetime import datetime

# Release klasörü adı
release_name = f"HardLinker_v1.0.1_{datetime.now().strftime('%Y%m%d')}"
release_path = f"releases/{release_name}"

# Eski release klasörünü temizle
if os.path.exists("releases"):
    shutil.rmtree("releases")

# Yeni release klasörünü oluştur
os.makedirs(release_path, exist_ok=True)

print("="*70)
print("📦 HARDLINKER RELEASE PACKAGE CREATOR")
print("="*70)
print(f"\n✨ Release name: {release_name}\n")

# Copy files
files_to_copy = [
    ("dist/HardLinker.exe", "HardLinker.exe"),
    ("hardlinker.ico", "hardlinker.ico"),
    ("README.txt", "README.txt"),
    ("LICENSE.txt", "LICENSE.txt"),
]

print("📋 Copying files...\n")

for source, dest in files_to_copy:
    if os.path.exists(source):
        dest_path = os.path.join(release_path, dest)
        shutil.copy2(source, dest_path)
        size = os.path.getsize(dest_path)
        print(f"  ✓ {dest:<25} ({size/1024/1024:.2f} MB)")
    else:
        print(f"  ✗ {source} not found!")

# Create installation guide
install_guide = """================================================================================
                         HardLinker v1.0.1
              Installation and Quick Start Guide for Windows
================================================================================

INSTALLATION
------------
1. Extract all files from the ZIP archive to any folder you like
2. No installation required - HardLinker.exe is a standalone executable
3. Keep all files together in the same folder

FIRST RUN
---------
When you run HardLinker.exe for the first time:

• Windows Defender/SmartScreen may show a warning (this is normal for new apps)
  - Click "More info"
  - Click "Run anyway"

• The program may request administrator rights
  - This is required to create hardlinks in some locations
  - Click "Yes" to allow

QUICK START
-----------
1. Double-click HardLinker.exe
2. Click "Browse Folder" and select a folder to scan
3. Click "Start Scan" to find duplicate files
4. Review the duplicate groups found
5. Click "Create Hardlinks" to save disk space
6. Done! Check the results summary

WHAT'S IN THIS PACKAGE
----------------------
• HardLinker.exe  - Main application (standalone executable)
• hardlinker.ico  - Application icon
• README.txt      - Full documentation and usage guide
• LICENSE.txt     - Software license (MIT License)
• INSTALL.txt     - This file

IMPORTANT NOTES
---------------
⚠️ Administrator Rights: Required for some hardlink operations
⚠️ Same Disk Only: Hardlinks work only within the same disk partition (e.g., C:)
⚠️ System Files: The program protects against critical system folders
⚠️ First Use: Keep backups of important files before first use

SYSTEM REQUIREMENTS
-------------------
• Windows 10 or Windows 11 (64-bit)
• At least 50 MB free disk space
• Administrator rights (recommended)

SUPPORT
-------
• GitHub: https://github.com/b-elci/hardlinker
• Buy Me a Coffee: https://buymeacoffee.com/bariselcii
• Issues: Report bugs on GitHub Issues page

SECURITY
--------
✓ No viruses or malware
✓ Uses Windows native hardlink feature
✓ Source code available on GitHub
✓ No internet connection required
✓ No data collection or telemetry

LICENSE
-------
This software is released under the MIT License.
Free for personal and commercial use.
See LICENSE.txt for full details.

================================================================================
                        Developer: Barış Elçi
                           Version: 1.0.1
                            Year: 2025
================================================================================
"""

with open(os.path.join(release_path, "INSTALL.txt"), "w", encoding="utf-8") as f:
    f.write(install_guide)

print(f"  ✓ INSTALL.txt")

# Create ZIP archive
print(f"\n📦 Creating ZIP archive...\n")
shutil.make_archive(f"releases/{release_name}", 'zip', release_path)

zip_size = os.path.getsize(f"releases/{release_name}.zip")
print(f"  ✓ {release_name}.zip ({zip_size/1024/1024:.2f} MB)")

print("\n" + "="*70)
print("✅ RELEASE PACKAGE READY!")
print("="*70)
print(f"\n📁 Folder: releases\\{release_name}")
print(f"📦 ZIP: releases\\{release_name}.zip")
print(f"\n💡 You can distribute the ZIP file!")
print("="*70)
