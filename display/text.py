import tkinter as tk
from tkinter import scrolledtext
import codecs


def display_txt(text, is_file=False):
    """
    Display some text within a Tkinter window.

    Params:
        - <text: str> The text to display | .txt file path
        - <is_file=False: bool> Whether or not the <text> param is a file path
    """
    # Tk window
    win = tk.Tk()
    # Scrolled Text Widget
    scroll = scrolledtext.ScrolledText(win, width=100, height=50, wrap=tk.WORD)
    scroll.pack()

    if is_file:
        # Open and grab
        with codecs.open(text, "r", "utf-8") as text_file:
            text = text_file.read()
    
    # Put text
    scroll.insert(tk.INSERT, text)

    # Show
    win.mainloop()