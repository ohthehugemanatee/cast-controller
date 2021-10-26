# Playlist for the show
import sys
import json
from time import sleep
from collections import deque
from evdev import InputDevice, ecodes, categorize
from castcontroller.ledcontrol import LEDs, LEDPreset
from castcontroller.pattern_library import palettes, patterns


StageLights = LEDs()

# Helpful blackout preset
blackout = LEDPreset(primary_pattern=patterns['Blackout'])


def run_playlist(input_device):
    device = InputDevice(input_device)

    player = deque(PLAYLIST)
    print("Executing {}".format(player[0].__name__))
    player[0]()
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
                print("Executing {}".format(player[0].__name__))
                player[0]()
                sys.stdout.flush()


def start():
    color = LEDPreset(palettes['Sunset Light'], patterns['Static Color'])
    StageLights.apply(blackout)
    sleep(2)
    StageLights.apply(color)
    sleep(2)
    StageLights.apply(blackout)
    sleep(2)
    StageLights.apply(color)
    sleep(2)
    StageLights.apply(blackout)
    sleep(2)
    StageLights.apply(color)
    sleep(2)
    StageLights.apply(blackout)
    return


def overture():
    StageLights.apply(LEDPreset(palettes["Sky Blue"],
                                patterns["Palette Plasma 2D"],
                                primary_speed=0.3,
                                secondary_speed=0.1))


def willkommen():
    params = """
        {
        "brightness": 1.0,
        "color_temp": 5830,
        "gamma": 1.0,
        "palette": 1634158357712,
        "primary_pattern": 141,
        "primary_scale": 1.0,
        "primary_speed": 0.77,
        "sacn": 0,
        "saturation": 1.0,
        "secondary_pattern": 7,
        "secondary_scale": 0.51,
        "secondary_speed": 0.3
    }
    """
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def moderation():
    StageLights.apply(
        LEDPreset(palettes["Sunset Light"],
                  patterns["Palette Plasma 2D"]))


def zitti_zitti():
    # @todo: new color palette for this.
    StageLights.apply(blackout)


def norma():
    StageLights.apply(LEDPreset(
        palettes["Purple"],
        patterns["Palette Fractal Plasma 2D"],
        primary_speed=0.2
    ))


def ganz_ohne_weiber():
    base = LEDPreset(
        palettes["Miami"],
        patterns["Palette Plasma 2D"],
        brightness=0.3
    )
    StageLights.apply(base)
    sleep(50)  # Or could be a cue?
    i = 0
    for i in range(i, 30):
        new_base = base
        if base.brightness < 1:

            new_base.brightness = base.brightness + 0.5
        if base.primary_speed < 1:
            new_base.primary_speed = base.primary_speed + 0.5
        if new_base is not base:
            base = new_base
            StageLights.apply(base)
        sleep(1)


def granada():
    StageLights.apply(LEDPreset(
        palettes["Golden Hour"],
        patterns["Palette Fractal Plasma 2D"],
        primary_speed=0.3
    ))


def a_beber():
    params = """
        {
        "brightness": 0.55,
        "color_temp": 12000,
        "gamma": 1.0,
        "palette": 150,
        "primary_pattern": 140,
        "primary_scale": 3.03,
        "primary_speed": 0.06,
        "sacn": 0,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": -5.4,
        "secondary_speed": 0.08
    }
    """
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def vilja1():
    # @todo: needs a new palette for flat white.
    StageLights.apply(blackout)


def vilja2():
    # @todo: needs a new pattern for (audience) right to left with her snaps.
    start()
    sleep(5)
    # @todo: needs a new pattern for crossfade.
    StageLights.apply(LEDPreset(palettes["Ocean"],
                                patterns["Static Gradient 1D"],
                                secondary_pattern=8))


def belle_nuit():
    params = """
        {
        "brightness": 0.55,
        "color_temp": 8000,
        "gamma": 1.0,
        "palette": 170,
        "primary_pattern": 140,
        "primary_scale": 3.03,
        "primary_speed": 0.06,
        "sacn": 0,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": -5.4,
        "secondary_speed": 0.08
    },"""
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def sempre_mobile():
    StageLights.apply(LEDPreset(
        palettes["Golden Hour"],
        patterns["Palette Scan Mirrored 1D"]
    ))


def fledermaus_brindisi():
    StageLights.apply(LEDPreset(
        palettes["Sunset Light"],
        patterns["Blackbody pulse from center"],
    ))


def end():
    StageLights.apply(LEDPreset(
        primary_pattern=patterns["Fade out"]
    ))


PLAYLIST = (
    start,
    willkommen,  # Willkommen
    moderation,  # Eröffnungstext Anne und Till
    zitti_zitti,  # Zitti zitti  / Sempre mobile
    norma,  # Mira, o Norma
    moderation,  # Text Till
    ganz_ohne_weiber,  # Ganz ohne Weiber
    granada,  # Granada
    moderation,  # Text Anne
    a_beber,  # A beber
    moderation,  # Text Sascha
    vilja1,  # Viljalied opening
    vilja2,  # Viljalied starting when she says NEIN.
    belle_nuit,  # Belle nuit
    sempre_mobile,  # Sempre mobile
    fledermaus_brindisi,  # Fledermaus Brindisi
    end  # End of the first half
)
