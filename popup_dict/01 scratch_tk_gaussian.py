#!/usr/bin/env python3
"""Testing"""

from ctypes import windll
import tkinter as tk

windll.shcore.SetProcessDpiAwareness(1)

class FloatingWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.w = 1900
        self.h = 700
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        x = (w / 2) - (self.w / 2)
        y = (h / 2) - (self.h / 2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

        self.overrideredirect(True)
        self.config(bg='green')
        self.attributes('-alpha', 0.99)
        self.wm_attributes("-transparent", 'green')
        self.update()



        self.label = tk.Label(text="要是你見了",
                              font=('kaiti 32'),
                              foreground="#f1f1e4",
                              bg='#272822',
                              highlightbackground='#2e2f29',
                              highlightthickness=1.5)
        self.label.pack(side="top", fill="both", expand=True)


if __name__ == '__main__':
    fw = FloatingWindow()
    fw.mainloop()
