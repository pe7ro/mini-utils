#!/usr/bin/env python3

import sys
import datetime
import collections
import logging

import psutil
import pyglet
from pyglet.media.codecs.gstreamer import GStreamerDecoder


def main(hours_offest=None):
    tzinfo = datetime.timezone(datetime.timedelta(hours=hours_offest)) if hours_offest is not None else None
    cpu_color = (0, 80, 40, 255)  # CPU usage color
    ram_color = (160, 0, 0, 255), (90, 20, 10, 255)  # RAM usage color
    bar_height = 5

    WIDTH = 400
    HEIGHT = 240
    window = pyglet.window.Window(width=WIDTH, height=HEIGHT, style=pyglet.window.Window.WINDOW_STYLE_OVERLAY)
    # if sys.platform == 'win':
    #     window = pyglet.window.Window(width=WIDTH, height=HEIGHT, style=pyglet.window.Window.WINDOW_STYLE_OVERLAY)
    # else:
    #     window = pyglet.window.Window(width=WIDTH, height=HEIGHT, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
    window.set_caption('peeper_pyglet')
    # window.set_minimum_size(WIDTH, HEIGHT), window.set_maximum_size()
    main_colors = {'fg': (222, 222, 222, 255), 'bg': (32, 32, 32, 255), 'bgr': (222, 0, 0, 255), }
    cpu_usage_queue = collections.deque(maxlen=20)
    colors = main_colors['bg'], main_colors['fg']
    # player = pyglet.media.Player()
    state = -1
    dt = datetime.datetime.now(tzinfo)
    clock = pyglet.clock.get_default()

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        wl = window.get_location()
        window.set_location(wl[0] + x - window.size[0] // 2, wl[1] - y  + window.size[1] // 2)

    @window.event
    def on_draw():
        nonlocal dt, colors

        perwid = WIDTH / 100.0
        cpu_usage_queue.append(psutil.cpu_percent())
        cpu_usage = sum(cpu_usage_queue) / len(cpu_usage_queue)
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        ram_cached = ram.cached / ram.total * 100
        cpu_bar_width = cpu_usage * perwid
        ram_bar_width = ram_usage * perwid, ram_cached * perwid

        window.clear()
        batch = pyglet.graphics.Batch()
        rect1 = pyglet.shapes.Rectangle(0, 0, WIDTH, HEIGHT, color=colors[0], batch=batch)
        rect2 = pyglet.shapes.Rectangle(0, bar_height, cpu_bar_width, bar_height, cpu_color, batch=batch)
        rect3 = pyglet.shapes.Rectangle(0, 0, ram_bar_width[0], bar_height, ram_color[0], batch=batch)
        rect4 = pyglet.shapes.Rectangle(ram_bar_width[0], 0, ram_bar_width[1], bar_height, ram_color[1], batch=batch)
        text = '{:02}:{:02}:{:02}'.format(dt.hour, dt.minute, dt.second)
        label = pyglet.text.Label(text, font_name='Freesans', bold=True, font_size=40, x=WIDTH//2, y=HEIGHT//2,
                                  anchor_x='center', anchor_y='center', color=colors[1], batch=batch)
        batch.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.X:
            logging.info('pressed x => quit')
            pyglet.app.exit()

    if sys.platform == 'linux':
        logging.info('running on linux')
        if pyglet.media.have_ffmpeg():
            logging.info('with ffmpeg')
            sound = pyglet.media.load('/usr/share/sounds/freedesktop/stereo/service-login.oga', streaming=False)
        else:
            logging.info('no ffmpeg')
            class MyMediaDecoder(GStreamerDecoder):
                def get_file_extensions(self):
                    return super().get_file_extensions() + ('.oga', )

            # sound = pyglet.media.load('/usr/share/sounds/sound-icons/cockchafer-gentleman-1.wav', streaming=False)
            sound = pyglet.media.load('/usr/share/sounds/freedesktop/stereo/service-login.oga', streaming=False, decoder=MyMediaDecoder())
    else:
        sound = pyglet.media.load('C:/Windows/Media/chimes.wav', streaming=False)

    def update(delta):
        # print(delta)
        nonlocal state, colors, dt
        # i += 1
        dt = datetime.datetime.now(tzinfo)
        if dt.minute % 15 == 0:
            if state != 1:
                state = 1
                sound.play()
                colors = main_colors['bgr'], main_colors['bg']
        else:
            if state != 0:
                state = 0
                # sound.play()
                colors = main_colors['bg'], main_colors['fg']

    clock.schedule_interval(update, 0.1)
    # clock.schedule(update)
    pyglet.app.run(0.1)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)
    pyglet.options['search_local_libs'] = True
    try:
        main()
        logging.info('exiting normally')
    except Exception as e:
        logging.exception(e)
    finally:
        pyglet.app.exit()
        exit()

