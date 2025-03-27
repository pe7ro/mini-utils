#!/usr/bin/env python3

import collections
import logging
import pathlib
import tkinter as tk
import datetime

import psutil
import pyglet
from pyglet.media.codecs.gstreamer import GStreamerDecoder


class PeeperApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Peeper')
        self.size = 400, 240
        self.root.geometry(f'{self.size[0]}x{self.size[1]}')
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.root.bind('x', lambda e: self.root.destroy())
        # see https://wiki.tcl-lang.org/page/wm+attributes
        # self.root.overrideredirect(True)  # Remove window decoration
        # self.root.attributes('-topmost', True)  # Always on top
        self.root.wm_attributes('-topmost', True)
        self.root.wm_attributes('-type', 'splash') # borderless but can have focus (to handle keyboard)
        # self.root.attributes('-transparentcolor', True)  # Optional: make the window transparent
        self.main_colors = ('#202020', '#dddddd', '#dd0000')
        self.bars_colors = ('#005533', '#aa0000', '#552211')
        self.bar_height = 5
        self.cpu_usage_queue = collections.deque(maxlen=20)
        self.i = 0
        self.state = -1
        class MyMediaDecoder(GStreamerDecoder):
            def get_file_extensions(self):
                return super().get_file_extensions() + ('.oga',)
        self.sound = pyglet.media.load('/usr/share/sounds/freedesktop/stereo/service-login.oga', streaming=False, decoder=MyMediaDecoder())
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.time_label = tk.Label(self.root, font=('FreeSans', 42, 'bold'), text="Centered Label", bg=self.root.cget("bg"))
        self.time_label.place(relx=0.5, rely=0.5, anchor="center")

        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<Button-1>', self.click)
        self.time_label.bind('<B1-Motion>', self.drag)
        self.time_label.bind('<Button-1>', self.click)

        self.update()


    def click(self, event):
        # print(event)
        x = event.x_root - self.size[0] // 2
        y = event.y_root - self.size[1] // 2
        self.root.geometry(f'{x:+}{y:+}')


    def drag(self, event):
        # print(event)
        x = event.x_root - self.size[0] // 2
        y = event.y_root - self.size[1] // 2
        self.root.geometry(f'{x:+}{y:+}')


    def update(self):
        dt = datetime.datetime.now()
        self.time_label['text'] = '{:02}:{:02}:{:02}'.format(dt.hour, dt.minute, dt.second)
        if dt.minute % 15 == 0:
            if self.state != 1:
                self.state = 1
                self.sound.play()
                self.canvas['bg'] = self.main_colors[2]
                self.time_label['bg'] = self.main_colors[2]
                self.time_label['fg'] = self.main_colors[0]
        else:
            if self.state != 0:
                self.state = 0
                self.canvas['bg'] = self.main_colors[0]
                self.time_label['bg'] = self.main_colors[0]
                self.time_label['fg'] = self.main_colors[1]

        perwid = self.canvas.winfo_width() / 100.0
        self.cpu_usage_queue.append(psutil.cpu_percent())
        cpu_usage = sum(self.cpu_usage_queue) / len(self.cpu_usage_queue)
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        ram_cached = ram.cached / ram.total * 100
        cpu_bar_width = cpu_usage * perwid
        ram_bar_width = ram_usage * perwid, ram_cached * perwid

        self.canvas.delete('all')
        self.canvas.create_rectangle(0, self.size[1] - self.bar_height * 2, cpu_bar_width, self.size[1] - self.bar_height, fill=self.bars_colors[0], width=0)
        self.canvas.create_rectangle(0, self.size[1] - self.bar_height, ram_bar_width[0], self.size[1], fill=self.bars_colors[1], width=0)
        self.canvas.create_rectangle(ram_bar_width[0], self.size[1] - self.bar_height, sum(ram_bar_width), self.size[1], fill=self.bars_colors[2], width=0)
        self.root.after(100, self.update)


def configure_logging(log_file=None, level=logging.INFO):
    # logging.basicConfig(filename='app.log', level=logging.INFO)
    if log_file is not None:
        handlers = [
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ]
    else:
        handlers = [
            logging.StreamHandler(),
        ]
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers,
    )
    logging.info('logging started: %s => %s', pathlib.Path(__file__).name, log_file)


if __name__ == "__main__":
    configure_logging(level=logging.INFO)
    root = tk.Tk()
    app = PeeperApp(root)
    root.mainloop()
