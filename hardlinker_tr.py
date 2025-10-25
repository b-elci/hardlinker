"""
HardLinker - Modern GUI ile Dosya Hardlink Yöneticisi
Windows 11 için optimize edilmiş - Ultra Animasyonlu Sürüm
"""

import os
import sys
import hashlib
import customtkinter as ctk
from pathlib import Path
from tkinter import filedialog, messagebox
from collections import defaultdict
from typing import Dict, List, Set
import threading
import time

# CustomTkinter ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Sabitler - Renkler
class Colors:
    # Primary colors - Minimal mavi tonları
    PRIMARY = ("#5aa9ff", "#4a99ef")
    PRIMARY_LIGHT = ("#6ab9ff", "#5aa9ff")
    PRIMARY_LIGHTER = ("#7ac9ff", "#6ab9ff")
    PRIMARY_HOVER = ("#4a99ef", "#3a89df")
    PRIMARY_DARK = ("#3a89df", "#2a79cf")
    
    # Secondary colors - Minimal tonlar
    BLUE = ("#5a7ca8", "#4a6c98")
    BLUE_HOVER = ("#6a8cb8", "#5a7ca8")
    BLUE_BORDER = ("#7a9cc8", "#6a8cb8")
    
    GREEN = ("#5da070", "#4d9060")
    GREEN_HOVER = ("#6db080", "#5da070")
    GREEN_BORDER = ("#7dc090", "#6db080")
    GREEN_SUCCESS = ("#4d9060", "#3d8050")
    
    RED = ("#d46a6a", "#c45a5a")
    RED_HOVER = ("#e47a7a", "#d46a6a")
    RED_BORDER = ("#f48a8a", "#e47a7a")
    RED_DARK = ("#c45a5a", "#b44a4a")
    
    # Background colors - Dark gray theme
    BG_DARK = ("#1e1e1e", "#141414")
    BG_FRAME = ("#2d2d2d", "#232323")
    BG_GLASS = ("#282828", "#1d1d1d")
    BG_PROGRESS = ("#353535", "#2a2a2a")
    
    # Text colors - Daha okunabilir
    TEXT_PRIMARY = ("#e8e8e8", "#d0d0d0")
    TEXT_GRAY = ("#c0c0c0", "#a0a0a0")
    TEXT_DARK_GRAY = ("#707070", "#505050")
    TEXT_WHITE = ("#f0f0f0", "#d8d8d8")
    
    # Special colors
    ORANGE = "#f0a860"

# Sabitler - Font
class Fonts:
    FAMILY = "Segoe UI"
    
    @staticmethod
    def get(size, weight="normal"):
        return ctk.CTkFont(family=Fonts.FAMILY, size=size, weight=weight)

# Sabitler - Boyutlar
class Sizes:
    # Pencere
    WINDOW_WIDTH = 950
    WINDOW_HEIGHT = 820
    MIN_WIDTH = 850
    MIN_HEIGHT = 750
    
    # Buton
    BUTTON_HEIGHT = 55
    BUTTON_WIDTH = 200
    BUTTON_CORNER = 15
    BUTTON_BORDER = 2
    
    # Progress bar
    PROGRESS_HEIGHT = 20
    PROGRESS_CORNER = 10
    
    # Padding
    PADDING_LARGE = 20
    PADDING_MEDIUM = 15
    PADDING_SMALL = 8

class HardLinkerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Pencere ayarları
        self.title("HardLinker - Disk Alanı Optimizasyonu")
        self.geometry(f"{Sizes.WINDOW_WIDTH}x{Sizes.WINDOW_HEIGHT}")
        self.minsize(Sizes.MIN_WIDTH, Sizes.MIN_HEIGHT)
        
        # Pencere ikonu ayarla
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "hardlinker.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass  # İkon yüklenemezse sessizce devam et
        
        # Pencereyi ekranın ortasına yerleştir (taskbar yüksekliği dahil)
        self.update_idletasks()  # Pencere boyutlarını güncelle
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        taskbar_height = 48  # Windows 11 taskbar yüksekliği
        
        # Kullanılabilir alan (taskbar hariç)
        available_height = screen_height - taskbar_height
        
        # Ortalama konumu hesapla
        x = (screen_width - Sizes.WINDOW_WIDTH) // 2
        y = (available_height - Sizes.WINDOW_HEIGHT) // 2
        
        self.geometry(f"{Sizes.WINDOW_WIDTH}x{Sizes.WINDOW_HEIGHT}+{x}+{y}")
        
        # Değişkenler
        self.selected_folder = None
        self.duplicate_groups = []
        self.total_space_saved = 0
        self.scanning = False
        self.animation_running = False
        self.cancel_requested = False
        
        # Kritik klasörler
        self.critical_folders = {
            'C:\\Windows',
            'C:\\Program Files',
            'C:\\Program Files (x86)',
            'C:\\ProgramData',
            'C:\\System Volume Information',
            os.path.expandvars('%SYSTEMROOT%'),
            os.path.expandvars('%PROGRAMFILES%'),
            os.path.expandvars('%PROGRAMFILES(X86)%')
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """UI bileşenlerini oluştur"""
        
        # Ana container - gradient efekti için
        self.main_container = ctk.CTkFrame(self, fg_color=Colors.BG_DARK)
        self.main_container.pack(fill="both", expand=True, padx=Sizes.PADDING_LARGE, pady=Sizes.PADDING_LARGE)
        
        # Başlık container - animasyonlu
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(pady=(10, 5), fill="x")
        
        # Yardım butonu - sağ üst köşe
        help_btn = ctk.CTkButton(
            header_frame,
            text="?",
            command=self.show_help,
            font=Fonts.get(16, "bold"),
            width=35,
            height=35,
            corner_radius=17,
            fg_color=Colors.BG_FRAME,
            hover_color=Colors.PRIMARY,
            text_color=Colors.TEXT_PRIMARY
        )
        help_btn.pack(side="right", padx=10)
        
        # Başlık içerik container
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack()
        
        # Başlık - gradient text efekti
        title_label = ctk.CTkLabel(
            title_container,
            text="🔗 HardLinker",
            font=Fonts.get(36, "bold"),
            text_color=Colors.PRIMARY
        )
        title_label.pack(pady=(0, 5))
        
        # Animasyonlu subtitle
        subtitle_label = ctk.CTkLabel(
            title_container,
            text="Aynı dosyaları hardlink yaparak disk alanı kazanın",
            font=Fonts.get(14, "bold"),
            text_color=Colors.TEXT_GRAY
        )
        subtitle_label.pack(pady=(0, 5))
        
        # Alt başlık
        tagline = ctk.CTkLabel(
            title_container,
            text="Hızlı • Güvenli • Akıllı",
            font=Fonts.get(11),
            text_color=Colors.TEXT_DARK_GRAY
        )
        tagline.pack(pady=(0, 20))
        
        # Ana UI bileşenlerini oluştur
        self.setup_main_ui()
        
        # Başlık animasyonu başlat - Kapatıldı
        # self.animate_title(title_label)
    
    def show_help(self):
        """Yardım penceresini göster"""
        help_window = ctk.CTkToplevel(self)
        help_window.title("🔗 HardLinker v1.0 - Developed by Barış Elçi")
        help_window.geometry("700x600")
        help_window.resizable(False, False)
        help_window.transient(self)
        help_window.grab_set()
        
        # Pencereyi ortalama
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() - 700) // 2
        y = (help_window.winfo_screenheight() - 600) // 2
        help_window.geometry(f"700x600+{x}+{y}")
        
        # İçerik container
        content_frame = ctk.CTkFrame(help_window, fg_color=Colors.BG_DARK)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Başlık
        title = ctk.CTkLabel(
            content_frame,
            text="🔗 HardLinker Hakkında",
            font=Fonts.get(28, "bold"),
            text_color=Colors.PRIMARY
        )
        title.pack(pady=(0, 20))
        
        # Açıklama metni
        help_text = ctk.CTkTextbox(
            content_frame,
            font=Fonts.get(13),
            fg_color=Colors.BG_GLASS,
            wrap="word",
            border_width=0
        )
        help_text.pack(fill="both", expand=True, pady=(0, 20))
        
        info_content = """HardLinker Nedir?

HardLinker, bilgisayarınızdaki duplicate (kopya) dosyaları bulup Windows'ın hardlink özelliğini kullanarak disk alanından tasarruf etmenizi sağlayan bir araçtır.

🔗 Hardlink Nedir?

Hardlink, Windows işletim sisteminin yerleşik bir özelliğidir. Normal bir dosya kopyasından farkı, hardlink'te aynı veri fiziksel olarak diskte sadece bir kez saklanır, ancak birden fazla dosya adı ile erişilebilir.

Bir benzetme ile: Hardlink, aynı eve birden fazla kapı açmak gibidir. Ev (veri) sadece bir tanedir, ama farklı kapılardan (dosya adlarından) girilebilir.

✨ Ne İşe Yarar?

• Disk Alanı Tasarrufu: Aynı dosyanın 10 kopyası varsa, sadece 1 tanesi yer kaplar.
• Dosya Bütünlüğü: Tüm hardlink'ler aynı veriye işaret ettiği için birini güncellediğinizde diğerleri de güncellenir.
• Güvenli: Windows'ın kendi özelliğidir, üçüncü parti bir hack değildir.

🛡️ Güvenlik

Hardlink işlemi Windows'ın native özelliği olduğu için güvenlidir ve veri kaybı riski yoktur. Ancak yine de önemli verilerinizin düzgün yedeğini aldığınızdan emin olun.

Bir hardlink'i sildiğinizde sadece o referans silinir, asIl veri diğer hardlink'ler kullanımda olduğu sürece korunur. Son hardlink silinince veri de silinir.

⚠️ Önemli Notlar

• Hardlink yalnızca aynı disk bölümündeki (partition) dosyalar arasında çalışır.
• Sistem dosyaları için kullanılmamalıdır (program zaten uyarır).
• İlk kullanımdan önce önemli dosyalarınızın yedeğini almanız tavsiye edilir.

🚀 Nasıl Çalışır?

1. Bir klasör seçin
2. Program dosyaları tarar ve aynı içeriğe sahip dosyaları bulur
3. Bulunan duplicate dosyaları görüntüleyin
4. Onayladıktan sonra hardlink işlemi yapılır
5. Disk alanından anlık tasarruf sağlanır!

👨‍💻 Geliştirici: Barış Elçi
💻 Versiyon: 1.0
📅 2025
"""
        
        help_text.insert("1.0", info_content)
        help_text.configure(state="disabled")
        
        # Kapat butonu
        close_btn = ctk.CTkButton(
            content_frame,
            text="Kapat",
            command=help_window.destroy,
            font=Fonts.get(14, "bold"),
            height=45,
            corner_radius=12,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER
        )
        close_btn.pack()
    
    def setup_main_ui(self):
        """Ana UI bileşenlerini oluştur"""
        # Klasör seçimi bölümü - gradient border
        folder_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=Colors.BG_FRAME,
            border_width=0
        )
        folder_frame.pack(fill="x", pady=(0, Sizes.PADDING_MEDIUM), padx=Sizes.PADDING_LARGE)
        
        folder_inner = ctk.CTkFrame(folder_frame, fg_color="transparent")
        folder_inner.pack(fill="x", padx=3, pady=3)
        
        self.folder_label = ctk.CTkLabel(
            folder_inner,
            text="Henüz klasör seçilmedi",
            font=Fonts.get(12, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        self.folder_label.pack(side="left", padx=Sizes.PADDING_MEDIUM, pady=12)
        
        self.browse_btn = ctk.CTkButton(
            folder_inner,
            text="📁 Klasör Seç",
            command=self.browse_folder,
            font=Fonts.get(14, "bold"),
            height=40,
            corner_radius=20,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER,
            border_width=Sizes.BUTTON_BORDER,
            border_color=Colors.TEXT_WHITE
        )
        self.browse_btn.pack(side="right", padx=Sizes.PADDING_MEDIUM, pady=12)
        
        # İlerleme bölümü - glassmorphism efekti
        progress_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=Colors.BG_GLASS,
            border_width=0
        )
        progress_frame.pack(fill="x", pady=(0, Sizes.PADDING_MEDIUM), padx=Sizes.PADDING_LARGE)
        
        # Status icon + text
        status_container = ctk.CTkFrame(progress_frame, fg_color="transparent")
        status_container.pack(pady=(Sizes.PADDING_MEDIUM, 5))
        
        self.status_icon = ctk.CTkLabel(
            status_container,
            text="⏸️",
            font=Fonts.get(18)
        )
        self.status_icon.pack(side="left", padx=(0, Sizes.PADDING_SMALL))
        
        self.status_label = ctk.CTkLabel(
            status_container,
            text="Tarama başlatılmadı",
            font=Fonts.get(12, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        self.status_label.pack(side="left")
        
        # Animasyonlu progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=Sizes.PROGRESS_HEIGHT,
            corner_radius=Sizes.PROGRESS_CORNER,
            progress_color=Colors.PRIMARY,
            fg_color=Colors.BG_PROGRESS
        )
        self.progress_bar.pack(fill="x", padx=Sizes.PADDING_LARGE, pady=(0, Sizes.PADDING_SMALL))
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="0 / 0 dosya tarandı",
            font=Fonts.get(10, "bold"),
            text_color=Colors.TEXT_GRAY
        )
        self.progress_label.pack(pady=(0, Sizes.PADDING_MEDIUM))
        
        # Butonlar - gradient ve animasyonlu
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, Sizes.PADDING_MEDIUM), padx=Sizes.PADDING_LARGE)
        
        # Butonların metinleri için sabit alanlar
        self.scan_btn = ctk.CTkButton(
            button_frame,
            text="Tarama Başlat",
            command=self.start_scan,
            font=Fonts.get(14, "bold"),
            height=Sizes.BUTTON_HEIGHT,
            width=Sizes.BUTTON_WIDTH,
            corner_radius=Sizes.BUTTON_CORNER,
            state="disabled",
            fg_color=Colors.BLUE,
            hover_color=Colors.BLUE_HOVER,
            border_width=Sizes.BUTTON_BORDER,
            border_color=Colors.BLUE_BORDER
        )
        self.scan_btn.pack(side="left", expand=True, fill="x", padx=(0, Sizes.PADDING_SMALL))
        
        self.cancel_btn = ctk.CTkButton(
            button_frame,
            text="Durdur",
            command=self.cancel_scan,
            font=Fonts.get(14, "bold"),
            height=Sizes.BUTTON_HEIGHT,
            width=Sizes.BUTTON_WIDTH,
            corner_radius=Sizes.BUTTON_CORNER,
            state="disabled",
            fg_color=Colors.RED,
            hover_color=Colors.RED_HOVER,
            border_width=Sizes.BUTTON_BORDER,
            border_color=Colors.RED_BORDER
        )
        self.cancel_btn.pack(side="left", expand=True, fill="x", padx=(Sizes.PADDING_SMALL, Sizes.PADDING_SMALL))
        
        self.hardlink_btn = ctk.CTkButton(
            button_frame,
            text="Hardlink Yap",
            command=self.show_hardlink_preview,
            font=Fonts.get(14, "bold"),
            height=Sizes.BUTTON_HEIGHT,
            width=Sizes.BUTTON_WIDTH,
            corner_radius=Sizes.BUTTON_CORNER,
            state="disabled",
            fg_color=Colors.GREEN,
            hover_color=Colors.GREEN_HOVER,
            border_width=Sizes.BUTTON_BORDER,
            border_color=Colors.GREEN_BORDER
        )
        self.hardlink_btn.pack(side="right", expand=True, fill="x", padx=(Sizes.PADDING_SMALL, 0))
        
        # Sonuçlar bölümü - gradient header
        results_header = ctk.CTkFrame(
            self.main_container,
            fg_color=Colors.BG_FRAME,
            height=40,
            corner_radius=10
        )
        results_header.pack(fill="x", pady=(0, Sizes.PADDING_SMALL), padx=Sizes.PADDING_LARGE)
        
        results_label = ctk.CTkLabel(
            results_header,
            text="Tarama Sonuçları",
            font=Fonts.get(16, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        results_label.pack(pady=Sizes.PADDING_SMALL, padx=Sizes.PADDING_MEDIUM, anchor="w")
        
        # Sonuçlar text box - glassmorphism
        self.results_textbox = ctk.CTkTextbox(
            self.main_container,
            font=Fonts.get(12),
            corner_radius=12,
            border_width=0,
            fg_color=Colors.BG_GLASS
        )
        self.results_textbox.pack(fill="both", expand=True, padx=Sizes.PADDING_LARGE)
        self.results_textbox.insert("1.0", "Tarama sonuçları burada görünecek...\n\nKlasör seçip taramayı başlatın!\n")
        self.results_textbox.configure(state="disabled")
        
        # İstatistikler (alt) - gradient ve animasyonlu
        stats_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=Colors.BG_FRAME,
            border_width=0,
            corner_radius=12
        )
        stats_frame.pack(fill="x", pady=(Sizes.PADDING_MEDIUM, Sizes.PADDING_LARGE), padx=Sizes.PADDING_LARGE)
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Kazanılabilecek Alan: 0 MB | Duplicate Grup: 0 | Toplam Dosya: 0",
            font=Fonts.get(11, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        self.stats_label.pack(pady=12)
        
        # Stats animasyonu başlat - Kapatıldı
        # self.animate_stats_border(stats_frame)
    
    def animate_title(self, label):
        """Başlık için pulse animasyonu"""
        colors = [Colors.PRIMARY, Colors.PRIMARY_LIGHT, Colors.PRIMARY_LIGHTER]
        
        def pulse(idx=0):
            if hasattr(self, 'main_container'):
                label.configure(text_color=colors[idx % len(colors)])
                self.after(1000, lambda: pulse((idx + 1) % len(colors)))
        
        pulse()
    
    def animate_stats_border(self, frame):
        """Stats frame için border pulse animasyonu"""
        colors = [Colors.PRIMARY, Colors.PRIMARY_HOVER, Colors.PRIMARY_DARK]
        
        def pulse(idx=0):
            if hasattr(self, 'main_container'):
                frame.configure(border_color=colors[idx % len(colors)])
                self.after(1500, lambda: pulse((idx + 1) % len(colors)))
        
        pulse()
    
    def browse_folder(self):
        """Klasör seçme dialog"""
        folder = filedialog.askdirectory(title="Taranacak Klasörü Seçin")
        if folder:
            self.selected_folder = folder
            self.folder_label.configure(text=f"{folder}")
            self.scan_btn.configure(state="normal")
            self.hardlink_btn.configure(state="disabled")
            self.duplicate_groups = []
            
            # Folder seçildiğinde animasyon - Kapatıldı
            # self.flash_folder_label()
            
            # Kritik klasör kontrolü
            if self.is_critical_folder(folder):
                self.show_critical_warning(folder)
    
    def flash_folder_label(self):
        """Klasör seçildiğinde yanıp sönen efekt"""
        colors = [Colors.GREEN_SUCCESS, Colors.PRIMARY]
        
        def flash(idx=0, count=0):
            if count < 4 and hasattr(self, 'folder_label'):
                self.folder_label.configure(text_color=colors[idx % 2])
                self.after(200, lambda: flash((idx + 1) % 2, count + 1))
            elif hasattr(self, 'folder_label'):
                self.folder_label.configure(text_color=Colors.PRIMARY)
        
        flash()
    
    def is_critical_folder(self, folder):
        """Kritik klasör kontrolü"""
        folder_path = Path(folder).resolve()
        for critical in self.critical_folders:
            critical_path = Path(critical).resolve()
            try:
                if folder_path == critical_path or folder_path.is_relative_to(critical_path):
                    return True
            except (ValueError, AttributeError):
                # is_relative_to Python 3.9+ için
                if str(folder_path).lower().startswith(str(critical_path).lower()):
                    return True
        return False
    
    def show_critical_warning(self, folder):
        """Kritik klasör uyarısı"""
        warning_window = ctk.CTkToplevel(self)
        warning_window.title("KRİTİK KLASÖR UYARISI")
        warning_window.geometry("500x300")
        warning_window.transient(self)
        warning_window.grab_set()
        
        # Uyarı ikonu ve mesaj
        warning_label = ctk.CTkLabel(
            warning_window,
            text="⚠️",
            font=Fonts.get(64)
        )
        warning_label.pack(pady=(Sizes.PADDING_LARGE, 10))
        
        title_label = ctk.CTkLabel(
            warning_window,
            text="KRİTİK SİSTEM KLASÖRÜ",
            font=Fonts.get(20, "bold"),
            text_color=Colors.ORANGE
        )
        title_label.pack(pady=(0, 10))
        
        message_label = ctk.CTkLabel(
            warning_window,
            text=f"Seçtiğiniz klasör sistem klasörüdür:\n\n{folder}\n\n"
                 "Bu klasörde hardlink işlemi yapmak sisteminize\n"
                 "zarar verebilir. Devam etmek istediğinize emin misiniz?",
            font=Fonts.get(13),
            justify="center"
        )
        message_label.pack(pady=(0, 20))
        
        # Butonlar
        button_frame = ctk.CTkFrame(warning_window, fg_color="transparent")
        button_frame.pack(pady=(0, 20))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="İptal Et",
            command=lambda: [warning_window.destroy(), self.reset_folder()],
            width=150,
            fg_color="#d32f2f",
            hover_color="#b71c1c"
        )
        cancel_btn.pack(side="left", padx=5)
        
        continue_btn = ctk.CTkButton(
            button_frame,
            text="Yine de Devam Et",
            command=warning_window.destroy,
            width=150
        )
        continue_btn.pack(side="right", padx=5)
    
    def reset_folder(self):
        """Klasör seçimini sıfırla"""
        self.selected_folder = None
        self.folder_label.configure(
            text="Henüz klasör seçilmedi",
            text_color=Colors.TEXT_PRIMARY
        )
        self.scan_btn.configure(state="disabled")
    
    def start_scan(self):
        """Taramayı başlat"""
        if not self.selected_folder or self.scanning:
            return
        
        self.scanning = True
        self.cancel_requested = False
        self.scan_btn.configure(state="disabled", text="⏳ Taranıyor")
        self.cancel_btn.configure(state="normal")
        self.hardlink_btn.configure(state="disabled")
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("1.0", "Tarama başlatılıyor...\n\nDosyalar toplanıyor...\n")
        self.results_textbox.configure(state="disabled")
        
        # Status icon animasyonu - Kapatıldı
        # self.animate_status_icon()
        
        # Thread'de tara
        scan_thread = threading.Thread(target=self.scan_folder, daemon=True)
        scan_thread.start()
    
    def cancel_scan(self):
        """Taramayı iptal et"""
        if self.scanning:
            self.cancel_requested = True
            self.update_status("⏹️ Tarama iptal ediliyor...")
            self.update_status_icon("⏹️")
            self.cancel_btn.configure(state="disabled", text="⏹️ İptal...")
            
            # İptal animasyonu - Kapatıldı
            # self.flash_cancel_button()
    
    def scan_folder(self):
        """Klasörü tara ve duplicate dosyaları bul"""
        try:
            # Dosya toplama
            self.update_status("Dosyalar toplanıyor...")
            self.update_status_icon("🔍")
            all_files = []
            
            for root, dirs, files in os.walk(self.selected_folder):
                if self.cancel_requested:
                    self.handle_scan_cancelled()
                    return
                
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        if os.path.isfile(filepath):
                            all_files.append(filepath)
                    except (PermissionError, OSError):
                        continue
            
            total_files = len(all_files)
            self.update_progress_label(0, total_files)
            
            # Boyuta göre gruplama
            self.update_status("Dosyalar boyutuna göre gruplandırılıyor...")
            self.update_status_icon("📦")
            size_groups = defaultdict(list)
            
            for idx, filepath in enumerate(all_files):
                if self.cancel_requested:
                    self.handle_scan_cancelled()
                    return
                
                try:
                    size = os.path.getsize(filepath)
                    if size > 0:  # Boş dosyaları atla
                        size_groups[size].append(filepath)
                    
                    if idx % 100 == 0:
                        progress = (idx + 1) / total_files
                        self.progress_bar.set(progress)
                        self.update_progress_label(idx + 1, total_files)
                except (PermissionError, OSError):
                    continue
            
            # Hash karşılaştırması
            self.update_status("Duplicate dosyalar hash ile kontrol ediliyor...")
            self.update_status_icon("🔐")
            self.duplicate_groups = []
            hash_groups = defaultdict(list)
            
            checked_files = 0
            files_to_check = [f for files in size_groups.values() if len(files) > 1 for f in files]
            total_to_check = len(files_to_check)
            
            for size, file_list in size_groups.items():
                if self.cancel_requested:
                    self.handle_scan_cancelled()
                    return
                
                if len(file_list) > 1:
                    # Aynı boyuttaki dosyaların hash'ini al
                    for filepath in file_list:
                        if self.cancel_requested:
                            self.handle_scan_cancelled()
                            return
                        
                        try:
                            file_hash = self.calculate_hash(filepath)
                            hash_groups[file_hash].append(filepath)
                            
                            checked_files += 1
                            if checked_files % 50 == 0:
                                progress = checked_files / max(total_to_check, 1)
                                self.progress_bar.set(progress)
                                self.update_progress_label(checked_files, total_to_check)
                        except (PermissionError, OSError, Exception):
                            continue
            
            # Duplicate grupları filtrele
            for file_hash, file_list in hash_groups.items():
                if len(file_list) > 1:
                    # Hardlink olmayanları kontrol et
                    inodes = {}
                    for filepath in file_list:
                        try:
                            stat = os.stat(filepath)
                            inode = (stat.st_dev, stat.st_ino)
                            if inode not in inodes:
                                inodes[inode] = []
                            inodes[inode].append(filepath)
                        except (OSError, Exception):
                            continue
                    
                    # Birden fazla farklı inode varsa duplicate
                    if len(inodes) > 1:
                        # Her inode grubundan bir dosya al
                        unique_files = [files[0] for files in inodes.values()]
                        if len(unique_files) > 1:
                            self.duplicate_groups.append(unique_files)
            
            # Sonuçları göster (GUI thread'inde çalıştır)
            self.after(0, self.show_results)
            
        except Exception as e:
            self.update_status(f"❌ Hata: {str(e)}")
            self.update_status_icon("❌")
        finally:
            self.scanning = False
            self.cancel_requested = False
            self.scan_btn.configure(state="normal", text="🔍 Tarama Başlat")
            self.cancel_btn.configure(state="disabled", text="⛔ Durdur")
            self.update_status_icon("✅")
            if self.duplicate_groups:
                self.hardlink_btn.configure(state="normal")
                # Başarı animasyonu - Kapatıldı
                # self.flash_success()
    
    def handle_scan_cancelled(self):
        """Tarama iptal edildiğinde temizlik yap"""
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("1.0", 
            "⛔ Tarama İptal Edildi\n\n"
            "Tarama kullanıcı tarafından durduruldu.\n"
            "Kısmi sonuçlar gösterilmeyecek.\n"
        )
        self.results_textbox.configure(state="disabled")
        self.update_status("⛔ Tarama iptal edildi")
        self.update_status_icon("⛔")
        self.progress_bar.set(0)
        self.duplicate_groups = []
    
    def flash_cancel_button(self):
        """İptal butonu için yanıp sönen efekt"""
        def flash(count=0):
            if count < 4 and hasattr(self, 'cancel_btn'):
                if count % 2 == 0:
                    self.cancel_btn.configure(border_color=Colors.RED_DARK)
                else:
                    self.cancel_btn.configure(border_color=Colors.RED_BORDER)
                self.after(150, lambda: flash(count + 1))
            elif hasattr(self, 'cancel_btn'):
                self.cancel_btn.configure(border_color=Colors.RED_BORDER)
        
        flash()
    
    def calculate_hash(self, filepath, chunk_size=8192):
        """Dosyanın SHA256 hash'ini hesapla"""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def show_results(self):
        """Tarama sonuçlarını göster"""
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        
        if not self.duplicate_groups:
            self.results_textbox.insert("1.0", 
                "Tarama tamamlandı!\n\n"
                "Duplicate dosya bulunamadı. Tüm dosyalarınız benzersiz.\n"
            )
            self.total_space_saved = 0
        else:
            # Toplam alanı hesapla
            self.total_space_saved = 0
            total_files_to_link = 0
            
            for group in self.duplicate_groups:
                try:
                    size = os.path.getsize(group[0])
                    space_saved = size * (len(group) - 1)
                    self.total_space_saved += space_saved
                    total_files_to_link += len(group) - 1
                except (OSError, Exception):
                    continue
            
            # Sadece bir kez özet bilgi
            summary_text = (
                f"Tarama Tamamlandı!\n\n"
                f"📊 Özet:\n"
                f"  • {len(self.duplicate_groups)} grup duplicate dosya bulundu\n"
                f"  • {total_files_to_link} dosya hardlink yapılacak\n"
                f"  • {self.format_size(self.total_space_saved)} disk alanı kazanılacak\n\n"
                f"{'─' * 70}\n\n"
            )
            self.results_textbox.insert("1.0", summary_text)
            
            # Grup detayları
            for idx, group in enumerate(self.duplicate_groups[:50], 1):  # İlk 50 grup
                try:
                    size = os.path.getsize(group[0])
                    space_saved = size * (len(group) - 1)
                    
                    group_text = (
                        f"📦 Grup {idx}:  "
                        f"Boyut: {self.format_size(size)}  |  "
                        f"Kopya: {len(group)}  |  "
                        f"Kazanç: {self.format_size(space_saved)}\n"
                    )
                    self.results_textbox.insert("end", group_text)
                    
                    for filepath in group[:3]:  # İlk 3 dosya
                        self.results_textbox.insert("end", f"   📄 {filepath}\n")
                    
                    if len(group) > 3:
                        self.results_textbox.insert("end", f"   ... ve {len(group) - 3} dosya daha\n")
                    
                    self.results_textbox.insert("end", "\n")
                    
                except (OSError, Exception):
                    continue
            
            if len(self.duplicate_groups) > 50:
                remaining_groups = len(self.duplicate_groups) - 50
                self.results_textbox.insert("end", 
                    f"💡 ... ve {remaining_groups} grup daha (toplam {len(self.duplicate_groups)} grup)\n"
                )
        
        self.results_textbox.configure(state="disabled")
        self.update_stats()
        self.update_status("Tarama tamamlandı!")
        self.update_status_icon("✅")
        self.progress_bar.set(1.0)
        
        # Progress bar için renk animasyonu
        self.animate_progress_success()
    
    def show_hardlink_preview(self):
        """Hardlink yapılacak dosyaları önizle ve onay al"""
        if not self.duplicate_groups:
            return
        
        preview_window = ctk.CTkToplevel(self)
        preview_window.title("Hardlink Önizleme ve Onay")
        preview_window.geometry("850x650")
        preview_window.transient(self)
        preview_window.grab_set()
        
        # Başlık
        title_label = ctk.CTkLabel(
            preview_window,
            text="Hardlink İşlemi Onayı",
            font=Fonts.get(22, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        title_label.pack(pady=Sizes.PADDING_LARGE)
        
        # Özet bilgi - daha kompakt
        total_files = sum(len(group) - 1 for group in self.duplicate_groups)
        info_label = ctk.CTkLabel(
            preview_window,
            text=f"📊 {len(self.duplicate_groups)} grup | {total_files} dosya | {self.format_size(self.total_space_saved)} kazanılacak",
            font=Fonts.get(13, "bold"),
            text_color=Colors.PRIMARY
        )
        info_label.pack(pady=(0, Sizes.PADDING_MEDIUM))
        
        # Detaylar
        details_frame = ctk.CTkFrame(preview_window)
        details_frame.pack(fill="both", expand=True, padx=Sizes.PADDING_LARGE, pady=(0, Sizes.PADDING_LARGE))
        
        details_textbox = ctk.CTkTextbox(details_frame, font=Fonts.get(11))
        details_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        details_textbox.insert("1.0", 
            f"📋 Hardlink Yapılacak Dosyalar:\n\n"
        )
        
        for idx, group in enumerate(self.duplicate_groups[:30], 1):
            try:
                size = os.path.getsize(group[0])
                space_saved = size * (len(group) - 1)
                details_textbox.insert("end", 
                    f"📦 Grup {idx}:  "
                    f"{len(group)} dosya  |  "
                    f"Boyut: {self.format_size(size)}  |  "
                    f"Kazanç: {self.format_size(space_saved)}\n"
                )
                details_textbox.insert("end", f"   ✓ Ana: {group[0]}\n")
                details_textbox.insert("end", f"   → Hardlink yapılacak:\n")
                for filepath in group[1:3]:
                    details_textbox.insert("end", f"      {filepath}\n")
                if len(group) > 3:
                    details_textbox.insert("end", f"      ... ve {len(group) - 3} dosya daha\n")
                details_textbox.insert("end", "\n")
            except (OSError, Exception):
                continue
        
        if len(self.duplicate_groups) > 30:
            details_textbox.insert("end", f"💡 ... ve {len(self.duplicate_groups) - 30} grup daha\n")
        
        details_textbox.configure(state="disabled")
        
        # Uyarı
        warning_label = ctk.CTkLabel(
            preview_window,
            text="Bu işlem geri alınamaz! Devam etmek istediğinize emin misiniz?",
            font=Fonts.get(11, "bold"),
            text_color=Colors.ORANGE
        )
        warning_label.pack(pady=(0, 10))
        
        # Butonlar - daha geniş ve görünür
        button_frame = ctk.CTkFrame(preview_window, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, Sizes.PADDING_LARGE), padx=40)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Vazgeç",
            command=preview_window.destroy,
            font=Fonts.get(14, "bold"),
            height=50,
            width=180,
            corner_radius=12,
            fg_color=Colors.RED,
            hover_color=Colors.RED_HOVER,
            border_width=Sizes.BUTTON_BORDER,
            border_color=Colors.RED_BORDER
        )
        cancel_btn.pack(side="left", expand=True, padx=(0, 10))
        
        confirm_btn = ctk.CTkButton(
            button_frame,
            text="Onayla",
            command=lambda: [preview_window.destroy(), self.perform_hardlink()],
            font=Fonts.get(14, "bold"),
            height=50,
            width=180,
            corner_radius=12,
            fg_color=Colors.GREEN,
            hover_color=Colors.GREEN_HOVER,
            border_width=Sizes.BUTTON_BORDER,
            border_color=Colors.GREEN_BORDER
        )
        confirm_btn.pack(side="right", expand=True, padx=(10, 0))
    
    def perform_hardlink(self):
        """Hardlink işlemini gerçekleştir"""
        self.cancel_requested = False
        self.hardlink_btn.configure(state="disabled", text="⏳ İşleniyor")
        self.scan_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal", text="⛔ Durdur")
        
        # Thread'de çalıştır
        hardlink_thread = threading.Thread(target=self.do_hardlink, daemon=True)
        hardlink_thread.start()
    
    def do_hardlink(self):
        """Hardlink işlemini yap"""
        success_count = 0
        fail_count = 0
        total_saved = 0
        total_groups = len(self.duplicate_groups)
        
        self.update_status("⚡ Hardlink işlemi başlatıldı...")
        
        for idx, group in enumerate(self.duplicate_groups):
            if self.cancel_requested:
                self.update_status("⛔ Hardlink işlemi iptal edildi!")
                self.show_completion_message(success_count, fail_count, total_saved, cancelled=True)
                break
            
            try:
                # İlk dosyayı master olarak tut
                master_file = group[0]
                
                # Diğerlerini hardlink yap
                for duplicate_file in group[1:]:
                    if self.cancel_requested:
                        break
                    
                    try:
                        # Backup adı
                        backup_file = duplicate_file + ".backup_temp"
                        
                        # Dosyayı yedekle
                        os.rename(duplicate_file, backup_file)
                        
                        # Hardlink oluştur
                        os.link(master_file, duplicate_file)
                        
                        # Backup'ı sil
                        os.remove(backup_file)
                        
                        size = os.path.getsize(master_file)
                        total_saved += size
                        success_count += 1
                        
                    except Exception as e:
                        fail_count += 1
                        # Hata olursa backup'tan geri yükle
                        try:
                            if os.path.exists(backup_file):
                                if os.path.exists(duplicate_file):
                                    os.remove(duplicate_file)
                                os.rename(backup_file, duplicate_file)
                        except:
                            pass
                
                # İlerlemeyi güncelle
                progress = (idx + 1) / total_groups
                self.progress_bar.set(progress)
                self.update_status(f"⚡ İşleniyor: {idx + 1}/{total_groups} grup")
                
            except Exception as e:
                fail_count += 1
                continue
        
        # Sonuç mesajı (iptal edilmediyse)
        if not self.cancel_requested:
            self.show_completion_message(success_count, fail_count, total_saved)
        
        # UI'ı güncelle
        self.hardlink_btn.configure(state="disabled", text="⚡ Hardlink")
        self.scan_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled", text="⛔ Durdur")
        
        if not self.cancel_requested:
            self.update_status("İşlem tamamlandı!")
            self.progress_bar.set(1.0)
        else:
            self.update_status("⛔ İşlem iptal edildi!")
            self.progress_bar.set(0)
    
    def show_completion_message(self, success, fail, saved, cancelled=False):
        """Tamamlanma mesajı göster"""
        if cancelled:
            message = (
                f"⛔ Hardlink İşlemi İptal Edildi\n\n"
                f"İşlem kullanıcı tarafından durduruldu.\n\n"
                f"Başarılı: {success} dosya\n"
                f"Başarısız: {fail} dosya\n"
                f"Kazanılan Alan: {self.format_size(saved)}\n\n"
                f"Not: İşlem tamamlanmadı."
            )
            self.after(0, lambda: messagebox.showwarning("İşlem İptal Edildi", message))
        else:
            message = (
                f"Hardlink İşlemi Tamamlandı!\n\n"
                f"Başarılı: {success} dosya\n"
                f"Başarısız: {fail} dosya\n"
                f"Kazanılan Alan: {self.format_size(saved)}\n"
            )
            self.after(0, lambda: messagebox.showinfo("İşlem Tamamlandı", message))
    
    def animate_status_icon(self):
        """Status icon için dönen animasyon"""
        icons = ["🔄", "🔃", "🔄", "🔃"]
        
        def rotate(idx=0):
            if self.scanning and hasattr(self, 'status_icon'):
                self.status_icon.configure(text=icons[idx % len(icons)])
                self.after(300, lambda: rotate((idx + 1) % len(icons)))
        
        rotate()
    
    def update_status(self, text):
        """Durum mesajını güncelle"""
        self.after(0, lambda: self.status_label.configure(text=text))
    
    def update_status_icon(self, icon):
        """Status iconunu güncelle"""
        self.after(0, lambda: self.status_icon.configure(text=icon))
    
    def flash_success(self):
        """Başarı için yanıp sönen efekt"""
        def flash(count=0):
            if count < 6 and hasattr(self, 'hardlink_btn'):
                if count % 2 == 0:
                    self.hardlink_btn.configure(border_color=Colors.GREEN_SUCCESS)
                else:
                    self.hardlink_btn.configure(border_color=Colors.GREEN_BORDER)
                self.after(200, lambda: flash(count + 1))
        
        flash()
    
    def update_progress_label(self, current, total):
        """İlerleme etiketini güncelle"""
        self.after(0, lambda: self.progress_label.configure(
            text=f"📊 {current:,} / {total:,} dosya tarandı"
        ))
    
    def animate_progress_success(self):
        """Progress bar başarı animasyonu"""
        colors = [Colors.GREEN_SUCCESS, Colors.PRIMARY]
        
        def pulse(idx=0, count=0):
            if count < 6 and hasattr(self, 'progress_bar'):
                self.progress_bar.configure(progress_color=colors[idx % 2])
                self.after(200, lambda: pulse((idx + 1) % 2, count + 1))
            elif hasattr(self, 'progress_bar'):
                self.progress_bar.configure(progress_color=Colors.PRIMARY)
        
        pulse()
    
    def update_stats(self):
        """İstatistikleri güncelle"""
        total_files = sum(len(group) for group in self.duplicate_groups)
        stats_text = (
            f"💾 Kazanılabilecek Alan: {self.format_size(self.total_space_saved)} | "
            f"📁 Duplicate Grup: {len(self.duplicate_groups)} | "
            f"📄 Toplam Dosya: {total_files}"
        )
        self.stats_label.configure(text=stats_text)
        
        # Stats güncellendiğinde pulse efekti - Kapatıldı
        # if total_files > 0:
        #     self.pulse_stats()
    
    def pulse_stats(self):
        """Stats için büyüme animasyonu"""
        original_font = Fonts.get(11, "bold")
        large_font = Fonts.get(12, "bold")
        
        def grow():
            if hasattr(self, 'stats_label'):
                self.stats_label.configure(font=large_font)
                self.after(200, shrink)
        
        def shrink():
            if hasattr(self, 'stats_label'):
                self.stats_label.configure(font=original_font)
        
        grow()
    
    def format_size(self, bytes_size):
        """Byte'ı okunabilir formata çevir"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"


def main():
    """Uygulamayı başlat"""
    # Admin kontrolü
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            messagebox.showwarning(
                "Yönetici Yetkisi",
                "Hardlink oluşturmak için yönetici yetkisi gerekebilir.\n"
                "Eğer işlem başarısız olursa, programı yönetici olarak çalıştırın."
            )
    except:
        pass
    
    app = HardLinkerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
