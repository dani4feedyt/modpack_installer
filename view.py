import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import re
from zipfile import ZipFile
import shutil


def unzip(source, dist):
    filename = os.path.basename(source)
    if filename.endswith(".zip"):
        with ZipFile(source, 'r', metadata_encoding = "utf-8") as zObject:
            file_count = 0
            for file in zObject.namelist():
                if file.startswith(('mods/', 'shaderpacks/', 'resourcepacks/', 'libraries/')):
                    file_count += 1
                    zObject.extract(file, path=dist)
            if file_count == 0:
                print(f'Error, no modpack found in {filename}')
            else:
                print(f'Modpack installed at {source}')
        zObject.close()
    else:
        print("The file is not a zip file")
    return


class Window:
    root = TkinterDnD.Tk()

    d_path = tk.StringVar()
    d_modpath = tk.StringVar()
    back = "lightgray"
    front = "gray"

    minecraft_path = ""
    modpack_path = ""
    filename = ""
    modfolder_name = ""

    default_d_path = f"C:/Users/{os.getlogin()}/AppData/Roaming/.minecraft/"
    temp_path = "C:/Modpack Installer/Temp"

    canvas = None
    E_path = None
    E_modpath = None
    B_load = None
    B_setDefault = None
    B_setUp = None
    tempfolderlist = []

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

        self.B_load = tk.Button(self.root, text="Save", command=self.save_push)
        self.B_setDefault = tk.Button(self.root, text="Set Default Path", command=self.set_default_push)
        self.B_setUp = tk.Button(self.root, text="Setup", command=self.set_up)

        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', self.handle_drop)

        self.B_load.place(x=760, y=50)
        self.B_setDefault.place(x=40, y=50)
        self.B_setUp.place(x=760, y=250)

        self.E_path.place(x=140, y=50)
        self.E_modpath.place(x=140, y=430)

        base_y = 90
        b_id = 0
        for folder in os.listdir(self.temp_path):
            tag = os.fsdecode(folder)
            self.tempfolderlist.append(tag)
            if len(tag) >= 12:
                tag = tag[:12] + "..."
            button = tk.Button(self.root, name=str(b_id), text=tag, height=1, width=12)
            button.config(command=(lambda name=b_id: self.load_modpack(name)))
            button.place(x=40, y=base_y)
            base_y += 30
            b_id += 1

        self.root.mainloop()

    def handle_drop(self, event):
        self.E_modpath.delete(0, len(self.d_modpath.get()))
        self.E_modpath.insert(tk.END, re.sub(r'[{}]', '', event.data))
        return event.action

    def load_modpack(self, name):
        self.modfolder_name = self.tempfolderlist[int(name)]
        self.filename = os.listdir(f"{self.temp_path}/{self.modfolder_name}")[0]
        self.E_modpath.delete(0, len(self.E_modpath.get()))
        self.E_modpath.insert(tk.END, f"{self.temp_path}/{self.modfolder_name}/{self.filename}")

    def save_push(self):
        self.minecraft_path = self.d_path.get()
        self.modpack_path = self.d_modpath.get()
        self.filename = os.path.basename(self.modpack_path)
        self.modfolder_name = self.filename[:-3]
        modpack_temp_path = f"{self.temp_path}/{self.modfolder_name}"

        try:
            os.mkdir(modpack_temp_path)
        except FileExistsError:
            print(f"File already exists: {self.temp_path}.")
        try:
            shutil.copy(self.modpack_path, modpack_temp_path)
        except FileNotFoundError:
            print(f"File not found: {modpack_temp_path}")

    def set_default_push(self):
        self.d_path.set(self.default_d_path)

    def set_up(self):
        self.minecraft_path = self.d_path.get()
        print(self.minecraft_path)
        self.modpack_path = self.d_modpath.get()
        print(self.modpack_path)
        unzip(self.modpack_path, self.minecraft_path)






