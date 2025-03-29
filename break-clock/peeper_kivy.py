#!/usr/bin/env python3
import collections
import datetime

import psutil
import kivy.graphics
import kivy.uix
import kivy.core.window
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import kivy.config
import kivy.core.audio.audio_gstplayer


class RectangleLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(RectangleLayout, self).__init__(**kwargs)

        self.cw = 1
        cpu_color = [x / 256 for x in [0, 80, 40, 256]]   # CPU usage color
        ram_color_1 = [x / 256 for x in [160, 0, 0, 256]]
        ram_color_2 = [x / 256 for x in [90, 20, 10, 256]]
        bar_height = 5
        with self.canvas:
            kivy.graphics.Color(*cpu_color)  # Red color
            self.cpu = kivy.graphics.Rectangle(pos=(0, bar_height),
                                             size=(kivy.core.window.Window.size[0] * 0.1, bar_height))
            kivy.graphics.Color(*ram_color_2)  # Red color
            self.memory_2 = kivy.graphics.Rectangle(pos=(0, 0),
                                             size=(kivy.core.window.Window.size[0] * 0.1, bar_height))
            kivy.graphics.Color(*ram_color_1)  # Red color
            self.memory_1 = kivy.graphics.Rectangle(pos=(0, 0),
                                             size=(kivy.core.window.Window.size[0] * 0.1, bar_height))
        self.kb = Window.request_keyboard(self._keyboard_closed, self)
        self.kb.bind(on_key_down=self.on_key_down)


    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None


    def on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 120:  # X key
            App.get_running_app().stop()


    def on_touch_move(self, touch):
        if touch.button == 'left' and self.collide_point(*touch.pos):
            Window.left += touch.x - Window.width / 2 - 2
            Window.top += Window.height / 2 - touch.y + 54
            # self.set_top(0)
            return True
        return super().on_touch_move(touch)


class RectangleApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ra = None
        self.cpu_usage_queue = collections.deque(maxlen=20)
        self.fg = (.875, .875, .875)
        self.bg = (.125, .125, .125)
        self.bgr = (.875, 0, 0)
        self.state = -1
        self.sound = None
        self.time_label = None

    def build(self):
        ws = (400, 240)
        kivy.core.window.Window.size = ws
        kivy.core.window.Window.minimum_width = ws[0]  # Set the minimum width
        kivy.core.window.Window.maximum_width = ws[0]  # Set the maximum width
        kivy.core.window.Window.minimum_height = ws[1]  # Set the minimum height
        kivy.core.window.Window.maximum_height = ws[1]  # Set the maximum height
        kivy.core.window.Window.resizable = False
        kivy.core.window.Window.borderless = True
        # kivy.core.window.Window.title = 'peeper_kivy'
        self.title = 'peeper_kivy'
        self.resizable = False
        kivy.core.window.Window.always_on_top = True
        self.ra = RectangleLayout()
        Clock.schedule_interval(self.update, 0.1)
        self.time_label = Label(
            color=self.fg,
            text="xxx",
            font_size=54,
            font_name='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf',
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.ra.add_widget(self.time_label)
        self.sound = kivy.core.audio.audio_gstplayer.SoundGstplayer(source='/usr/share/sounds/freedesktop/stereo/service-login.oga')
        return self.ra


    def update(self, dt):
        dt = datetime.datetime.now()
        self.time_label.text = "{:02}:{:02}:{:02}".format(dt.hour, dt.minute, dt.second)

        perwid = kivy.core.window.Window.size[0] / 100.0
        self.cpu_usage_queue.append(psutil.cpu_percent())
        cpu_usage = sum(self.cpu_usage_queue) / len(self.cpu_usage_queue)
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        ram_cached = ram.cached / ram.total * 100
        cpu_bar_width = cpu_usage * perwid
        ram_bar_width = ram_usage * perwid, ram_cached * perwid
        self.ra.cw = ram_bar_width
        self.ra.cpu.size = [cpu_bar_width, 5]
        self.ra.memory_1.size = [ram_bar_width[0], 5]
        self.ra.memory_2.size = [sum(ram_bar_width), 5]

        if dt.minute % 15 == 0:
            if self.state != 1:
                self.state = 1
                Window.clearcolor = self.bgr
                self.time_label.color = self.bg
                self.sound.play()
        else:
            if self.state != 0:
                self.state = 0
                Window.clearcolor = self.bg
                self.time_label.color = self.fg
                # self.sound.play()



if __name__ == "__main__":
    kivy.config.Config.set('kivy', 'exit_on_escape', '0')
    # kivy.config.Config.set('graphics', 'maxfps', '10')
    RectangleApp().run()
