"""
HardLinker - File Hardlink Manager with Modern GUI
Optimized for Windows 11 - English Version
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
import webbrowser
import settings

# CustomTkinter settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Constants - Colors
class Colors:
    # Primary colors
    PRIMARY = ("#5aa9ff", "#4a99ef")
    PRIMARY_LIGHT = ("#6ab9ff", "#5aa9ff")
    PRIMARY_LIGHTER = ("#7ac9ff", "#6ab9ff")
    PRIMARY_HOVER = ("#4a99ef", "#3a89df")
    PRIMARY_DARK = ("#3a89df", "#2a79cf")
    
    # Secondary colors
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
    
    # Background colors
    BG_DARK = ("#1e1e1e", "#141414")
    BG_FRAME = ("#2d2d2d", "#232323")
    BG_GLASS = ("#282828", "#1d1d1d")
    BG_PROGRESS = ("#353535", "#2a2a2a")
    
    # Text colors
    TEXT_PRIMARY = ("#e8e8e8", "#d0d0d0")
    TEXT_GRAY = ("#c0c0c0", "#a0a0a0")
    TEXT_DARK_GRAY = ("#707070", "#505050")
    TEXT_WHITE = ("#f0f0f0", "#d8d8d8")
    
    # Special colors
    ORANGE = "#f0a860"

# Constants - Font
class Fonts:
    FAMILY = "Segoe UI"
    
    @staticmethod
    def get(size, weight="normal"):
        return ctk.CTkFont(family=Fonts.FAMILY, size=size, weight=weight)

# Constants - Sizes
class Sizes:
    # Window
    WINDOW_WIDTH = 950
    WINDOW_HEIGHT = 820
    MIN_WIDTH = 850
    MIN_HEIGHT = 750
    
    # Button
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
        
        # Window settings
        self.title("HardLinker - Disk Space Optimizer")
        self.geometry(f"{Sizes.WINDOW_WIDTH}x{Sizes.WINDOW_HEIGHT}")
        self.minsize(Sizes.MIN_WIDTH, Sizes.MIN_HEIGHT)
        
        # Set window icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "hardlinker.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass
        
        # Center window on screen (including taskbar height)
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        taskbar_height = 48  # Windows 11 taskbar height
        
        # Available area (excluding taskbar)
        available_height = screen_height - taskbar_height
        
        # Calculate center position
        x = (screen_width - Sizes.WINDOW_WIDTH) // 2
        y = (available_height - Sizes.WINDOW_HEIGHT) // 2
        
        self.geometry(f"{Sizes.WINDOW_WIDTH}x{Sizes.WINDOW_HEIGHT}+{x}+{y}")
        
        # Variables
        self.selected_folder = None
        self.duplicate_groups = []
        self.total_space_saved = 0
        self.scanning = False
        self.animation_running = False
        self.cancel_requested = False
        
        # Critical folders
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
        
        # Show welcome dialog if not disabled
        if settings.should_show_welcome():
            self.after(500, self.show_welcome_dialog)
        
    def show_welcome_dialog(self):
        """Show welcome dialog on first run"""
        welcome_window = ctk.CTkToplevel(self)
        welcome_window.title("Welcome to HardLinker")
        welcome_window.geometry("600x550")
        welcome_window.resizable(False, False)
        welcome_window.transient(self)
        welcome_window.grab_set()
        
        # Center window
        welcome_window.update_idletasks()
        x = (welcome_window.winfo_screenwidth() - 600) // 2
        y = (welcome_window.winfo_screenheight() - 550) // 2
        welcome_window.geometry(f"600x550+{x}+{y}")
        
        # Content frame
        content_frame = ctk.CTkFrame(welcome_window, fg_color=Colors.BG_DARK)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title = ctk.CTkLabel(
            content_frame,
            text="🔗 Welcome to HardLinker!",
            font=Fonts.get(28, "bold"),
            text_color=Colors.PRIMARY
        )
        title.pack(pady=(0, 20))
        
        # Welcome text
        welcome_text = ctk.CTkTextbox(
            content_frame,
            font=Fonts.get(13),
            fg_color=Colors.BG_GLASS,
            wrap="word",
            border_width=0
        )
        welcome_text.pack(fill="both", expand=True, pady=(0, 20))
        
        info_content = """What is HardLinker?

