#!/usr/bin/python

import sys
import requests as req
from collections import deque
from dataclasses import dataclass, asdict
from time import sleep
from evdev import InputDevice, list_devices, ecodes, categorize

CODE_MAP_CHAR = {
    'KEY_PAGEDOWN': 'Page Down',
    'KEY_PAGEUP': 'Page Up',
    'KEY_ESC': 'Escape',
    'KEY_B': 'B',
    'KEY_LEFTSHIFT': 'Left shift',
    'KEY_F5': 'F5',
}

PLAYLIST = (
    'start',
    'heia',
    'fireAriaStart',
    'fireAriaWings',
    'fireAriaEnd',
    'anotherSong',
    'end',
    )

# Data class for light settings
@dataclass
class LEDPreset:
    palette: int = 200
    primary_pattern: int = 0
    primary_scale: float = 1
    primary_speed: float = 0.05
    secondary_pattern: int = 0
    secondary_scale: float = 1
    secondary_speed: float = 0.05
    # brightness: float = 1.0
    # color_temp: int = 6000
    # gamma: float = 1.0
    # saturation: float = 1.0

    def apply(self):
        for k, v in asdict(self).items():
            send_request(k, v)


# Pattern library
patterns = {
        "Static Color": 0,
        "Static Gradient 1D": 1,
        "Palette Waves 1D": 150,
        "Palette Plasma 2D": 170,
        "Palette Twinkle 1D": 190,
        "Fade in": 1633213622116,
        "Fade out": 1633036792965,
        "Wipe in": 1633213463693,
        "Blackout": 1633910057112,
        "Blackbody pulse from center": 1634079287296,
        "Wipe out from center": 1634080813116
        }

palettes = {
        "Sunset Light": 0,
        "Fire": 150,
        "Golden Hour": 160,
        "Ocean": 170,
        "Sky Blue": 190,
        "Purple": 200,
        "Hot Pink": 210
        }


def parse_key_to_char(val):
    return CODE_MAP_CHAR[val] if val in CODE_MAP_CHAR else val + " not found"

def send_request(key, value):
    return req.get('http://localhost/setparam?key={}&value={}'.format(key, value))

def start():
    send_request("primary_pattern", patterns["Blackout"])
    send_request("primary_speed", "1")
    send_request("palette", palettes["Sunset Light"])
    sleep(1)
    send_request("primary_pattern", patterns["Static Color"])
    sleep(1)
    send_request("primary_pattern", patterns["Blackout"])
    sleep(1)
    send_request("primary_pattern", patterns["Static Color"])
    sleep(1)
    send_request("primary_pattern", patterns["Blackout"])
    sleep(1)
    send_request("primary_pattern", patterns["Static Color"])
    sleep(1)
    send_request("primary_pattern", patterns["Blackout"])
    return

def heia():
    preset = LEDPreset(palettes["Sky Blue"], patterns["Fade in"])
    preset.apply()
    # send_request("palette", palettes["Sky Blue"])
    # send_request("primary_pattern", patterns["Fade in"])
    sleep(3)
    preset.primary_pattern = patterns["Palette Plasma 2D"]
    preset.apply()
    # send_request("primary_pattern", patterns["Palette Plasma 2D"])

def fireAriaStart():
    send_request("palette", palettes["Fire"])
    send_request("primary_pattern", patterns["Palette Twinkle 1D"])
    send_request("primary_speed", "1")
    return

def fireAriaWings():
    send_request("primary_pattern", patterns["Blackbody pulse from center"])
    return

def fireAriaEnd():
    send_request("primary_pattern", patterns["Palette Plasma 2D"])
    send_request("primary_speed", "0")
    sleep(4)
    send_request("primary_pattern", patterns["Fade out"])
    send_request("primary_speed", "0.2")
    return

def anotherSong():
    send_request("palette", palettes["Ocean"])
    send_request("primary_pattern", patterns["Wipe in"])
    send_request("primary_speed", "0.18")
    return

def end():
    send_request("primary_pattern", patterns["Fade out"])
    return

if __name__ == "__main__":
    device = InputDevice('/dev/input/event0')
        
    print("Listening to controller: {}".format(device.name))
    
    player = deque(PLAYLIST)
    current = player[0] 
    print("Executing {}".format(current))
    eval(player[0])()
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            e = categorize(event)
            if e.keystate == e.key_up:
                if e.keycode == 'KEY_PAGEDOWN':
                    # Next
                    player.rotate(-1)
                elif e.keycode == 'KEY_PAGEUP':
                    # Previous
                    player.rotate(1)
                print("Executing {}".format(player[0]))
                eval(player[0])()
                sys.stdout.flush()



