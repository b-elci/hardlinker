================================================================================
                         HardLinker v1.0.1
                    Disk Space Optimizer for Windows
================================================================================

DESCRIPTION
-----------
HardLinker finds duplicate files on your computer and uses Windows' hardlink 
feature to save disk space without deleting any files.

FEATURES
--------
• Fast duplicate file detection using SHA-256 hashing
• Safe hardlink creation using Windows native features
• Modern dark-themed user interface
• Multi-threaded processing for better performance
• Automatic backup system during hardlink operations
• Protection against critical system folders

WHAT IS A HARDLINK?
-------------------
A hardlink is a built-in Windows feature where multiple file names point to 
the same physical data on disk. Unlike copies, hardlinks don't duplicate data:
- Same file appears in multiple locations
- Only one copy of data stored on disk
- Deleting one hardlink doesn't affect others
- Data deleted only when all hardlinks are removed

SYSTEM REQUIREMENTS
-------------------
• Windows 10 or Windows 11
• Administrator rights (for some operations)
• Files must be on the same disk partition

HOW TO USE
----------
1. Run HardLinker.exe
2. Click "Browse Folder" and select a folder to scan
3. Click "Start Scan" to find duplicate files
4. Review the duplicate groups found
5. Click "Create Hardlinks" to save disk space
6. Done! Check the results to see how much space you saved

IMPORTANT NOTES
---------------
⚠️ Administrator Rights: Some hardlink operations may require admin rights
⚠️ Same Disk Only: Hardlinks only work for files on the same partition
⚠️ System Files: The program will warn you about critical system folders
⚠️ Backups: Keep backups of important files before first use

SAFETY
------
HardLinker is designed with safety in mind:
• Uses Windows native hardlink feature (not a hack)
• Creates temporary backups during hardlink operations
• Protects against critical system folders
• Verifies files are on same partition before linking
• Checks inode numbers to avoid double-linking

USE CASES
---------
📷 Photo Libraries: Multiple copies of photos in different folders
🎵 Music Collections: Duplicate songs across different playlists
📁 Backup Folders: Old backups with many duplicate files
🎮 Game Mods: Duplicate mod files across installations
🤖 AI Models: Large model files (safetensors) duplicated across projects

TECHNICAL DETAILS
-----------------
Language: Python 3.11
GUI Framework: CustomTkinter
Hash Algorithm: SHA-256 for duplicate detection
Platform: Windows 10/11 (64-bit)

SUPPORT
-------
If you find this project helpful, consider supporting its development:
https://buymeacoffee.com/bariselcii

DEVELOPER
---------
Barış Elçi
GitHub: https://github.com/b-elci/hardlinker
Year: 2025

LICENSE
-------
This software is released under the MIT License.
See LICENSE.txt for full details.

Free for personal and commercial use.

================================================================================
                   HardLinker - Fast • Safe • Smart
================================================================================
