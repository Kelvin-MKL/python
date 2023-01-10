class Friend:
    def __init__(self, name, expense, row, col):
        self.name = name
        self.inner_label = "inner_frame_" + name
        self.outter_label = "outter_frame_" + name
        self.expense = float(expense)
        self.row, self.col = row, col
        self.btn_add_label = "btn_add_" + name
        self.btn_reset_label = "btn_reset_" + name
        self.check_box_label = "checkBox_label_" + name
        self.check_box_value = 0 # 1 = onvalue, 0 = offvalue
        self.disable_font_color = "light grey"
        self.active_font_color = "black"
        self.group_label = "group_" + name
        self.group_value = ""
        self.group_diff = 0

    def increase_expense(self, amount):
        try:
            self.expense += float(amount)
        except ValueError:
            print("value is not numeric type.")

    def reset(self):
        self.expense = 0.0

