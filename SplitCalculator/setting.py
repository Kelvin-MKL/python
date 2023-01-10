import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from friends import *
import json


class Setting:
    def __init__(self, config_file):
        self.sw = tk.Tk()
        self.sw.title("Setting")
        self.config_file = config_file
        self.sw.geometry("600x450")
        self.json_data = None
        self.row = None
        self.col = None
        self.load_json_file()
        self.list_box_left = Listbox(self.sw, width=20)
        self.member_list = StringVar(self.sw)
        self.list = ""
        self.first_frame = tk.LabelFrame(self.sw, text="Friend List")
        self.fd_list_combobox = ttk.Combobox(self.first_frame, values=[], width=18)

    def load_json_file(self):
        with open(self.config_file) as f:
            self.json_data = json.load(f)
            self.row = self.json_data["row"]
            self.col = self.json_data["col"]
        print("json data imported successfully.")
        print(self.json_data["namelist"], self.row, self.col)

    def show_ui(self):
        self.list = [x for x in self.json_data['namelist']]
        self.first_frame.grid(row=0, column=0, padx=20, pady=20)
        self.fd_list_combobox.config(values=self.list)
        self.fd_list_combobox.grid(row=0, column=0, sticky="w",padx=20, pady=20)
        btn_show = tk.Button(self.first_frame, text="Show", bd=1, command=self.get_list_value)
        btn_show.grid(row=0, column=1, padx=(20, 5))
        btn_use_list = tk.Button(self.first_frame, text="Select & close", bd=1, command=self.select_list)
        btn_use_list.grid(row=0, column=2, padx=(0, 5), sticky="w")

        fd_list_label = tk.Label(self.first_frame, text="Member:", width=50)
        fd_list_label.grid(row=2, column=0, sticky=W, padx=(10 ,20), columnspan=3)
        fd_list_value_label = tk.Label(self.first_frame, textvariable=self.member_list)
        fd_list_value_label.grid(row=3, column=0, sticky="w", padx=20, pady=10, columnspan=4)

    def get_list_value(self):
        try:
            a = self.fd_list_combobox.get()
            e = ", ".join(self.json_data['namelist'][a])
            self.member_list.set(e)
        except KeyError:
            tk.messagebox.showwarning(title=None, message="Please select a list.")

    def select_list(self):
        self.json_data['on_use'] = self.fd_list_combobox.get()
        print(self.json_data)

        with open('config.json', 'w') as outfile:
            json.dump(self.json_data, outfile)
        print("Json file has been updated successfully.")
        self.sw.destroy()

    def send_wid(self):
        a = self.sw.winfo_id()
        return a