HardLinker finds duplicate files on your computer and uses Windows' hardlink feature to save disk space.

🔗 What is a Hardlink?

A hardlink is a built-in Windows feature. Unlike a regular file copy, with hardlinks the same data is physically stored on disk only once, but can be accessed through multiple file names.

Think of it like this: A hardlink is like opening multiple doors to the same house. The house (data) is only one, but you can enter through different doors (file names).

✨ Benefits

• Disk Space Savings: If you have 10 copies of the same file, only 1 takes up space.
• File Integrity: Since all hardlinks point to the same data, updating one updates all.
• Safe: It's a Windows native feature, not a third-party hack.

⚠️ Important Notes

• Hardlinks only work between files on the same disk partition.
• Should not be used for system files (program will warn you).
• Back up your important files before first use.

🚀 How to Use

1. Select a folder to scan
2. Click "Start Scan"
3. Review the duplicate files found
4. Confirm and click "Create Hardlinks"
5. Instantly save disk space!

👨‍💻 Developer: Barış Elçi
💻 Version: 1.0.1
📅 2025
"""
        
        welcome_text.insert("1.0", info_content)
        welcome_text.configure(state="disabled")
        
        # Don't show again checkbox
        show_again_var = ctk.BooleanVar(value=False)
        
        checkbox_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        checkbox_frame.pack(pady=(0, 15))
        
        checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="Don't show this again",
            variable=show_again_var,
            font=Fonts.get(12),
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER
        )
        checkbox.pack()
        
        # OK button
        def on_ok():
            if show_again_var.get():
                settings.set_show_welcome(False)
            welcome_window.destroy()
        
        ok_btn = ctk.CTkButton(
            content_frame,
            text="Get Started",
            command=on_ok,
            font=Fonts.get(14, "bold"),
            height=45,
            width=200,
            corner_radius=12,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER
        )
        ok_btn.pack()
        
    def setup_ui(self):
        """Create UI components"""
        
        # Main container
        self.main_container = ctk.CTkFrame(self, fg_color=Colors.BG_DARK)
        self.main_container.pack(fill="both", expand=True, padx=Sizes.PADDING_LARGE, pady=Sizes.PADDING_LARGE)
        
        # Header container
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(pady=(10, 5), fill="x")
        
        # Help button - top right corner
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
        
        # Buy Me a Coffee button - next to help button
        coffee_btn = ctk.CTkButton(
            header_frame,
            text="☕",
            command=self.open_coffee_link,
            font=Fonts.get(16, "bold"),
            width=35,
            height=35,
            corner_radius=17,
            fg_color=Colors.ORANGE,
            hover_color="#e09850",
            text_color=Colors.TEXT_WHITE
        )
        coffee_btn.pack(side="right", padx=(10, 0))
        
        # Title content container
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack()
        
        # Title
        title_label = ctk.CTkLabel(
            title_container,
            text="🔗 HardLinker",
            font=Fonts.get(36, "bold"),
            text_color=Colors.PRIMARY
        )
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            title_container,
            text="Save disk space by creating hardlinks for duplicate files",
            font=Fonts.get(14, "bold"),
            text_color=Colors.TEXT_GRAY
        )
        subtitle_label.pack(pady=(0, 5))
        
        # Tagline
        tagline = ctk.CTkLabel(
            title_container,
            text="Fast • Safe • Smart",
            font=Fonts.get(11),
            text_color=Colors.TEXT_DARK_GRAY
        )
        tagline.pack(pady=(0, 20))
        
        # Create main UI components
        self.setup_main_ui()
    
    def open_coffee_link(self):
        """Open Buy Me a Coffee link in browser"""
        webbrowser.open("https://buymeacoffee.com/bariselcii")
    
    def show_help(self):
        """Show help window"""
        help_window = ctk.CTkToplevel(self)
        help_window.title("🔗 HardLinker v1.0.1 - Developed by Barış Elçi")
        help_window.geometry("700x600")
        help_window.resizable(False, False)
        help_window.transient(self)
        help_window.grab_set()
        
        # Center window
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() - 700) // 2
        y = (help_window.winfo_screenheight() - 600) // 2
        help_window.geometry(f"700x600+{x}+{y}")
        
        # Content frame
        content_frame = ctk.CTkFrame(help_window, fg_color=Colors.BG_DARK)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title = ctk.CTkLabel(
            content_frame,
            text="🔗 About HardLinker",
            font=Fonts.get(28, "bold"),
            text_color=Colors.PRIMARY
        )
        title.pack(pady=(0, 20))
        
        # Help text
        help_text = ctk.CTkTextbox(
            content_frame,
            font=Fonts.get(13),
            fg_color=Colors.BG_GLASS,
            wrap="word",
            border_width=0
        )
        help_text.pack(fill="both", expand=True, pady=(0, 20))
        
        info_content = """What is HardLinker?

