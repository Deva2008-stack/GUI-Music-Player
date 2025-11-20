import pygame
import os
import tkinter as tk
from tkinter import filedialog, Listbox, SINGLE

pygame.mixer.init()

current_index = -1
songs = []


def play_selected_song():
    global current_index
    selection = song_listbox.curselection()
    if not selection:
        return
    current_index = selection[0]
    song_path = songs[current_index]
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    now_playing_label.config(text=f"Playing: {os.path.basename(song_path)}")


def pause_resume():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        now_playing_label.config(text="Paused")
    else:
        pygame.mixer.music.unpause()
        now_playing_label.config(text="Resumed")


def stop_song():
    pygame.mixer.music.stop()
    now_playing_label.config(text="Stopped")


def next_song():
    global current_index
    if not songs:
        return
    
    current_index = (current_index + 1) % len(songs)
    song_listbox.selection_clear(0, tk.END)
    song_listbox.selection_set(current_index)
    play_selected_song()


def load_folder():
    global songs
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return
    
    songs = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".mp3")]

    song_listbox.delete(0, tk.END)

    for s in songs:
        song_listbox.insert(tk.END, os.path.basename(s))

    now_playing_label.config(text="Songs Loaded.")


root = tk.Tk()
root.title("Simple Music Player")
root.geometry("400x500")
root.resizable(False, False)


load_btn = tk.Button(root, text="Load Music Folder", command=load_folder, width=30, height=2)
load_btn.pack(pady=10)


song_listbox = Listbox(root, selectmode=SINGLE, width=50, height=15)
song_listbox.pack(pady=10)


now_playing_label = tk.Label(root, text="No song playing", font=("Arial", 12))
now_playing_label.pack(pady=5)


control_frame = tk.Frame(root)
control_frame.pack(pady=10)

play_btn = tk.Button(control_frame, text="Play", width=10, command=play_selected_song)
play_btn.grid(row=0, column=0, padx=5)

pause_btn = tk.Button(control_frame, text="Pause/Resume", width=15, command=pause_resume)
pause_btn.grid(row=0, column=1, padx=5)

stop_btn = tk.Button(control_frame, text="Stop", width=10, command=stop_song)
stop_btn.grid(row=0, column=2, padx=5)

next_btn = tk.Button(root, text="Next Song", width=20, command=next_song)
next_btn.pack(pady=5)

root.mainloop()
