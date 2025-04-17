# pip install spotdl spotipy tk

import os
import sys
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


def log_message(message):
    """Append a line of text to the console output."""
    console_text.insert(tk.END, message + "\n")
    console_text.see(tk.END)


def download_playlist():
    # Gather inputs
    playlist_url = url_entry.get().strip()
    client_id = client_id_entry.get().strip()
    client_secret = client_secret_entry.get().strip()

    if not playlist_url:
        messagebox.showerror("Error", "Please enter a Spotify playlist URL")
        return

    if not client_id or not client_secret:
        messagebox.showerror(
            "Error",
            "Please enter both Spotify Client ID and Client Secret"
        )
        return

    folder = folder_path.get()
    if not folder:
        messagebox.showerror("Error", "Please select a download folder")
        return

    log_message(f"📂 Downloading playlist to: {folder}")
    log_message(f"🔗 Spotify URL: {playlist_url}")

    def run_sequential():
        try:
            import spotipy
            from spotipy.oauth2 import SpotifyClientCredentials

            auth_manager = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
            sp = spotipy.Spotify(auth_manager=auth_manager)

            # Extract playlist ID and fetch metadata
            pid = playlist_url.rstrip('/').split('/')[-1].split('?')[0]
            meta = sp.playlist(pid, fields=['name'])
            pl_name = meta['name']

            # Fetch tracks
            items = []
            results = sp.playlist_items(pid)
            items.extend(results['items'])
            while results['next']:
                results = sp.next(results)
                items.extend(results['items'])

            total = len(items)
            log_message(f"🎵 Found {total} tracks in '{pl_name}'")

            bitrate = "192k"
            for idx, entry in enumerate(items, start=1):
                track = entry['track']
                t_url = track['external_urls']['spotify']
                title = track.get('name', 'unknown')
                num = f"{idx:02d}"
                out_dir = os.path.join(folder, pl_name)
                os.makedirs(out_dir, exist_ok=True)
                filename = f"{num} - {title}.mp3"
                out_path = os.path.join(out_dir, filename)

                log_message(f"⬇️ [{idx}/{total}] {title}")
                cmd = [
                    sys.executable,
                    "-m", "spotdl", "download", t_url,
                    "--bitrate", bitrate,
                    "--output", out_path
                ]

                proc = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True
                )
                for line in proc.stdout:
                    log_message(line.rstrip())
                proc.wait()

                if proc.returncode != 0:
                    log_message(f"❌ Failed: {title} (code {proc.returncode})")
                else:
                    log_message(f"✅ Completed: {title}")

            messagebox.showinfo("Success", "All tracks processed")
        except Exception as e:
            log_message(f"❌ Error: {e}")
            messagebox.showerror("Error", str(e))

    threading.Thread(target=run_sequential, daemon=True).start()


def choose_folder():
    selected = filedialog.askdirectory()
    if selected:
        folder_path.set(selected)

# --- GUI Setup ---
root = tk.Tk()
root.title("Spotify Playlist Downloader")
root.geometry("640x600")

# Credentials frame
cred_frame = tk.Frame(root)
cred_frame.pack(pady=10)

tk.Label(cred_frame, text="Client ID:").grid(row=0, column=0, sticky="e", padx=5)
client_id_entry = tk.Entry(cred_frame, width=40)
client_id_entry.grid(row=0, column=1, pady=2)

tk.Label(cred_frame, text="Client Secret:").grid(row=1, column=0, sticky="e", padx=5)
client_secret_entry = tk.Entry(cred_frame, show="*", width=40)
client_secret_entry.grid(row=1, column=1, pady=2)

# Spotify URL input
tk.Label(root, text="Spotify Playlist URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

# Folder chooser
tk.Label(root, text="Download Folder:").pack(pady=5)
folder_path = tk.StringVar()
tk.Entry(root, textvariable=folder_path, width=45, state="readonly").pack(pady=5)
tk.Button(root, text="Choose Folder", command=choose_folder).pack(pady=5)

# Download button
tk.Button(
    root, text="Download Playlist",
    command=download_playlist,
    bg="green", fg="white"
).pack(pady=10)

# Console output area
tk.Label(root, text="Console:").pack(pady=5)
console_text = scrolledtext.ScrolledText(root, width=80, height=20)
console_text.pack(pady=5)

root.mainloop()
