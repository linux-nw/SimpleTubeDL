import tkinter as tk
from tkinter import ttk

# Farbpalette
PRIMARY_COLOR = "#01aacd"
BG_COLOR = "#1e1e1e"         # Dunkelgrau
FG_COLOR = "#e0e0e0"
ACCENT_COLOR = "#2a2a2a"
BTN_COLOR = "#ff3b3b"        # Roter Akzent
BTN_HOVER = "#ff5555"

class DownloaderGUI(tk.Tk):
    def __init__(self, download_callback):
        super().__init__()
        self.title("🔥 YouTube Downloader")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.geometry("520x350")

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=("Segoe UI", 11))
        style.configure("TEntry", fieldbackground=ACCENT_COLOR, foreground=FG_COLOR, font=("Segoe UI", 11))
        style.configure("TButton", background=BTN_COLOR, foreground="white", font=("Segoe UI", 12, "bold"), borderwidth=0)
        style.map("TButton", background=[('!active', BTN_COLOR)])
        style.map("TRadiobutton", background=[('!active', BG_COLOR)], foreground=[('!active', FG_COLOR)])
        style.configure("TRadiobutton", background=BG_COLOR, foreground=FG_COLOR, font=("Segoe UI", 11))
        style.configure("Horizontal.TProgressbar", troughcolor=ACCENT_COLOR, background=PRIMARY_COLOR)

        self.download_callback = download_callback

        # YouTube URL
        ttk.Label(self, text="🎥 YouTube URL:").pack(pady=(20, 3), anchor="w", padx=30)

        url_frame = tk.Frame(self, bg=BG_COLOR)
        url_frame.pack(padx=30, fill="x")

        self.url_entry = ttk.Entry(url_frame, width=60)
        self.url_entry.pack(side="left", fill="x", expand=True, ipady=6)

        paste_btn = tk.Button(
            url_frame, text="📋", bg=BTN_COLOR, fg="white",
            activebackground=BTN_HOVER, borderwidth=0,
            font=("Segoe UI", 11, "bold"), command=self._paste_url
        )
        paste_btn.pack(side="right", ipadx=8, ipady=2)

        # Format Auswahl
        ttk.Label(self, text="💾 Format:").pack(pady=(20, 3), anchor="w", padx=30)
        self.format_var = tk.StringVar(value="mp4")
        ttk.Radiobutton(self, text="MP4 (Video)", variable=self.format_var, value="mp4").pack(anchor="w", padx=45)
        ttk.Radiobutton(self, text="MP3 (Audio)", variable=self.format_var, value="mp3").pack(anchor="w", padx=45)

        # Fortschrittsbalken
        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, variable=self.progress, maximum=100, style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, padx=30, pady=25)

        # Download Button
        self.download_btn = ttk.Button(self, text="Download starten", command=self._on_download)
        self.download_btn.pack(pady=(5, 20), ipadx=10, ipady=8)

    def _on_download(self):
        url = self.url_entry.get().strip()
        fmt = self.format_var.get()
        self.download_callback(url, fmt)

    def _paste_url(self):
        try:
            clip = self.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clip)
        except tk.TclError:
            pass

    def set_progress(self, val):
        self.progress.set(val)

    def disable_download(self):
        self.download_btn.state(["disabled"])

    def enable_download(self):
        self.download_btn.state(["!disabled"])
