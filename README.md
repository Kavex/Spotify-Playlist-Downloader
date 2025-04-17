# Spotify Playlist Downloader

A simple Tkinter-based application that lets you download Spotify playlists track‑by‑track using [spotDL](https://github.com/spotDL/spotify-downloader) and the Spotify Web API (via [Spotipy](https://spotipy.readthedocs.io/)).

---

## Features

- **GUI interface** with fields for Spotify **Client ID**, **Client Secret**, **Playlist URL**, and **Download Folder**  
- Sequential download of each track in a playlist  
- Real-time console log inside the app window  
- Automatic organization: saves into `DownloadFolder/PlaylistName/XX - TrackTitle.mp3`  
- Customizable audio bitrate (default: 192 kbps)  

---

## Prerequisites

- **Python 3.7+** installed and on your PATH  
- **ffmpeg** installed and on your PATH  
- Spotify Developer credentials:  
  - **Client ID**  
  - **Client Secret**  
  - Create an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) to obtain these  

---

## Installation

1. Clone or download this repository.  
2. Install required Python packages:

```bash
pip install spotdl spotipy tk
```
   
3. Install ffmpeg, you can check the version using this command

```bash
ffmpeg -version
```
