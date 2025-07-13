import threading
import os
import yt_dlp
from pathlib import Path
from datetime import datetime, timezone
import ctypes
import time
from gui import DownloaderGUI

DOWNLOAD_FOLDER = str(Path.home() / "Downloads")

class YouTubeDownloader:
    def __init__(self, gui):
        self.gui = gui

    def download(self, url, fmt):
        print(f"Download startet: {url} im Format {fmt}")


class Downloader:
    def __init__(self):
        self.app = DownloaderGUI(self.start_download)
        self.downloading = False

    def run(self):
        self.app.mainloop()

        

    def start_download(self, url, fmt):
        if self.downloading:
            self.show_message("Nur ein Download gleichzeitig möglich!")
            return
        if not url:
            self.show_message("Bitte YouTube URL eingeben!")
            return

        self.downloading = True
        self.app.disable_download()
        self.app.set_progress(0)
        threading.Thread(target=self.download_thread, args=(url, fmt), daemon=True).start()

    def download_thread(self, url, fmt):
        ydl_opts = {
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            "format": "bestaudio/best" if fmt == "mp3" else "bestvideo+bestaudio/best",
            "postprocessors": [],
            "progress_hooks": [self.progress_hook],
            "quiet": True,
            "no_warnings": True,
        }
        if fmt == "mp3":
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                self.title = info.get("title", "downloaded_file")
                ydl.download([url])
            self.set_file_date_utc_now()
            self.show_message("Download abgeschlossen!")
        except Exception as e:
            self.show_message(f"Fehler: {e}")
        finally:
            self.downloading = False
            self.app.enable_download()
            self.app.set_progress(0)

    def progress_hook(self, d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
            downloaded = d.get("downloaded_bytes", 0)
            progress = downloaded / total * 100
            self.app.set_progress(progress)
        elif d["status"] == "finished":
            self.app.set_progress(100)

    def set_file_date_utc_now(self):
        # Datei-Pfad ermitteln
        ext = "mp3" if self.app.format_var.get() == "mp3" else "mp4"
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{self.title}.{ext}")

        local_time = datetime(2025, 7, 5, 3, 9)

        local_time = local_time.astimezone()
        utc_time = local_time.astimezone(timezone.utc)

        timestamp = utc_time.timestamp()

        os.utime(file_path, (timestamp, timestamp))

    def show_message(self, text):
        from tkinter import messagebox
        messagebox.showinfo("Info", text)

if __name__ == "__main__":
    downloader = Downloader()
    downloader.run()
