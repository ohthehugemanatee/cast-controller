# Playlist for the show
import sys
from time import sleep
from collections import deque
from evdev import InputDevice, ecodes, categorize
from castcontroller.ledcontrol import LEDs, LEDPreset
from castcontroller.pattern_library import palettes, patterns


PLAYLIST = (
    'start',
    'heia',
    'fireAriaStart',
    'fireAriaWings',
    'fireAriaEnd',
    'anotherSong',
    'end',
)

StageLights = LEDs()


def run_playlist(input_device):
    device = InputDevice(input_device)

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


def start():
    blackout = LEDPreset(primary_pattern=patterns['Blackout'])
    color = LEDPreset(palettes['Sunset Light'], patterns['Static Color'])
    StageLights.apply(blackout)
    sleep(1)
    StageLights.apply(color)
    sleep(1)
    StageLights.apply(blackout)
    sleep(1)
    StageLights.apply(color)
    sleep(1)
    StageLights.apply(blackout)
    sleep(1)
    StageLights.apply(color)
    sleep(1)
    StageLights.apply(blackout)
    return


def heia():
    base = LEDPreset(palettes["Sky Blue"], patterns["Fade in"])
    StageLights.apply(base)
    sleep(3)
    base.primary_pattern = patterns["Palette Plasma 2D"]
    StageLights.apply(base)


def fireAriaStart():
    StageLights.apply(
        LEDPreset(palettes["Fire"], patterns["Palette Twinkle 1D"]))


def fireAriaWings():
    StageLights.apply(
        LEDPreset(primary_pattern=patterns["Blackbody pulse from center"]))


def fireAriaEnd():
    StageLights.apply(
        LEDPreset(primary_pattern=patterns["Palette Plasma 2D"],
                  primary_speed=0))
    sleep(4)
    StageLights.apply(
        LEDPreset(primary_pattern=patterns["Fade out"], primary_speed=0.2))
    return


def anotherSong():
    StageLights.apply(LEDPreset(
        primary_pattern=patterns["Wipe in"],
        primary_speed=0.18,
        palette=palettes["Ocean"]
    ))


def end():
    StageLights.apply(LEDPreset(
        primary_pattern=patterns["Fade out"]
    ))
