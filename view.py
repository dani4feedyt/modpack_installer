import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from screeninfo import get_monitors
import os
import re
from zipfile import ZipFile
import shutil
import webbrowser


def unzip(source, dist):
    filename = os.path.basename(source)
    errflag = False
    response = None

    if filename.endswith(".zip"):
        try:
            with ZipFile(source, 'r', metadata_encoding="utf-8") as zObject:
                file_count = 0
                for file in zObject.namelist():
                    if file.startswith(('mods/', 'shaderpacks/', 'resourcepacks/', 'libraries/', 'config/')):
                        file_count += 1
                        zObject.extract(file, path=dist)
                if file_count == 0:
                    response = f'No modpack found in {filename}'
                    errflag = True

            zObject.close()
        except FileNotFoundError:
            errflag = True
            response = f'File not found: {filename}'
    else:
        response = "Selected file is not a zip file."
        errflag = True
    return response, errflag


def check_for_input(entry):
    if entry.endswith((".zip", ".rar")):
        if any(i in entry for i in [':\\', ':/']):
            if len(entry) >= 7:
                return True
    return False


class Window:
    root = TkinterDnD.Tk()

    d_path = tk.StringVar()
    d_modpath = tk.StringVar()

    root_with = 960
    root_height = 480
    back = "lightgray"
    front = "gray"

    minecraft_path = ""
    modpack_path = ""
    filename = ""
    modfolder_name = ""

    default_d_path = f"C:/Users/{os.getlogin()}/AppData/Roaming/.minecraft/"
    temp_path = "C:/Modpack Installer/Temp"

    canvas = None
    L_error = None
    L_info = None
    E_path = None
    E_modpath = None
    B_save = None
    B_setDefault = None
    B_openFolder = None
    B_setUp = None
    is_admin = False

    btn_list = []
    tempfolderlist = []

    def start(self):
        self.d_path.set(self.default_d_path)
        self.minecraft_path = self.default_d_path

        self.root.title("Modpack Installer 0.6.6.1")
        self.root.iconbitmap("src/image.ico")
        self.root.configure(background=self.back)
        self.root.bind("<Key>", self.key_callback)
        self.root.minsize(self.root_with, self.root_height)
        self.root.maxsize(self.root_with, self.root_height)
        self.root.geometry(f"{self.root_with}x{self.root_height}+{(get_monitors()[0].width - self.root_with) // 2}+{(get_monitors()[0].height - self.root_height) // 2}")

        # self.root.geometry("300x300+50+50")

        self.canvas = tk.Canvas(self.root, width=self.root_with, height=self.root_height, background=self.back, borderwidth=0, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_rectangle((140, 90), (750, 430), fill=self.front)

        self.canvas.bind("<Button-1>", self.root_focus)

        self.L_error = tk.Label(self.root, background=self.back, fg="Red", font="Arial 15 bold")
        self.L_info = tk.Label(self.root, background=self.back, fg="Blue", font="Arial 15 bold")

        self.E_path = tk.Entry(self.root, width=100, borderwidth=5, textvariable=self.d_path)
        self.E_modpath = tk.Entry(self.root, width=100, borderwidth=5, textvariable=self.d_modpath, fg='Grey')

        self.E_path.bind("<FocusIn>", lambda args: self.focus_in_entry_box(self.E_path))
        self.E_path.bind("<FocusOut>", lambda args: self.focus_out_entry_box(self.E_path, 'Enter .minecraft folder path'))

        self.d_modpath.set('Enter modpack archive path')

        self.E_modpath.bind("<FocusIn>", lambda args: self.focus_in_entry_box(self.E_modpath))
        self.E_modpath.bind("<FocusOut>", lambda args: self.focus_out_entry_box(self.E_modpath, 'Enter modpack archive path'))

        self.B_save = tk.Button(self.root, text="Save", command=self.save_push)
        self.B_setDefault = tk.Button(self.root, text="Set Default Path", command=self.set_default_push)
        self.folder_image = tk.PhotoImage(width=1, height=7)
        self.B_openFolder = tk.Button(self.root, width=20, height=18, text='🗀', image=self.folder_image, compound="bottom", font='Helvetica 18 bold', command=self.open_folder)##for garbage collector folder_image defined as attribute
        self.B_setUp = tk.Button(self.root, text="Setup", command=self.set_up)

        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', self.handle_drop)

        self.B_save.place(x=760, y=50)
        self.B_setDefault.place(x=40, y=50)
        self.B_openFolder.place(x=800, y=50)
        self.B_setUp.place(x=760, y=250)

        self.E_path.place(x=140, y=50)
        self.E_modpath.place(x=140, y=440)

        self.buttons_place()

        if self.is_admin:
            self.root.lower()
            tk.messagebox.showwarning("Warning", "Program is opened in adminisrator mode. Some features may not work properly. Please restart in non-admin mode.")
            self.is_admin = False
            self.root.focus_set()

        def filechange_monitor():
            self.d_path.set(self.d_path.get().replace('\\', '/'))
            self.d_modpath.set(self.d_modpath.get().replace('\\', '/'))
            if len(os.listdir(self.temp_path)) != len(self.tempfolderlist):
                self.buttons_place()
            self.root.after(1000, filechange_monitor)

        self.root.after(1000, filechange_monitor)
        self.root.mainloop()

    def key_callback(self, key):
        if key.state & 4 > 0 and key.keysym == "??":
            if chr(key.keycode) == 'V':
                self.root.focus_get().event_generate("<<Paste>>")
            elif chr(key.keycode) == 'C':
                self.root.focus_get().event_generate("<<Copy>>")
            elif chr(key.keycode) == 'X':
                self.root.focus_get().event_generate("<<Cut>>")
            elif chr(key.keycode) == 'A':
                self.root.focus_get().event_generate("<<SelectAll>>")

    def root_focus(self, event):
        # x, y = self.root.winfo_pointerxy()
        # print(x, y)
        # widget = self.root.winfo_containing(x, y)
        # print(widget)

        self.root.focus()

    def focus_out_entry_box(self, entry, widget_text):
        if len(entry.get()) == 0:
            entry.delete(0, tk.END)
            entry['fg'] = 'Grey'
            entry.insert(0, widget_text)

    def focus_in_entry_box(self, entry):
        if entry['fg'] == 'Grey':
            entry['fg'] = 'Black'
            entry.delete(0, tk.END)

    def buttons_place(self):
        for btn in self.btn_list:
            btn.destroy()
            self.tempfolderlist.clear()
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
            self.btn_list.append(button)
            base_y += 30
            b_id += 1

    def handle_drop(self, event):
        self.L_error.place_forget()
        self.L_info.place_forget()

        self.E_modpath.delete(0, len(self.d_modpath.get()))
        self.E_modpath['fg'] = 'Black'
        self.E_modpath.insert(tk.END, re.sub(r'[{}]', '', event.data))
        return event.action

    def load_modpack(self, name):
        self.L_error.place_forget()
        self.L_info.place_forget()

        self.modfolder_name = self.tempfolderlist[int(name)]
        try:
            self.filename = os.listdir(f"{self.temp_path}/{self.modfolder_name}")[0]
            self.E_modpath.delete(0, len(self.E_modpath.get()))
            self.E_modpath['fg'] = 'Black'
            self.E_modpath.insert(tk.END, f"{self.temp_path}/{self.modfolder_name}/{self.filename}")
        except IndexError:
            self.L_info.place_forget()
            self.L_error.config(text="Error. Folder is empty")
            self.L_error.place(x=40, y=15)

    def open_folder(self):
        self.L_error.place_forget()
        self.L_info.place_forget()

        self.minecraft_path = self.d_path.get()
        webbrowser.open(os.path.realpath(self.minecraft_path))

    def save_push(self):
        self.L_error.place_forget()
        self.L_info.place_forget()

        self.L_info.config(text="Saving the modpack to the temp folder...")
        self.L_info.place(x=40, y=15)

        self.root.update()

        if check_for_input(self.d_modpath.get()):
            self.minecraft_path = self.d_path.get()
            self.modpack_path = self.d_modpath.get()
            self.filename = os.path.basename(self.modpack_path)
            self.modfolder_name = self.filename[:-3]
            modpack_temp_path = f"{self.temp_path}/{self.modfolder_name}"

            try:
                os.mkdir(modpack_temp_path)
            except FileExistsError:
                self.L_info.place_forget()
                self.L_error.config(text=f"Error. File already saved: {modpack_temp_path}")
                self.L_error.place(x=40, y=15)
            else:
                try:
                    shutil.copy(self.modpack_path, modpack_temp_path)
                except FileNotFoundError:
                    self.L_info.place_forget()
                    self.L_error.config(text=f"Error. File not found: {self.modpack_path}")
                    self.L_error.place(x=40, y=15)
                    os.rmdir(modpack_temp_path)
                except shutil.SameFileError:
                    self.L_info.place_forget()
                    self.L_error.config(text=f"Error. Same file: {self.modpack_path}")
                    self.L_error.place(x=40, y=15)
                    os.rmdir(modpack_temp_path)
                else:
                    self.L_info.config(text="Modpack has been saved successfully.")
                    self.L_info.place(x=40, y=15)
        else:
            self.L_info.place_forget()
            self.L_error.config(text="Error. Invalid modpack path.")
            self.L_error.place(x=40, y=15)

        self.buttons_place()

    def set_default_push(self):
        self.L_error.place_forget()
        self.L_info.place_forget()

        self.E_path['fg'] = 'Black'
        self.d_path.set(self.default_d_path)

    def set_up(self):
        self.L_error.place_forget()
        self.L_info.place_forget()

        self.L_info.config(text="Setting up the modpack...")
        self.L_info.place(x=40, y=15)

        self.root.update()

        if check_for_input(self.d_modpath.get()):

            self.minecraft_path = self.d_path.get()
            self.modpack_path = self.d_modpath.get()

            unzipped_resp = unzip(self.modpack_path, self.minecraft_path)

            if unzipped_resp[1] is True:
                self.L_info.place_forget()
                self.L_error.config(text=f"Error. {unzipped_resp[0]}")
                self.L_error.place(x=40, y=15)

            else:
                self.L_info.config(text=f"Modpack successfully istalled at: {self.minecraft_path}.")
                self.L_info.place(x=40, y=15)
        else:
            self.L_info.place_forget()
            self.L_error.config(text="Error. Invalid modpack path.")
            self.L_error.place(x=40, y=15)








