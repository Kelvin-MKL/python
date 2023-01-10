from win32gui import GetWindowRect
from PIL import ImageGrab
from datetime import date


class Screenshot:
    def __init__(self, window_id, file_path):
        self.canvas = GetWindowRect(window_id)
        self.ig = ImageGrab.grab(self.canvas)
        self.file_path = file_path
        self.file_name = self.get_file_name()

    def get_file_name(self):
        today = date.today()
        file_name = "Receipt_" + today.strftime("%b_%d_%Y") + '.png'
        print(file_name)
        return file_name

    def save(self):
        fp = self.file_path
        self.ig.save(fp + "/" + self.file_name, format='png')