HardLinker finds duplicate files on your computer and uses Windows' hardlink feature to save disk space.

🔗 What is a Hardlink?

A hardlink is a built-in Windows feature. Unlike a regular file copy, with hardlinks the same data is physically stored on disk only once, but can be accessed through multiple file names.

Think of it like this: A hardlink is like opening multiple doors to the same house. The house (data) is only one, but you can enter through different doors (file names).

✨ Benefits

• Disk Space Savings: If you have 10 copies of the same file, only 1 takes up space.
• File Integrity: Since all hardlinks point to the same data, updating one updates all.
• Safe: It's a Windows native feature, not a third-party hack.

🛡️ Security

The hardlink operation is safe because it's a Windows native feature and there's no risk of data loss. However, make sure you have proper backups of your important data.

When you delete a hardlink, only that reference is deleted. The actual data is preserved as long as other hardlinks are in use. The data is deleted when the last hardlink is removed.

⚠️ Important Notes

• Hardlinks only work between files on the same disk partition.
• Should not be used for system files (program will warn you).
• Back up your important files before first use.

🚀 How It Works

1. Select a folder
2. Program scans files and finds duplicates based on content
3. View the duplicate files found
4. Confirm and create hardlinks
5. Instantly save disk space!

👨‍💻 Developer: Barış Elçi
💻 Version: 1.0.1
📅 2025
"""
        
        help_text.insert("1.0", info_content)
        help_text.configure(state="disabled")
        
        # Close button
        close_btn = ctk.CTkButton(
            content_frame,
            text="Close",
            command=help_window.destroy,
            font=Fonts.get(14, "bold"),
            height=45,
            corner_radius=12,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER
        )
        close_btn.pack()
    
    def setup_main_ui(self):
        """Create main UI components"""
        # Folder selection section
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
            text="No folder selected yet",
            font=Fonts.get(12, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        self.folder_label.pack(side="left", padx=Sizes.PADDING_MEDIUM, pady=12)
        
        self.browse_btn = ctk.CTkButton(
            folder_inner,
            text="📁 Browse Folder",
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
        
        # Progress section
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
            text="Scan not started",
            font=Fonts.get(12, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        self.status_label.pack(side="left")
        
        # Progress bar
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
            text="0 / 0 files scanned",
            font=Fonts.get(10, "bold"),
            text_color=Colors.TEXT_GRAY
        )
        self.progress_label.pack(pady=(0, Sizes.PADDING_MEDIUM))
        
        # Buttons
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, Sizes.PADDING_MEDIUM), padx=Sizes.PADDING_LARGE)
        
        self.scan_btn = ctk.CTkButton(
            button_frame,
            text="Start Scan",
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
            text="Stop",
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
            text="Create Hardlinks",
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
        
        # Results section
        results_header = ctk.CTkFrame(
            self.main_container,
            fg_color=Colors.BG_FRAME,
            height=40,
            corner_radius=10
        )
        results_header.pack(fill="x", pady=(0, Sizes.PADDING_SMALL), padx=Sizes.PADDING_LARGE)
        
        results_label = ctk.CTkLabel(
            results_header,
            text="Scan Results",
            font=Fonts.get(16, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        results_label.pack(pady=Sizes.PADDING_SMALL, padx=Sizes.PADDING_MEDIUM, anchor="w")
        
        # Results textbox
        self.results_textbox = ctk.CTkTextbox(
            self.main_container,
            font=Fonts.get(12),
            corner_radius=12,
            border_width=0,
            fg_color=Colors.BG_GLASS
        )
        self.results_textbox.pack(fill="both", expand=True, padx=Sizes.PADDING_LARGE)
        self.results_textbox.insert("1.0", "Scan results will appear here...\n\nSelect a folder and start scanning!\n")
        self.results_textbox.configure(state="disabled")
        
        # Statistics (bottom)
        stats_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=Colors.BG_FRAME,
            border_width=0,
            corner_radius=12
        )
        stats_frame.pack(fill="x", pady=(Sizes.PADDING_MEDIUM, Sizes.PADDING_LARGE), padx=Sizes.PADDING_LARGE)
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Space to Save: 0 MB | Duplicate Groups: 0 | Total Files: 0",
            font=Fonts.get(11, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        self.stats_label.pack(pady=12)
    
    def browse_folder(self):
        """Folder selection dialog"""
        folder = filedialog.askdirectory(title="Select Folder to Scan")
        if folder:
            self.selected_folder = folder
            self.folder_label.configure(text=f"{folder}")
            self.scan_btn.configure(state="normal")
            self.hardlink_btn.configure(state="disabled")
            self.duplicate_groups = []
            
            # Check for critical folder
            if self.is_critical_folder(folder):
                self.show_critical_warning(folder)
    
    def is_critical_folder(self, folder):
        """Check if folder is critical"""
        folder_path = Path(folder).resolve()
        for critical in self.critical_folders:
            critical_path = Path(critical).resolve()
            try:
                if folder_path == critical_path or folder_path.is_relative_to(critical_path):
                    return True
            except (ValueError, AttributeError):
                if str(folder_path).lower().startswith(str(critical_path).lower()):
                    return True
        return False
    
    def show_critical_warning(self, folder):
        """Show critical folder warning"""
        warning_window = ctk.CTkToplevel(self)
        warning_window.title("CRITICAL SYSTEM FOLDER WARNING")
        warning_window.geometry("500x300")
        warning_window.transient(self)
        warning_window.grab_set()
        
        # Warning icon and message
        warning_label = ctk.CTkLabel(
            warning_window,
            text="⚠️",
            font=Fonts.get(64)
        )
        warning_label.pack(pady=(Sizes.PADDING_LARGE, 10))
        
        title_label = ctk.CTkLabel(
            warning_window,
            text="CRITICAL SYSTEM FOLDER",
            font=Fonts.get(20, "bold"),
            text_color=Colors.ORANGE
        )
        title_label.pack(pady=(0, 10))
        
        message_label = ctk.CTkLabel(
            warning_window,
            text=f"The selected folder is a system folder:\n\n{folder}\n\n"
                 "Creating hardlinks in this folder may\n"
                 "damage your system. Are you sure you want to continue?",
            font=Fonts.get(13),
            justify="center"
        )
        message_label.pack(pady=(0, 20))
        
        # Buttons
        button_frame = ctk.CTkFrame(warning_window, fg_color="transparent")
        button_frame.pack(pady=(0, 20))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=lambda: [warning_window.destroy(), self.reset_folder()],
            width=150,
            fg_color="#d32f2f",
            hover_color="#b71c1c"
        )
        cancel_btn.pack(side="left", padx=5)
        
        continue_btn = ctk.CTkButton(
            button_frame,
            text="Continue Anyway",
            command=warning_window.destroy,
            width=150
        )
        continue_btn.pack(side="right", padx=5)
    
    def reset_folder(self):
        """Reset folder selection"""
        self.selected_folder = None
        self.folder_label.configure(
            text="No folder selected yet",
            text_color=Colors.TEXT_PRIMARY
        )
        self.scan_btn.configure(state="disabled")
    
    def start_scan(self):
        """Start scanning"""
        if not self.selected_folder or self.scanning:
            return
        
        self.scanning = True
        self.cancel_requested = False
        self.scan_btn.configure(state="disabled", text="⏳ Scanning")
        self.cancel_btn.configure(state="normal")
        self.hardlink_btn.configure(state="disabled")
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("1.0", "Starting scan...\n\nCollecting files...\n")
        self.results_textbox.configure(state="disabled")
        
        # Scan in thread
        scan_thread = threading.Thread(target=self.scan_folder, daemon=True)
        scan_thread.start()
    
    def cancel_scan(self):
        """Cancel scanning"""
        if self.scanning:
            self.cancel_requested = True
            self.update_status("⏹️ Cancelling scan...")
            self.update_status_icon("⏹️")
            self.cancel_btn.configure(state="disabled", text="⏹️ Cancelling...")
    
    def scan_folder(self):
        """Scan folder and find duplicate files"""
        try:
            # Collect files
            self.update_status("Collecting files...")
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
            
            # Group by size
            self.update_status("Grouping files by size...")
            self.update_status_icon("📦")
            size_groups = defaultdict(list)
            
            for idx, filepath in enumerate(all_files):
                if self.cancel_requested:
                    self.handle_scan_cancelled()
                    return
                
                try:
                    size = os.path.getsize(filepath)
                    if size > 0:
                        size_groups[size].append(filepath)
                    
                    if idx % 100 == 0:
                        progress = (idx + 1) / total_files
                        self.progress_bar.set(progress)
                        self.update_progress_label(idx + 1, total_files)
                except (PermissionError, OSError):
                    continue
            
            # Hash comparison
            self.update_status("Checking duplicates with hash...")
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
            
            # Filter duplicate groups
            for file_hash, file_list in hash_groups.items():
                if len(file_list) > 1:
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
                    
                    # Only add group if there are multiple unique inodes
                    if len(inodes) > 1:
                        unique_files = [files[0] for files in inodes.values()]
                        if len(unique_files) > 1:
                            self.duplicate_groups.append(unique_files)
            
            # Show results
            self.after(0, self.show_results)
            
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            self.update_status_icon("❌")
        finally:
            self.scanning = False
            self.cancel_requested = False
            self.scan_btn.configure(state="normal", text="🔍 Start Scan")
            self.cancel_btn.configure(state="disabled", text="⛔ Stop")
            self.update_status_icon("✅")
            if self.duplicate_groups:
                self.hardlink_btn.configure(state="normal")
    
    def handle_scan_cancelled(self):
        """Handle scan cancellation"""
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("1.0", 
            "⛔ Scan Cancelled\n\n"
            "Scan was stopped by user.\n"
            "Partial results will not be shown.\n"
        )
        self.results_textbox.configure(state="disabled")
        self.update_status("⛔ Scan cancelled")
        self.update_status_icon("⛔")
        self.progress_bar.set(0)
        self.duplicate_groups = []
    
    def calculate_hash(self, filepath, chunk_size=8192):
        """Calculate SHA256 hash of file"""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def show_results(self):
        """Show scan results"""
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        
        if not self.duplicate_groups:
            self.results_textbox.insert("1.0", 
                "Scan completed!\n\n"
                "No duplicate files found. All your files are unique.\n"
            )
            self.total_space_saved = 0
        else:
            # Calculate total space
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
            
            # Insert summary ONCE at the beginning
            summary_text = (
                f"Scan Completed!\n\n"
                f"📊 Summary:\n"
                f"  • {len(self.duplicate_groups)} duplicate file groups found\n"
                f"  • {total_files_to_link} files will be hardlinked\n"
                f"  • {self.format_size(self.total_space_saved)} disk space will be saved\n\n"
                f"{'─' * 70}\n\n"
            )
            self.results_textbox.insert("1.0", summary_text)
            
            # Group details
            for idx, group in enumerate(self.duplicate_groups[:50], 1):
                try:
                    size = os.path.getsize(group[0])
                    space_saved = size * (len(group) - 1)
                    
                    group_text = (
                        f"📦 Group {idx}:  "
                        f"Size: {self.format_size(size)}  |  "
                        f"Copies: {len(group)}  |  "
                        f"Savings: {self.format_size(space_saved)}\n"
                    )
                    self.results_textbox.insert("end", group_text)
                    
                    for filepath in group[:3]:
                        self.results_textbox.insert("end", f"   📄 {filepath}\n")
                    
                    if len(group) > 3:
                        self.results_textbox.insert("end", f"   ... and {len(group) - 3} more files\n")
                    
                    self.results_textbox.insert("end", "\n")
                    
                except (OSError, Exception):
                    continue
            
            if len(self.duplicate_groups) > 50:
                remaining_groups = len(self.duplicate_groups) - 50
                self.results_textbox.insert("end", 
                    f"💡 ... and {remaining_groups} more groups (total {len(self.duplicate_groups)} groups)\n"
                )
        
        self.results_textbox.configure(state="disabled")
        self.update_stats()
        self.update_status("Scan completed!")
        self.update_status_icon("✅")
        self.progress_bar.set(1.0)
    
    def show_hardlink_preview(self):
        """Show hardlink preview and confirmation"""
        if not self.duplicate_groups:
            return
        
        preview_window = ctk.CTkToplevel(self)
        preview_window.title("Hardlink Preview and Confirmation")
        preview_window.geometry("850x650")
        preview_window.transient(self)
        preview_window.grab_set()
        
        # Title
        title_label = ctk.CTkLabel(
            preview_window,
            text="Hardlink Operation Confirmation",
            font=Fonts.get(22, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        title_label.pack(pady=Sizes.PADDING_LARGE)
        
        # Summary info
        total_files = sum(len(group) - 1 for group in self.duplicate_groups)
        info_label = ctk.CTkLabel(
            preview_window,
            text=f"📊 {len(self.duplicate_groups)} groups | {total_files} files | {self.format_size(self.total_space_saved)} to save",
            font=Fonts.get(13, "bold"),
            text_color=Colors.PRIMARY
        )
        info_label.pack(pady=(0, Sizes.PADDING_MEDIUM))
        
        # Details
        details_frame = ctk.CTkFrame(preview_window)
        details_frame.pack(fill="both", expand=True, padx=Sizes.PADDING_LARGE, pady=(0, Sizes.PADDING_LARGE))
        
        details_textbox = ctk.CTkTextbox(details_frame, font=Fonts.get(11))
        details_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        details_textbox.insert("1.0", 
            f"📋 Files to be Hardlinked:\n\n"
        )
        
        for idx, group in enumerate(self.duplicate_groups[:30], 1):
            try:
                size = os.path.getsize(group[0])
                space_saved = size * (len(group) - 1)
                details_textbox.insert("end", 
                    f"📦 Group {idx}:  "
                    f"{len(group)} files  |  "
                    f"Size: {self.format_size(size)}  |  "
                    f"Savings: {self.format_size(space_saved)}\n"
                )
                details_textbox.insert("end", f"   ✓ Master: {group[0]}\n")
                details_textbox.insert("end", f"   → Will be hardlinked:\n")
                for filepath in group[1:3]:
                    details_textbox.insert("end", f"      {filepath}\n")
                if len(group) > 3:
                    details_textbox.insert("end", f"      ... and {len(group) - 3} more files\n")
                details_textbox.insert("end", "\n")
            except (OSError, Exception):
                continue
        
        if len(self.duplicate_groups) > 30:
            details_textbox.insert("end", f"💡 ... and {len(self.duplicate_groups) - 30} more groups\n")
        
        details_textbox.configure(state="disabled")
        
        # Warning
        warning_label = ctk.CTkLabel(
            preview_window,
            text="This operation cannot be undone! Are you sure you want to continue?",
            font=Fonts.get(11, "bold"),
            text_color=Colors.ORANGE
        )
        warning_label.pack(pady=(0, 10))
        
        # Buttons
        button_frame = ctk.CTkFrame(preview_window, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, Sizes.PADDING_LARGE), padx=40)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
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
            text="Confirm",
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
        """Perform hardlink operation"""
        self.cancel_requested = False
        self.hardlink_btn.configure(state="disabled", text="⏳ Processing")
        self.scan_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal", text="⛔ Stop")
        
        # Run in thread
        hardlink_thread = threading.Thread(target=self.do_hardlink, daemon=True)
        hardlink_thread.start()
    
    def do_hardlink(self):
        """Do hardlink operation"""
        success_count = 0
        fail_count = 0
        total_saved = 0
        total_groups = len(self.duplicate_groups)
        
        self.update_status("⚡ Hardlink operation started...")
        
        for idx, group in enumerate(self.duplicate_groups):
            if self.cancel_requested:
                self.update_status("⛔ Hardlink operation cancelled!")
                self.show_completion_message(success_count, fail_count, total_saved, cancelled=True)
                break
            
            try:
                master_file = group[0]
                
                for duplicate_file in group[1:]:
                    if self.cancel_requested:
                        break
                    
                    try:
                        backup_file = duplicate_file + ".backup_temp"
                        os.rename(duplicate_file, backup_file)
                        os.link(master_file, duplicate_file)
                        os.remove(backup_file)
                        
                        size = os.path.getsize(master_file)
                        total_saved += size
                        success_count += 1
                        
                    except Exception as e:
                        fail_count += 1
                        try:
                            if os.path.exists(backup_file):
                                if os.path.exists(duplicate_file):
                                    os.remove(duplicate_file)
                                os.rename(backup_file, duplicate_file)
                        except:
                            pass
                
                progress = (idx + 1) / total_groups
                self.progress_bar.set(progress)
                self.update_status(f"⚡ Processing: {idx + 1}/{total_groups} groups")
                
            except Exception as e:
                fail_count += 1
                continue
        
        if not self.cancel_requested:
            self.show_completion_message(success_count, fail_count, total_saved)
        
        self.hardlink_btn.configure(state="disabled", text="⚡ Create Hardlinks")
        self.scan_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled", text="⛔ Stop")
        
        if not self.cancel_requested:
            self.update_status("Operation completed!")
            self.progress_bar.set(1.0)
        else:
            self.update_status("⛔ Operation cancelled!")
            self.progress_bar.set(0)
    
    def show_completion_message(self, success, fail, saved, cancelled=False):
        """Show completion message"""
        if cancelled:
            message = (
                f"⛔ Hardlink Operation Cancelled\n\n"
                f"Operation was stopped by user.\n\n"
                f"Successful: {success} files\n"
                f"Failed: {fail} files\n"
                f"Space Saved: {self.format_size(saved)}\n\n"
                f"Note: Operation not completed."
            )
            self.after(0, lambda: messagebox.showwarning("Operation Cancelled", message))
        else:
            message = (
                f"Hardlink Operation Completed!\n\n"
                f"Successful: {success} files\n"
                f"Failed: {fail} files\n"
                f"Space Saved: {self.format_size(saved)}\n"
            )
            self.after(0, lambda: messagebox.showinfo("Operation Completed", message))
    
    def update_status(self, text):
        """Update status message"""
        self.after(0, lambda: self.status_label.configure(text=text))
    
    def update_status_icon(self, icon):
        """Update status icon"""
        self.after(0, lambda: self.status_icon.configure(text=icon))
    
    def update_progress_label(self, current, total):
        """Update progress label"""
        self.after(0, lambda: self.progress_label.configure(
            text=f"📊 {current:,} / {total:,} files scanned"
        ))
    
    def update_stats(self):
        """Update statistics"""
        total_files = sum(len(group) for group in self.duplicate_groups)
        stats_text = (
            f"💾 Space to Save: {self.format_size(self.total_space_saved)} | "
            f"📁 Duplicate Groups: {len(self.duplicate_groups)} | "
            f"📄 Total Files: {total_files}"
        )
        self.stats_label.configure(text=stats_text)
    
    def format_size(self, bytes_size):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"


def main():
    """Start application"""
    # Create main app first
    app = HardLinkerApp()
    
    # Admin check - show after app is created
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin and settings.should_show_admin_warning():
            # Schedule admin warning after app starts
            app.after(100, lambda: show_admin_warning_dialog(app))
    except:
        pass
    
    app.mainloop()


def show_admin_warning_dialog(parent):
    """Show admin warning dialog with checkbox"""
    warning_window = ctk.CTkToplevel(parent)
    warning_window.title("Administrator Rights")
    warning_window.geometry("500x400")
    warning_window.resizable(False, False)
    
    # Center window
    warning_window.update_idletasks()
    x = (warning_window.winfo_screenwidth() - 500) // 2
    y = (warning_window.winfo_screenheight() - 400) // 2
    warning_window.geometry(f"500x400+{x}+{y}")
    
    # Content frame
    content_frame = ctk.CTkFrame(warning_window, fg_color=Colors.BG_DARK)
    content_frame.pack(fill="both", expand=True, padx=30, pady=30)
    
    # Warning icon
    warning_icon = ctk.CTkLabel(
        content_frame,
        text="⚠️",
        font=Fonts.get(48)
    )
    warning_icon.pack(pady=(0, 15))
    
    # Title
    title_label = ctk.CTkLabel(
        content_frame,
        text="Administrator Rights",
        font=Fonts.get(20, "bold"),
        text_color=Colors.PRIMARY
    )
    title_label.pack(pady=(0, 10))
    
    # Message
    message_label = ctk.CTkLabel(
        content_frame,
        text="Administrator rights may be required to create hardlinks.\n\n"
             "If the operation fails, please run the program\n"
             "as administrator (Right-click → Run as administrator).",
        font=Fonts.get(13),
        justify="center"
    )
    message_label.pack(pady=(0, 20))
    
    # Don't show again checkbox
    show_again_var = ctk.BooleanVar(value=False)
    
    checkbox = ctk.CTkCheckBox(
        content_frame,
        text="Don't show this again",
        variable=show_again_var,
        font=Fonts.get(12),
        fg_color=Colors.PRIMARY,
        hover_color=Colors.PRIMARY_HOVER
    )
    checkbox.pack(pady=(0, 20))
    
    # OK button
    def on_ok():
        if show_again_var.get():
            settings.set_show_admin_warning(False)
        warning_window.destroy()
    
    ok_btn = ctk.CTkButton(
        content_frame,
        text="OK",
        command=on_ok,
        font=Fonts.get(14, "bold"),
        height=45,
        width=150,
        corner_radius=12,
        fg_color=Colors.PRIMARY,
        hover_color=Colors.PRIMARY_HOVER
    )
    ok_btn.pack()
    
    # Make window modal
    warning_window.transient(parent)
    warning_window.grab_set()


if __name__ == "__main__":
    main()
