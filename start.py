from gui import DownloaderGUI
from downloader import YouTubeDownloader
import tkinter as tk

def main():
    app = DownloaderGUI(download_callback=None)
    downloader = YouTubeDownloader(app)
    app.download_callback = downloader.download
    app.mainloop()

if __name__ == "__main__":
    main()
