from tkinter import *

class StegToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Displaying text in the tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x1, y1, x2, y2 = self.widget.bbox("insert")
        x1 = x1 + self.widget.winfo_rootx() + 57
        y1 = y1 + y2 + self.widget.winfo_rooty() +27
        tooltip_window = Toplevel(self.widget)
        self.tipwindow = tooltip_window
        tooltip_window.wm_overrideredirect(1)
        tooltip_window.wm_geometry("+%d+%d" % (x1, y1))
        label = Label(tooltip_window,
                      text=self.text,
                      justify=LEFT,
                      background="#ffffe0",
                      relief=SOLID,
                      borderwidth=1,
                      font=("tahoma", "10", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        "Destroying text in the tooltip window"
        tooltip_window = self.tipwindow
        self.tipwindow = None
        if tooltip_window:
            tooltip_window.destroy()

