import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import time
import pygame
import threading

def load_lrc(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    lyrics = []
    for line in lines:
        if not line.startswith('['):
            continue
        try:
            time_tag, text = line.strip().split(']', 1)
            timestamp = time_tag[1:]
            mins, secs = map(float, timestamp.split(':'))
            if not text.strip():
                continue  # skip empty lyric lines
            lyrics.append((mins * 60 + secs, text.strip()))
        except ValueError:
            continue  # skip lines that aren't valid time+text
    return lyrics

class SimpleLyricPopup:
    def __init__(self, audio_file, lrc_file, english_lines):
        self.audio_file = audio_file
        self.lyrics = load_lrc(lrc_file)
        self.english_lines = english_lines
        self.index = 0
        self.running = True

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.title("Agust D - 28")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.bg_image = Image.open("bg1.jpg")
        self.bg_image = self.bg_image.resize((800, 800), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.custom_font = tkfont.Font(family="Caveat Brush", size=22)

        self.label = tk.Label(
            self.root,
            text="",
            font=self.custom_font,
            # fg="white",
            # bg="black",
            wraplength=750,
            justify="center"
        )
        self.label.pack(expand=True)

    def on_close(self):
        self.running = False
        pygame.mixer.music.stop()
        self.root.destroy()

    def fade_in_text(self, text):
        self.label.config(text=text)
        for i in range(0, 10):
            color = f'#{i*12:02x}{i*12:02x}{i*12:02x}'
            self.label.config(fg=color)
            self.root.update()
            time.sleep(0.03)

    def fade_out_text(self):
        for i in reversed(range(0, 10)):
            color = f'#{i*12:02x}{i*12:02x}{i*12:02x}'
            self.label.config(fg=color)
            self.root.update()
            time.sleep(0.03)

    def start(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play()

        threading.Thread(target=self.update_lyrics, daemon=True).start()
        self.root.mainloop()

    def update_lyrics(self):
        start_time = time.time()
        for i, (ts, _) in enumerate(self.lyrics):
            if not self.running:
                break
            delay = ts - (time.time() - start_time)
            if delay > 0:
                time.sleep(delay)
            if i > 0:
                self.fade_out_text()
                # time.sleep(delay)
            self.fade_in_text(self.english_lines[i])
            # self.label.config(text=self.english_lines[i])

# === ENGLISH LYRICS ===
english_lyrics = [
    "As we grow older, getting to know the world",
    "And yet, knowing the world felt more like a weakness",
    "Gazing at a night view so different from this dark room, I murmured the words",
    "I guess he's getting older and I don't remember",
    "What were the things I wished for? I'm scared now, where did the fragments of my dreams go?",
    "Though I'm breathing, it feels like my heart has broken down",
    "Yeah, to talk about now, finding it hard to hold onto your dream, that's becoming an adult",
    "I thought I'd change when I turned twenty, I thought I'd change when I graduated",
    "Shit, like that, that, when I become thirty, so what's changed about me?",
    "Sometimes, tears suddenly pour down with no reason",
    "The life I wished for, the life I wanted, a so-so life",
    "Whatever it is, it doesn't matter anymore",
    "For just one day, without any concerns, for just one day, without any worries, to live, to live, to live",
    "I guess he's getting older and I don't remember",
    "What were the things I wished for? I'm scared now, where did the fragments of my dreams go?",
    "Though I'm breathing, it feels like my heart has broken down",
    "Yeah, to talk about now, finding it hard to hold onto your dream, that's becoming an adult"
]

if __name__ == "__main__":
    app = SimpleLyricPopup("28.mp3", "28.lrc.txt", english_lyrics)
    app.start()
