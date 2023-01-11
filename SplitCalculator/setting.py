import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from friends import *
import json


class Setting(tk.Toplevel):
    def __init__(self, config_file):
        tk.Toplevel.__init__(self)
        self.title("Setting")
        self.config_file = config_file
        self.geometry("600x450")
        self.json_data = None
        self.row = None
        self.col = None
        self.load_json_file()
        self.member_list = StringVar(self)
        self.list = ""
        self.first_frame = LabelFrame(self, text="Friend List")
        self.sec_frame = LabelFrame(self, text="Edit")
        self.fd_list_combobox = ttk.Combobox(self.first_frame, values=[], width=15)
        self.edit_combobox = ttk.Combobox(self.sec_frame, values=[], width=15)
        self.v = StringVar(self)
        self.entry = Entry(self.sec_frame, width=60, textvariable=self.v)
        self.show_ui()
        self.grab_set()  # this instance will be focused until it is closed.
        tk.Tk.wait_window(self)  # tk.Tk() will be stopping running until this tk.Toplevel is destroyed.

    def load_json_file(self):
        with open(self.config_file) as f:
            self.json_data = json.load(f)
            self.row = self.json_data["row"]
            self.col = self.json_data["col"]
        print("json data imported successfully.")
        print("this is setting")

    def show_ui(self):
        self.list = [x for x in self.json_data['namelist']]
        self.first_frame.grid(row=0, column=0, padx=20, pady=20)
        self.fd_list_combobox.config(values=self.list)
        self.fd_list_combobox.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        btn_create = Button(self.first_frame, text="Create", bd=1, command=self.create_new_list)
        btn_create.grid(row=0, column=1, padx=(10, 0), sticky="e")
        btn_show = Button(self.first_frame, text="Show", bd=1, command=self.get_list_value)
        btn_show.grid(row=0, column=0, padx=(10, 0), sticky="e")
        btn_use_list = Button(self.first_frame, text="Select & close", bd=1, command=self.select_list)
        btn_use_list.grid(row=0, column=2, padx=(5, 0), sticky="w")
        fd_list_label = Label(self.first_frame, text="Member:", width=50)
        fd_list_label.grid(row=2, column=0, sticky=W, padx=(10, 20), columnspan=3)
        fd_list_value_label = Label(self.first_frame, textvariable=self.member_list)
        fd_list_value_label.grid(row=3, column=0, sticky="w", padx=20, pady=10, columnspan=4)
        self.sec_frame.grid(row=1, column=0, padx=20, pady=20)
        self.edit_combobox.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        self.edit_combobox.config(values=self.list)
        btn_show_2 = Button(self.sec_frame, text="Show", bd=1, command=self.show_edit_value)
        btn_show_2.grid(row=0, column=0, padx=(10, 10), sticky="e")
        btn_edit = Button(self.sec_frame, text="Save changing", bd=1, command=self.save_edit_list)
        btn_edit.grid(row=0, column=1, padx=(0, 30), sticky="e")
        fd_list_label_b = Label(self.sec_frame, text="Example: Alex, Warren, Tom ", width=50)
        fd_list_label_b.grid(row=1, column=0, sticky=W, padx=(10, 20), columnspan=3)
        self.entry.grid(row=2, column=0, padx=10, pady=10, columnspan=5)

    def get_list_value(self):
        try:
            a = self.fd_list_combobox.get()
            if len(self.json_data['namelist'][a]) > 1:
                e = ", ".join(self.json_data['namelist'][a])
            else:
                e = "None"
            self.member_list.set(e)
        except KeyError:
            tk.messagebox.showwarning(title=None, message="Please select a list.")

    def select_list(self):
        if self.fd_list_combobox.get() in self.json_data['namelist'].keys():
            self.json_data['on_use'] = self.fd_list_combobox.get()

            with open('config.json', 'w') as outfile:
                json.dump(self.json_data, outfile)
            print("Json file has been updated successfully.")
            self.destroy()
        else:
            tk.messagebox.showwarning(message="List non-exist.")

    def create_new_list(self):
        value = self.fd_list_combobox.get()
        if value in self.json_data['namelist'].keys():
            tk.messagebox.showinfo(message=value + " already exists")
        else:
            self.json_data['namelist'][value] = ["good"]
            print(value + " list is established!")
            with open('config.json', 'w') as outfile:
                json.dump(self.json_data, outfile)
            print("Json file has been updated successfully.")
            self.list = [x for x in self.json_data['namelist']]
            self.fd_list_combobox.config(values=self.list)
            self.edit_combobox.config(values=self.list)

    def show_edit_value(self):
        try:
            a = self.edit_combobox.get()
            if len(self.json_data['namelist'][a]) > 1:
                e = ", ".join(self.json_data['namelist'][a])
                self.v.set(e)
                self.entry.config(fg="black")
            else:
                holder = "Create your name list here.. follow the format above!"
                self.v.set(holder)
                self.entry.config(fg="grey")
        except KeyError:
            tk.messagebox.showwarning(title=None, message="Please select a list.")

    def save_edit_list(self):
        list_name = self.edit_combobox.get()
        list_value = self.entry.get()
        self.json_data['namelist'][list_name] = list_value.split(sep=", ")

        with open('config.json', 'w') as outfile:
            json.dump(self.json_data, outfile)
        print("Json file has been updated from edit frame.")
