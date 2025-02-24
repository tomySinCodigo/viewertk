import tkinter as tk
import time
from pathlib import Path
from PIL import ImageTk, Image, ImageOps



class ViewerC(tk.Frame):
    def __init__(self, parent, *args, **kw):
        super(ViewerC, self).__init__(master=parent, *args, **kw)
        self.parent = parent
        self._configViewerC()

    def _configViewerC(self):
        self.DATA = None
        self.RSZ = False
        self.LTR = 0 # last time resize
        self.ICACHE = {} # cache de imagenes
        self.HZ = True # horizontal
        bg = self.cget("bg")
        self.cv = tk.Canvas(master=self.parent, bg=bg, borderwidth=0, bd=0)
        self.cv.grid(row=0, column=0, sticky='wens')
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        self.bind("<Configure>", self.resizer)
        self.parent.bind("<Button-3>", self.orientacion)

    def setImage(self, file:str):
        img = Path(file).as_posix()
        imgp = Image.open(img)
        img_tk = ImageTk.PhotoImage(imgp)
        self.DATA = {
            "file":img,
            "w":img_tk.width(),
            "h":img_tk.height(),
            "Image":imgp,
            "img tk":img_tk,
            "wh":(img_tk.width(),img_tk.height())
        }
        self.img_id = self.cv.create_image(0,0,image=img_tk,anchor="nw")

    def setBg(self, color:str):
        self.cv.config(bg=color)
        self.config(bg=color)

    def resizer(self, e=None):
        # now = time.time()
        # if now - self.LTR > 0.1:
        #     self.LTR = now
        #     self._setImageResized(e.width, e.height)

        self._setImageResized(e.width, e.height)

    def _setImageResized(self, w, h):
        rsz_img = self._cachedImage(self.DATA.get("Image"), w, h)
        img_tk = ImageTk.PhotoImage(rsz_img)
        self.cv.itemconfig(self.img_id, image=img_tk)
        self.cv.image = img_tk
        self.DATA["img tk"] = img_tk
        self.DATA["wh"] = (img_tk.width(),img_tk.height())

    def _cachedImage(self, image, w, h):
        clave = (w, h)
        if clave not in self.ICACHE: #0-6 low-high
            self.ICACHE[clave] = ImageOps.fit(image, (w, h), method=2) \
                if self.HZ else ImageOps.pad(image, (w,h), method=2)
        return self.ICACHE[clave]
    
    def orientacion(self, e=None):
        print("clciky")
        w, h = self.DATA.get("wh")
        print(w,h)
        if w:
            self._setImageResized(w, h)
            self.HZ = not self.HZ
        # self.cv.update()
        # self.parent.update()
        self.parent.geometry(f"{w+1}x{h+1}")
        
        # img = self.DATA.get("file")
        # img = self.DATA.get("file")
        # self.img_id = self.cv.create_image(0,0,image=img_tk,anchor="nw")
        # self.setImage(img)

        # self.setImage_wh(self.DATA.get("Image"), w, h)
        # self._setImageResized(w, h)

    def setImage_wh(self, img:str, w, h) -> Image:
        image = ImageOps.fit(img, (w, h), method=2) \
            if self.HZ else ImageOps.pad(img, (w,h), method=2)
        img_tk = ImageTk.PhotoImage(image)
        self.cv.itemconfig(self.img_id, image=img_tk)
        self.cv.image = img_tk
        self.DATA["img tk"] = img_tk
        self.DATA["wh"] = (img_tk.width(),img_tk.height())


if __name__ == '__main__':
    vn = tk.Tk()
    vn.geometry('400x220')
    wg = ViewerC(vn)
    wg.setImage("frog.jpg")
    wg.grid(row=0, column=0, sticky='wens')
    wg.setBg("blue")
    # wg.orientacion()
    # wg.orientacion()

    vn.columnconfigure(0, weight=1)
    vn.rowconfigure(0, weight=1)
    vn.mainloop()