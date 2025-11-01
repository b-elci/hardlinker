# 🔗 HardLinker v1.0.1

**Save disk space by creating hardlinks for duplicate files**

---

## 📖 Description

HardLinker finds duplicate files on your computer and uses Windows' hardlink feature to save disk space.

### ✨ Features

- 🔍 **Fast Scanning**: Finds duplicate groups by comparing files by size and hash
- 💾 **Disk Space Savings**: With hardlinks, the same data is stored only once
- 🛡️ **Safe**: Uses Windows' native hardlink feature
- 🎨 **Modern Interface**: Dark mode and smooth animations
- ⚡ **Performance**: Fast processing with multi-threading

### 🔗 What is a Hardlink?

A hardlink is a built-in Windows feature. Unlike a regular file copy, with hardlinks the same data is physically stored on disk only once, but can be accessed through multiple file names.

**An analogy:** A hardlink is like opening multiple doors to the same house. The house (data) is only one, but you can enter through different doors (file names).

### 🚀 How to Use

1. Run the program (`HardLinker.exe`)
2. Select a folder to scan
3. Click "Start Scan" button
4. Review the duplicate files found
5. Confirm with "Create Hardlinks"
6. Instantly save disk space!

### ⚠️ Important Notes

- **Administrator Rights**: Administrator rights may be required to create hardlinks
- **Same Disk**: Hardlinks only work between files on the same disk partition
- **System Files**: Be careful with system folders (program will warn you)
- **Backup**: It's recommended to back up your important files before first use

### 🛡️ Security

The hardlink operation is safe because it's a Windows native feature and there's no risk of data loss. However, make sure you have proper backups of your important data.

When you delete a hardlink, only that reference is deleted. The actual data is preserved as long as other hardlinks are in use. The data is deleted when the last hardlink is removed.

### 🔧 Technical Details

- **Language**: Python 3.11
- **GUI Framework**: CustomTkinter
- **Hash Algorithm**: SHA-256
- **Platform**: Windows 10/11

### 📊 Example Use Cases

- 📷 **Photo Backups**: Copies of the same photos in different folders
- 🎵 **Music Archive**: Duplicate song files
- 📁 **AI Model Files**: Multiple copies of the same models in different folders (eg. safetensors)
- 🎮 **Game Files**: Duplicate files from mods

### 👨‍💻 Developer

**Barış Elçi**  
📅 2025

### ☕ Support

If you find this project helpful, you can support its development:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-yellow?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/bariselcii)

### 📜 License

This software is free for personal and commercial use.

---

## 🐛 Report Issues

If you have any issues or suggestions, please contact us.

---

**🔗 HardLinker - Fast • Safe • Smart**
