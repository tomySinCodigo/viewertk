from pathlib import Path
import tkinter as tk
from PIL import ImageTk, Image, ImageOps


class ViewerTkBasico(tk.Frame):
    def __init__(self, parent, *args, **kw):
        super(ViewerTkBasico, self).__init__(master=parent, *args, **kw)
        self.parent = parent
        self._configViewerTkBasico()

    def _configViewerTkBasico(self):
        self.DATA = {}
        self.HOR = True # orientacion
        bg = self.cget("bg")
        self.cv = tk.Canvas(master=self.parent, bg="blue", borderwidth=0, bd=0)
        self.cv.grid(row=0, column=0, sticky='wens')
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        self.parent.bind("<Button-3>", self.fix)

        # self.bt = tk.Button(self.parent, text="T", command=self.resizer)
        # self.bt_id = self.cv.create_window(14,18,window=self.bt)

        # self.imgtk_bt = tk.PhotoImage(file="boton.png")
        # self.bti = self.cv.create_image(60,20,image=self.imgtk_bt, anchor="center")

        # self.bt = self.cv.create_rectangle(
        #     0,0,100,30,fill="gray30",outline="gray"
        # )
        # self.cv.tag_bind(self.bt, "<Button-1>", self._presionado)

        # self.bt = tk.Button(self, text="RES", command=self._presionado, width=40, height=20)
        # self.bt = tk.Button(self.parent, text="T", command=lambda: print("¡Botón presionado!"))
        # self.bt = tk.Button(self.parent, text="RES", command=self.resizer)
        # self.bt.place(relx=0.98, rely=0.98, anchor="se")
        

    def setImage(self, file:str):
        img = Path(file).as_posix()
        imgp = Image.open(img)
        self.update_idletasks()
        print(self.parent.geometry())
        
        wh = self._getWH()
        red_img = ImageOps.fit(imgp, wh, method=5) \
        if self.HOR else ImageOps.pad(imgp, wh, method=5)
        self.HOR = not self.HOR
        img_tk = ImageTk.PhotoImage(red_img)
        self.DATA = {
            "file":img,
            "w":img_tk.width(),
            "h":img_tk.height(),
            "Image":imgp,
            "img tk":img_tk
        }
        self.img_id = self.cv.create_image(0,0,image=img_tk,anchor="nw")
        self.cv.image = img_tk
        print("aasignado iMagen")

        # self.imgtk_bt = tk.PhotoImage(file="boton.png")
        # self.bti = self.cv.create_image(60,20,image=self.imgtk_bt, anchor="center")

    def resizer(self, e=None):
        if not e:
            wh = self._getWH()
        else:
            wh = (e.width, e.height)
        self._resizeImage(wh)

    def _resizeImage(self, wh:tuple):
        """redimensionar imagen wh:(w,h)"""
        if "file" in self.DATA.keys():
            img = Image.open(self.DATA.get('file'))
            red_img = ImageOps.fit(img, wh, method=5) \
            if self.HOR else ImageOps.pad(img, wh, method=5)
            self.HOR = not self.HOR
            img_tk = ImageTk.PhotoImage(red_img)
            self.DATA["img_tk"] = img_tk
            self.cv.itemconfigure(self.img_id, image=img_tk)
            # self.cv.image = img_tk

    def _getWH(self):
        self.update_idletasks()
        return self.winfo_width(), self.winfo_height()
    
    def fix(self, e=None):
        self._resizeImage(self._getWH())

    def _getGm(self):
        pass


if __name__ == '__main__':
    vn = tk.Tk()
    vn.geometry('400x220')
    wg = ViewerTkBasico(vn)
    wg.grid(row=0, column=0, sticky='wens')

    wg.setImage("frog.jpg")
    # wg.fix()

    vn.columnconfigure(0, weight=1)
    vn.rowconfigure(0, weight=1)
    vn.mainloop()