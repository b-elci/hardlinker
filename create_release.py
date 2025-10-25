"""
HardLinker Release Package Creator
Dağıtım için gerekli dosyaları bir klasöre toplar
"""

import os
import shutil
from datetime import datetime

# Release klasörü adı
release_name = f"HardLinker_v1.0_{datetime.now().strftime('%Y%m%d')}"
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
    ("README.md", "README.md"),
    ("settings.py", "settings.py"),
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
install_guide = """# 🔗 HardLinker v1.0 - Installation Guide

## 📥 Installation

1. Copy **HardLinker.exe** to any folder you like
2. No installation required - directly executable
3. Windows Defender/SmartScreen warning may appear on first run:
   - Click "More info" option
   - Click "Run anyway" button

## 🚀 Usage

1. Double-click **HardLinker.exe** to start the program
2. May request administrator rights on first use (required to create hardlinks)
3. Select folder to scan
4. Click "Start Scan" button
5. Review results and confirm with "Create Hardlinks"

## ⚠️ Important Notes

- **Administrator Rights**: It's recommended to run the program as administrator
- **First Use**: Back up your important files
- **System Folders**: Be careful with C:\\Windows, C:\\Program Files, etc.
- **Same Disk**: Hardlinks only work within the same disk partition (e.g., within C:)

## 🛡️ Security

- Program contains no viruses/malware
- Uses Windows' native hardlink feature
- Source code can be reviewed: github.com/...

## 📞 Support

For any issues:
- GitHub Issues
- Email: [email address]

## 📜 License

Free to use - For personal and commercial use

---

**Developer**: Barış Elçi
**Version**: 1.0
**Date**: 2025
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
