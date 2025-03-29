# Simple Break Clock with System Monitor

## Overview

Peeper is a simple Python application that displays a digital clock along with CPU and RAM usage bars. It also plays a sound every 15 minutes to remind the user of the time. The application is built using the Pygame library and is designed to run on both Linux and Windows.

## Variants

There are 3 implementations using different libraries, you can choose the one you prefer.

- pygame ⭐⭐⭐☆☆
  - cannot change the window position (dragging) and as a result it may be less convenient to move the window around
  - cannot set "always on top"
  - easiest audio support out of the box
- pyglet ⭐⭐⭐☆☆
  - reversed Y axis 
  - cpu usage seems to be the highest
  - smoothest window dragging out of 3
  - cannot set "always on top"
  - can play oga files wish some hacks (gstreamer) but does not see ffmpeg
- kivy ⭐⭐⭐☆☆
  - reversed Y axis 
  - the most confusing wiki and architecture
  - lowest cpu usage
  - window dragging can(?) be improved
  - needs absolute paths for fonts (?)
  - ESC closes the app by default but can be changed
  - freezes when given 'oga' file, but works ok if renamed to 'ogg'
- tkinter (pyglet for audio) ⭐⭐⭐⭐☆
  - surprisingly straightforward to implement (maybe lacking documentation though)
  - smooth dragging
  - low cpu usage
- pyqt5 ⭐⭐⭐⭐⭐
  - meaningful mature architecture
  - documentation mostly for C, but still quite helpful
  - lowest cpu and ram usage
  - smooth window dragging

## Features

- Digital clock display
- CPU and RAM (used + cached) usage bars
- Sound notification every 15 minutes
- Cross-platform support (Linux and Windows)

## Requirements

- Python 3.6 or higher
- Psutil library
- pygame / pyglet / kivy / pyqt5 library

## Installation

1. **Install Python**: Ensure you have Python 3.6 or higher installed on your system.

2. **Install Pygame and Psutil**:
   - Using pip:
     ```sh
     pip install pygame psutil
     ```

## Usage

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/peeper.git
   cd peeper
   ```

2. **Run the Application**:
   ```sh
   python3 peeper.py
   ```

3. **Optional: Set Timezone Offset**:
   You can set a timezone offset in hours by passing it as an argument:
   ```sh
   python3 peeper_pygame.py 2  # This will set the timezone to UTC+2
   ```

## Controls

- **X Key**: Press the 'x' key to exit the application.
- **Window Close Button**: Click the close button to exit the application.

## Configuration

- **Colors**:
  - CPU usage color: `(0, 80, 40)`
  - RAM usage color: `(160, 0, 0)` for used RAM, `(90, 20, 10)` for cached RAM
  - Background color: `(32, 32, 32)`
  - Foreground color: `(222, 222, 222)`
  - Background color for sound notification: `(222, 0, 0)`

- **Sound**:
  - On Linux, the sound file is located at `/usr/share/sounds/freedesktop/stereo/service-login.oga`.
  - On Windows, the sound file is located at `C:/Windows/Media/chimes.wav`.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.


---

Enjoy using Peeper! 🕐