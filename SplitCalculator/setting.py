import tkinter as tk
from tkinter import *
from friends import *
import json


class Setting:
    def __init__(self, config_file):
        self.sw = tk.Tk()
        self.sw.title = "Setting"
        self.config_file = config_file
        self.sw.geometry("600x450")
        self.json_data = None
        self.row = None
        self.col = None
        self.load_json_file()
        self.list_box_left = Listbox(self.sw, width=20)
        self.sv = StringVar(self.sw)

    def load_json_file(self):
        with open(self.config_file) as f:
            self.json_data = json.load(f)
            self.row = self.json_data["row"]
            self.col = self.json_data["col"]
        print("json data imported successfully.")
        print(self.json_data["namelist"], self.row, self.col)

    def show_ui(self):
        friend_label = tk.Label(self.sw, text="Friend list: ")
        friend_label.grid(row=0, column=0, padx=(20, 10), pady=10)


        self.list_box_left.grid(row=1, column=0, padx=(20, 10))
        list_name = [x for x in self.json_data['namelist']]
        print(list_name)
        for i in range(len(list_name)):
            self.list_box_left.insert(i+1, list_name[i])

        member_label = tk.Label(self.sw, text="Member: ")
        member_label.grid(row=0, column=20, padx=(20, 10), pady=10)
        list_box_right = Listbox(self.sw, width=20)
        list_box_right.grid(row=1, column=20)
        btn1 = tk.Button(self.sw, text="press", command=self.text1)
        btn1.grid(row= 2, column=5)
        n_label = tk.Label(self.sw, textvariable=self.sv)
        n_label.grid(row =3, column= 5)

    def text1(self):
        for i in self.list_box_left.curselection():
            self.sv.set(self.list_box_left.get(i))
            print(self.sv.get())



