import tkinter as tk
from tkinter import ttk
from kviewer import KViewer


class TestWidgetPane(tk.Frame):
    def __init__(self, parent, *args, **kw):
        super(TestWidgetPane, self).__init__(master=parent, *args, **kw)
        self.parent = parent
        self._configTestWidgetPane()

    def _configTestWidgetPane(self):
        pw = tk.PanedWindow(
            self, orient=tk.VERTICAL, bg='skyblue'
        )
        pw.grid(row=0, column=0, sticky='wens')

        self.viewer = KViewer(pw, bg='green')
        tex = tk.Text(pw, bg='red')
        tex.insert(tk.END, "holas  sa")

        pw.add(self.viewer)
        pw.add(tex, minsize=30)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.parent.bind('<Button-3>', self.viewer.changeModeView)
        pw.bind('<ButtonRelease>', self.viewer._resize)


if __name__ == '__main__':
    vn = tk.Tk()
    vn.geometry('250x420')
    wg = TestWidgetPane(vn, bg='pink')
    # wg = KViewer(vn, bg='yellow')
    wg.grid(row=0, column=0, sticky='wens')
    vn.columnconfigure(0, weight=1)
    vn.rowconfigure(0, weight=1)
    vn.mainloop()