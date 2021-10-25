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
    current = player[0]
    print("Executing {}".format(current))
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
                print("Executing {}".format(player[0]))
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
        params: {
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
    params = json.load(params)
    StageLights.apply(LEDPreset(params))


def moderation():
    params = """
        params: {
        "brightness": 1.0,
        "color_temp": 5830,
        "gamma": 1.0,
        "palette": 1634158357712,
        "primary_pattern": 170,
        "primary_scale": 1.0,
        "primary_speed": 0.77,
        "sacn": 0,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": 0.51,
        "secondary_speed": 0.3
    }
    """
    params = json.load(params)
    StageLights.apply(
        LEDPreset(palettes["Sunset Light"],
                  patterns["Palette Plasma 2D"]))


def zitti_zitti():
    # @todo: new color palette for this.
    StageLights.apply(blackout)


def ganz_ohne_weiber():
    base = LEDPreset(
        palettes["Hot Pink"],
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


def end():
    StageLights.apply(LEDPreset(
        primary_pattern=patterns["Fade out"]
    ))


PLAYLIST = (
    start,
    overture,  # Ouvertüre in Teilen von Yu
    willkommen,  # Willkommen
    moderation,  # Eröffnungstext Anne und Till
    zitti_zitti,  # Zitti zitti  / Sempre mobile
    moderation,  # Interview 1
                 # Text Till
    ganz_ohne_weiber,  # Ganz ohne Weiber
    moderation,
    # Il dolce suono
    # Text Sasha
    # Villja Lied
    # Interview 2
    # Text Till
    # Zueignung
    # Text Till
    # When I am laid
    # Text Guillermo
    # Bolero
    # Text Anne
    # Don’t stop me now
    # Interview 3
    # Text Anne und Till
    # A beber
    # Pause
    # Ouvertüre komplett
    # Belle nuit
    # Text Anne
    # Ombra mai fu
    # Text Guillermo
    # Una furtiva lagrima
    # Anvil
    # Text Anne
    # Mira o Norma
    # Text CarrieAnne
    # Ah non credea non giunge
    # Es ist einmal im Leben so
    # Interview Anne und Yu
    # Mendelssohn Hochzeitsmarsch
    # Dein ist mein ganzes Herz

    # Zugabe

    # Funiculi Funicula
    # Lippen schweigen

    # Outro Anne und Till
    end,
)
