from pathlib import Path
import tkinter as tk
from PIL import ImageTk, Image, ImageOps


class ViewerTk(tk.Canvas):
    def __init__(self, parent, *args, **kw):
        super(ViewerTk, self).__init__(master=parent, *args, **kw)
        self.parent = parent
        self._configViewerTk()

    def _configViewerTk(self):
        self.HOR = True
        self.DATA = {}
        self.parent.bind("<Button-3>", self._orientacion)
        # self.parent.bind("<Button-3>", self.fix)
        self.parent.bind("<space>", self.fix)

    def _setFile(self, file=str, wh=None, change=False) -> dict:
        archivo = Path(file).as_posix()
        img_pil = Image.open(archivo)
        wh = self._getWH() if not wh else wh
        print('wh :: ', wh)
        red_img = ImageOps.fit(img_pil, wh, method=5) \
        if self.HOR else ImageOps.pad(img_pil, wh, method=5)
        if change:
            self.HOR = not self.HOR
        img_tk = ImageTk.PhotoImage(red_img)
        self.DATA = {
            "file":archivo,
            "img_pil":img_pil,
            "img_tk":img_tk,
            "wh":wh
        }
    
    def _setImage(self, img:str, wh=None, change=True):
        self._setFile(file=img, wh=wh, change=change)
        img_tk = self.DATA.get("img_tk")
        self.img_id = self.create_image(
            0,0,image=img_tk,anchor="nw"
        )
        self.image = img_tk

    def _getWH(self):
        self.update_idletasks()
        gm = self.parent.geometry()
        i = gm.index("+")
        res = gm[:i]
        w, h = map(int, res.split("x"))
        # return self.winfo_width(), self.winfo_height()
        return w, h
    
    def _getGeo(self):
        self.update_idletasks()
        return self.winfo_width(), self.winfo_height()

    def _orientacion(self, e=None):
        self._setImage(self.DATA.get("file"), self._getGeo())

    def fix(self, e=None):
        self._setImage(self.DATA.get("file"), self._getGeo(), False)
        self.update_idletasks()



if __name__ == '__main__':
    vn = tk.Tk()
    vn.geometry('600x400')
    wg = ViewerTk(vn, bg="red")
    wg.grid(row=0, column=0, sticky='wens')
    wg.rowconfigure(0, weight=1)
    wg.columnconfigure(0, weight=1)

    wg.HOR = False
    wg._setImage("frog.jpg")


    vn.columnconfigure(0, weight=1)
    vn.rowconfigure(0, weight=1)
    vn.mainloop()