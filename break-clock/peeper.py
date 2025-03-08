#!/usr/bin/env python3

# import pathlib
import sys
import datetime
import collections
import logging

import psutil
import pygame


def main(hours_offest=None):
    tzinfo = datetime.timezone(datetime.timedelta(hours=hours_offest)) if hours_offest is not None else None
    cpu_color = (0, 80, 40)  # CPU usage color
    ram_color = (160, 0, 0), (90, 20, 10)  # RAM usage color
    bar_height = 4

    WIDTH = 400
    HEIGHT = 240
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), )  # pygame.NOFRAME
    pygame.display.set_caption('peeper')
    running = True

    pygame.mixer.init()
    if sys.platform == 'linux':
        logging.info('running on linux')
        sound = pygame.mixer.Sound('/usr/share/sounds/freedesktop/stereo/service-login.oga')
    else:
        sound = pygame.mixer.Sound('C:/Windows/Media/chimes.wav')

    main_colors = {'fg': [222, 222, 222], 'bg': [32, 32, 32], 'bgr': [222, 0, 0], }
    font = pygame.font.Font(None, 80)
    # font = pathlib.Path('/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf')
    # font = pygame.font.Font(font if font.exists() else None, 80)

    cpu_usage_queue = collections.deque(maxlen=20)
    i = 0
    state = 0
    clock = pygame.time.Clock()
    while running:
        i += 1
        # time.sleep(1)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_x]:
            logging.info('pressed x => quit')
            running = False
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info('window closed')
                running = False
                return
        # screen.blit()
        # no AA, no transparancy, normal
        dt = datetime.datetime.now(tzinfo)
        if dt.minute % 15 == 0 and state == 0:
            state = 1
            bg = main_colors['bgr']
            fg = main_colors['bg']
            sound.play()
        elif dt.minute % 15 != 0:
            state = 0
            bg = main_colors['bg']
            fg = main_colors['fg']

        screen.fill(bg)
        text = '{:02}:{:02}:{:02}'.format(dt.hour, dt.minute, dt.second)
        size = font.size(text)
        ren = font.render(text, 0, fg, bg)

        perwid = WIDTH / 100.0
        cpu_usage_queue.append(psutil.cpu_percent())
        cpu_usage = sum(cpu_usage_queue) / len(cpu_usage_queue)
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        ram_cached = ram.cached / ram.total * 100
        cpu_bar_width = cpu_usage * perwid
        pygame.draw.rect(screen, cpu_color, (0, HEIGHT - bar_height * 2, cpu_bar_width, bar_height))
        ram_bar_width = ram_usage * perwid, ram_cached * perwid
        pygame.draw.rect(screen, ram_color[0], (0, HEIGHT - bar_height * 1, ram_bar_width[0], bar_height))
        pygame.draw.rect(screen, ram_color[1], (ram_bar_width[0], HEIGHT - bar_height * 1, ram_bar_width[1], bar_height))
        screen.blit(ren, ((WIDTH - size[0]) // 2, (int(HEIGHT - size[1]) // 2)) )

        pygame.display.flip()
        clock.tick(10)
        # pygame.event.wait()
        # pygame.display.update()
    # time.sleep(1)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)
    try:
        main()
        logging.info('exiting normally')
    except Exception as e:
        logging.exception(e)
    finally:
        pygame.quit()
        exit()

