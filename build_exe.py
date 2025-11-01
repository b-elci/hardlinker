"""
HardLinker - PyInstaller Build Script
Programı tek bir .exe dosyasına paketler
"""

import PyInstaller.__main__
import os

# Build klasörünü temizle
if os.path.exists('build'):
    import shutil
    shutil.rmtree('build')

if os.path.exists('dist'):
    import shutil
    shutil.rmtree('dist')

# PyInstaller ile paketleme
PyInstaller.__main__.run([
    'hardlinker.py',
    '--name=HardLinker',
    '--onefile',
    '--windowed',
    '--icon=hardlinker.ico',
    '--add-data=hardlinker.ico;.',
    '--noconsole',
    '--clean',
    '--noconfirm',
    # Hidden imports for CustomTkinter
    '--hidden-import=customtkinter',
    '--hidden-import=darkdetect',
    '--hidden-import=tkinter',
    '--hidden-import=_tkinter',
    '--hidden-import=PIL',
    '--hidden-import=PIL._tkinter_finder',
    '--collect-all=customtkinter',
    '--collect-all=darkdetect',
    # Optimizasyonlar
    '--optimize=2',
    # Gereksiz modülleri hariç tut
    '--exclude-module=matplotlib',
    '--exclude-module=numpy',
    '--exclude-module=pandas',
    '--exclude-module=scipy',
    '--exclude-module=pytest',
    # Metadata
    '--version-file=version_info.txt',
])

print("\n" + "="*70)
print("✅ BUILD TAMAMLANDI!")
print("="*70)
print(f"\n📦 Çıktı dosyası: dist\\HardLinker.exe")
print(f"📊 Dosya boyutu: {os.path.getsize('dist/HardLinker.exe') / (1024*1024):.2f} MB")
print("\n💡 Programı test etmek için: dist\\HardLinker.exe")
print("="*70)
