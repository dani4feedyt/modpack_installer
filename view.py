import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import re
from zipfile import ZipFile

class Window:
    root = TkinterDnD.Tk()

    d_path = tk.StringVar()
    d_modpath = tk.StringVar()
    back = "lightgray"
    front = "gray"

    minecraft_path = ""
    modpack_path = ""
    filename = ""

    default_d_path = f"C:/Users/{os.getlogin()}/AppData/Roaming/.minecraft/"

    canvas = None
    E_path = None
    E_modpath = None
    B_load = None
    B_setDefault = None
    B_setUp = None

    def start(self):
        self.d_path.set(self.default_d_path)

        self.root.title("Modpack Installer")
        self.root.configure(background=self.back)
        self.root.minsize(960, 480)
        self.root.maxsize(960, 480)
        self.root.geometry("300x300+50+50")

        self.canvas = tk.Canvas(self.root, width=960, height=480, background=self.back, borderwidth=0, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_rectangle((140, 90), (750, 430), fill=self.front)

        self.E_path = tk.Entry(self.root, width=100, borderwidth=5, textvariable=self.d_path)
        self.E_modpath = tk.Entry(self.root, width=100, borderwidth=5, textvariable=self.d_modpath)

        self.B_load = tk.Button(self.root, text="Load", command=self.load_push)
        self.B_setDefault = tk.Button(self.root, text="Set Default Path", command=self.set_default_push)
        self.B_setUp = tk.Button(self.root, text="Setup", command=self.set_up)

        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', self.handle_drop)

        self.B_load.place(x=760, y=50)
        self.B_setDefault.place(x=40, y=50)
        self.B_setUp.place(x=760, y=250)

        self.E_path.place(x=140, y=50)
        self.E_modpath.place(x=140, y=430)

        self.root.mainloop()

    def handle_drop(self, event):
        self.E_modpath.delete(0, len(self.d_modpath.get()))
        self.E_modpath.insert(tk.END, re.sub(r'[{}]', '', event.data))
        return event.action

    def load_push(self):
        user_path = self.d_path.get()
        self.minecraft_path = user_path
        mod_path = self.d_modpath.get()
        self.modpack_path = mod_path
        self.filename = os.path.basename(mod_path)
        print(self.filename)

    def set_default_push(self):
        self.d_path.set(self.default_d_path)

    def set_up(self):
        #os.replace(self.modpack_path, f"{self.minecraft_path}{self.filename}")
        if self.filename.endswith(".zip"):
            with ZipFile(self.modpack_path, 'r', metadata_encoding = "utf-8") as zObject:
                file_count = 0
                for file in zObject.namelist():
                    if file.startswith(('mods/', 'shaderpacks/', 'resourcepacks/', 'librarires/')):
                        file_count += 1
                        zObject.extract(file, path=self.minecraft_path)
                if file_count == 0:
                    print(f'Error, no modpack found in {self.filename}')
                else:
                    print(f'Modpack installed at {self.minecraft_path}')
            zObject.close()
        else:
            print("The file is not a zip file")
        return







