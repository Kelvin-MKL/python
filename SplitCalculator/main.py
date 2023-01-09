import tkinter as tk
from tkinter import ttk
from friends import *
import json
from win32gui import GetWindowRect



class App:
    def __init__(self, friend, config_file):
        self.window = tk.Tk()
        self.window.title("Easy Split")
        self.frame = tk.Frame(self.window)
        self.frame.pack()
        self.friend = friend  # Friend class
        self.config_file = config_file  # config json file
        self.json_data = None
        self.friend_list = []
        self.row = None  # will be set according to config file -> grid row
        self.col = None  # will be set according to config file -> grid col
        self.expense_label = tk.Label(self.frame, text="$")
        self.expense_entry = tk.Entry(self.frame)
        self.total_expense_label = tk.Label(self.frame, text="Total expense $0")
        self.number_of_people_sharing_label = tk.Label(self.frame, text="People sharing 0")
        self.number_of_people_participated = 0
        self.combobox_value = ["a", "b", "c", "d", "e", "f"]
        self.group_expense_dict = {}
        self.average = 0

    def load_json_file(self):
        with open(self.config_file) as f:
            self.json_data = json.load(f)
            self.row = self.json_data["row"]
            self.col = self.json_data["col"]
        print("json data imported successfully.")
        print(self.json_data["name"], self.row, self.col)

    def create_friend_list_obj(self):
        initial_expense = 0
        i = 0
        try:
            for r in range(self.row):
                for c in range(self.col):
                    self.friend_list.append(Friend(self.json_data["name"][i], initial_expense, r, c))
                    i += 1
        except IndexError:
            print("It is ok, name list is not long enough to match with row & col")
        print("Friend list object created successfully.")
        # for h in self.friend_list:
        #     print(h.name, h.row, h.col)

    def create_form(self):
        fl = self.friend_list
        for index in range(len(self.friend_list)):
            font_color = self.check_font_color(index)
            fl[index].outter_label = tk.LabelFrame(self.frame, text=fl[index].name, fg=font_color)
            fl[index].outter_label.grid(row=fl[index].row, column=fl[index].col, padx=20, pady=20)
            fl[index].inner_label = tk.Label(fl[index].outter_label, text="Current expense $" + str(fl[index].expense),
                                             fg=font_color)
            fl[index].inner_label.grid(row=0, column=0, padx=20)
            fl[index].btn_add_label = tk.Button(fl[index].outter_label, text="Add", fg=font_color,
                                                command=lambda i=index: [fl[i].increase_expense(
                                                    float(self.expense_entry.get())),
                                                    self.update_ui(update_cmd="expense_label", index=i),
                                                    self.total_expense_cal()])
            fl[index].btn_add_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            fl[index].btn_reset_label = tk.Button(fl[index].outter_label, text="Reset", fg=font_color,
                                                  command=lambda i=index: [fl[i].reset(),
                                                                           self.update_ui(update_cmd="expense_label",
                                                                                          index=i)])
            fl[index].btn_reset_label.grid(row=1, column=0, pady=5)
            checkbox = tk.Checkbutton(fl[index].outter_label, text="Join",
                                      variable=fl[index].check_box_label, onvalue=1,
                                      offvalue=fl[index].check_box_value,
                                      command=lambda i=index: [self.toggle_check_box(i),
                                                               self.update_ui(update_cmd="update_all", index=i)])
            checkbox.grid(row=1, column=0, padx=5, pady=5, sticky="e")
            combo_box_label = tk.Label(fl[index].outter_label, text="Group")
            combo_box_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
            fl[index].group_label = ttk.Combobox(fl[index].outter_label, values=self.combobox_value, width=2)
            fl[index].group_label.grid(row=4, column=0)

        self.expense_label.grid(row=fl[-1].row + 1, column=0, sticky="w", padx=15, pady=10)
        self.expense_entry.grid(row=fl[-1].row + 1, column=0, padx=10, pady=10)
        self.expense_entry.select_range(0, 5)
        button_reset_all = tk.Button(self.frame, text="Reset All",
                                     command=lambda i=len(fl): [[fl[x].reset() for x in range(i)],
                                        [self.update_ui(update_cmd="update_all", index=j) for j in range(i)]])
        button_reset_all.grid(row=fl[-1].row + 1, column=3, pady=10, padx=5, sticky="w")
        button_finalise = tk.Button(self.frame, text="Finalise", command=self.finalise)
        button_finalise.grid(row=fl[-1].row + 1, column=2, pady=10, padx=5, sticky="e")
        self.total_expense_label.grid(row=fl[-1].row + 1, column=1, pady=10, padx=5)
        self.number_of_people_sharing_label.grid(row=fl[-1].row + 1, column=2, sticky="w", pady=10, padx=5)

    def finalise(self):
        new_window = tk.Tk()
        new_window.geometry("600x450")
        new_window.title("Result")

        total = self.total_expense_cal()
        self.average = round(total / self.number_of_people_participated, 1)
        self.get_combobox_value()
        name_title_label = tk.Label(new_window, text="Name", font='Helvetica 13 underline')
        name_title_label.grid(row=0, column=0, sticky="w", padx=20)
        amount_title_label = tk.Label(new_window, text="Paid", font='Helvetica 13 underline')
        amount_title_label.grid(row=0, column=1, sticky="e")
        average_title_label = tk.Label(new_window, text="Average", font='Helvetica 13 underline')
        average_title_label.grid(row=0, column=3, sticky="e")
        credit_or_liability_label = tk.Label(new_window, text=" + / - ", font='Helvetica 13 underline')
        credit_or_liability_label.grid(row=0, column=4, sticky="e")
        btn_save = tk.Button(new_window, text="Save file", command=self.save_file)
        btn_save.grid(row=0, column=6, sticky="e", padx=10, pady=5, columnspan=3)

        row, col, p = 1, 0, 0
        for ppl in self.friend_list:
            if ppl.check_box_value == 1:
                diff = float(ppl.expense - self.average)
                if diff > 0.1:
                    font_color = "green"
                else:
                    font_color = "red"

                name_label = tk.Label(new_window, text=ppl.name)
                name_label.grid(row=row, column=col, sticky="w", padx=20)
                amount_label = tk.Label(new_window, text="$"+str(round(float(ppl.expense), 1)))
                amount_label.grid(row=row, column=col+1, sticky="e")
                average_label = tk.Label(new_window, text="$"+str(round(float(self.average), 1)))
                average_label.grid(row=row, column=col+3, sticky="e", padx=10)
                diff_label = tk.Label(new_window, text=str(round(float(diff), 1)), fg=font_color)
                diff_label.grid(row=row, column=col+4, sticky="e")
                row += 1
                p += 1

        total_label = tk.Label(new_window, text="Total expense: ")
        total_label.grid(row=row+3, column=col, padx=20, sticky="w")
        total_cost_label = tk.Label(new_window, text="$"+str(float(total)))
        total_cost_label.grid(row=row+3, column=col+1, sticky="e")
        separate_label = tk.Label(new_window, text=str("*"*60))
        separate_label.grid(row=row+4, column=0, columnspan=10)

        for i in self.group_expense_dict:
            if i != "":
                if self.group_expense_dict[i][1] > 0.1:
                    font_color = "green"
                else:
                    font_color = "red"
                group_label = tk.Label(new_window, text=str(self.group_expense_dict[i][0]))
                group_label.grid(row=row+5, column=0, sticky="w", padx=20, columnspan=3)
                group_expense_label = tk.Label(new_window, text=str(self.group_expense_dict[i][1]), fg=font_color)
                group_expense_label.grid(row=row+5, column=col+4, sticky="e")
                print(self.group_expense_dict[i][0], self.group_expense_dict[i][1])
                row += 1
        print("Total expenditure: " + str(total))

    def save_file(self):
        print(self.window.winfo_id())

    def toggle_check_box(self, index):
        fl = self.friend_list
        if fl[index].check_box_value == 0:
            fl[index].check_box_value = 1
            self.number_of_people_participated += 1
        else:
            fl[index].check_box_value = 0
            self.number_of_people_participated += -1
        # print(fl[index].check_box_label, fl[index].check_box_value)

    def check_font_color(self, index):
        fl = self.friend_list
        if fl[index].check_box_value == 0:
            font = fl[index].disable_font_color
        else:
            font = fl[index].active_font_color
        return font

    def update_ui(self, **update_section):
        if update_section.get('update_cmd') == "update_all":
            fl = self.friend_list
            index = update_section.get('index')
            font_color = self.check_font_color(index)
            fl[index].inner_label.configure(text="Current expense $" + str(fl[index].expense))
            fl[index].inner_label.config(fg=font_color)
            fl[index].outter_label.config(fg=font_color)
            fl[index].btn_add_label.config(fg=font_color)
            fl[index].btn_reset_label.config(fg=font_color)
            self.expense_entry.select_range(0, len(self.expense_entry.get()))
            t = self.total_expense_cal()
            self.total_expense_label.configure(text="Total expense $" + str(t))
            self.number_of_people_sharing_label.configure(text="People sharing " +
                                                               str(self.number_of_people_participated))
        elif update_section.get('update_cmd') == "expense_label":
            fl = self.friend_list
            index = update_section.get('index')
            fl[index].inner_label.configure(text="Current expense $" + str(fl[index].expense))
            t = self.total_expense_cal()
            self.total_expense_label.configure(text="Total expense $" + str(t))
            self.expense_entry.select_range(0, len(self.expense_entry.get()))

    def total_expense_cal(self):
        x = 0
        for i in self.friend_list:
            if i.check_box_value == 1:
                x += i.expense
        return x

    def get_combobox_value(self):
        self.group_expense_dict = {}
        d = self.group_expense_dict
        extra = "i"
        for i in self.friend_list:
            if i.check_box_value == 1:
                m = i.group_label.get()
                i.group_value = m  # eg.'a', 'b'
                if m != "":
                    try:
                        if d[m][0] == "":
                            raise KeyError
                        d[m] = (d[m][0] + " & " + str(i.name), round(float(d[m][1] + i.expense - self.average), 1))
                    except KeyError:
                        d[m] = (i.name, round(float(i.expense - self.average), 1))
                else:
                    d[extra] = (i.name, round(float(i.expense - self.average), 1))
                    extra += "i"

        print(d)


if __name__ == '__main__':
    new_app = App(Friend, 'config.json')
    new_app.load_json_file()
    new_app.create_friend_list_obj()
    new_app.create_form()
    new_app.window.mainloop()


