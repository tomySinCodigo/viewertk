import typing
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from windnd import drop_files


class KViewer(tk.Canvas):
    def __init__(self, parent, *args, **kw):
        super(KViewer, self).__init__(master=parent, *args, **kw)
        self.parent = parent
        self._configKViewer()

    def _configKViewer(self):
        self.config(
            highlightthickness=0,
            border=0, borderwidth=0
        )
        self.FIT = True
        drop_files(self, func=self.onDrop)

    def setImage(self, file:str) -> None:
        """set image from file"""
        self.IMAGE = Image.open(file)
        self._setImage(self.IMAGE)

    def _setImage(self, image:Image, cnf:bool=False) -> None:
        """Set image(PIL:Image) to canvas"""
        wh = (self.winfo_width(), self.winfo_height())
        if wh == (0, 0):
            return
        img = ImageOps.fit(image, wh, method=2) \
        if self.FIT else ImageOps.pad(image, wh, method=2)
        self.imagetk = ImageTk.PhotoImage(image=img)
        if cnf: self.itemconfig(self.img_id, image=self.imagetk)
        else: self.img_id = self.create_image(0, 0, anchor='nw', image=self.imagetk)

    def onDrop(self, li:list) -> None:
        """on drop event show image file"""
        if not li: return
        file = li[0].decode('utf-8')
        ext = file.split('.')[-1].lower()
        if ext in ('jpg', 'jpeg', 'png', 'gif', 'bmp'):
            self.setImage(file)

    def getWH(self) -> tuple[int, int]:
        """get image width and height"""
        if hasattr(self, 'IMAGE'):
            return self.IMAGE.size
        return 0, 0
    
    def changeModeView(self, e=None) -> None:
        """change image view mode"""
        print('changeModeView')
        self.FIT = not self.FIT
        if hasattr(self, 'IMAGE'):
            self._setImage(self.IMAGE, cnf=True)


if __name__ == '__main__':
    vn = tk.Tk()
    vn.geometry('300x420')

    wg = KViewer(vn, bg='gray15')
    vn.bind('<Button-3>', wg.changeModeView)


    wg.grid(row=0, column=0, sticky='wens')
    vn.columnconfigure(0, weight=1)
    vn.rowconfigure(0, weight=1)
    vn.mainloop()