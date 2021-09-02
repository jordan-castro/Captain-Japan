# TODO import selenium
import requests
from bs4 import BeautifulSoup
from generator.text_gen import generate_text_file
import tkinter as tk
from tkinter import ttk, scrolledtext



URL = "https://www.wuxiaworld.com/novel/necropolis-immortal/necro-chapter-964"
page = requests.get(URL)

window = tk.Tk()

def find_text(text):
    if not text:
        return None
    else:
        return "Chapter" in text


soup = BeautifulSoup(page.content, "html.parser")
chapter_data = soup.find_all(dir="ltr")
chapter_title = soup.find_all(
    "h4", 
    string=lambda text: find_text(text)
)[0].text.strip().split(":")[-1]

chapter_text = ""
for data in chapter_data:
    if data == chapter_data[-1]:
        chapter_text += data.text
    else:
        chapter_text += f"{data.text}\n\n"

generate_text_file(chapter_text, chapter_title)

window.title(chapter_title)

scroll = scrolledtext.ScrolledText(window, width=100, height=50, wrap=tk.WORD)
scroll.pack()
scroll.insert(tk.INSERT, chapter_text)

window.mainloop()