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
        "palette": 1634158357712,
        "primary_pattern": 141,
        "primary_scale": 1.0,
        "primary_speed": 0.77,
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
                  patterns["Palette Plasma 2D"],
                  brightness=0.55))


def zitti_zitti():
    params = """
     {
        "brightness": 1,
        "color_temp": 6000,
        "palette": 1635281872064,
        "primary_pattern": 180,
        "primary_scale": 1.0,
        "primary_speed": 0.2,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": 0.0,
        "secondary_speed": 0.33
    }"""
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def norma():
    params = """
    {
        "brightness": 0.6,
        "color_temp": 6000,
        "palette": 1635282276093,
        "primary_pattern": 141,
        "primary_scale": 1.0,
        "primary_speed": 0.25,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": 0.0,
        "secondary_speed": 0.33
    }"""

    params = json.loads(params)
    base = LEDPreset(**params)
    StageLights.apply(base)
    sleep(120)
    for i in range(0, 45):
        new_base = base
        if base.brightness < 1:
            new_base.brightness = base.brightness + 0.02
        if base.primary_speed < 1.2:
            new_base.primary_speed = base.primary_speed + 0.02
        if new_base != base:
            base = new_base
            StageLights.apply(base)
        sleep(1)


def ganz_ohne_weiber():
    # The loop is still not working. :(
    base = LEDPreset(
        palettes["Miami"],
        patterns["Palette Plasma 2D"],
        brightness=0.3
    )
    StageLights.apply(base)
    sleep(50)  # Or could be a cue?
    for i in range(0, 30):
        new_base = base
        if base.brightness < 1:
            new_base.brightness = base.brightness + 0.05
        if base.primary_speed < 1:
            new_base.primary_speed = base.primary_speed + 0.05
        if new_base != base:
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
        "palette": 150,
        "primary_pattern": 140,
        "primary_scale": 3.03,
        "primary_speed": 0.06,
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
    # only the outer two lit
    StageLights.apply(blackout)


def vilja2():
    # @todo: needs a new pattern for (audience) right to left with her snaps.
    start()
    sleep(5)
    # @todo: needs a new pattern for crossfade.
    # Note: needs a blackout palette before starting the twinkle.
    StageLights.apply(LEDPreset(palettes["Ocean"],
                                patterns["Static Gradient 1D"],
                                secondary_pattern=8,
                                secondary_speed=0.88,
                                secondary_scale=5.71))


def belle_nuit():
    params = """
        {
        "brightness": 0.55,
        "color_temp": 8000,
        "palette": 170,
        "primary_pattern": 140,
        "primary_scale": 3.03,
        "primary_speed": 0.06,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": -5.4,
        "secondary_speed": 0.08
    }"""
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def sempre_mobile():
    params = """
    {
        "brightness": 1.0,
        "color_temp": 6000,
        "palette": 1635283757687,
        "primary_pattern": 1635283894849,
        "primary_scale": 1.0,
        "primary_speed": 0.05,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": 0.0,
        "secondary_speed": 0.05
    }"""

    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def fledermaus_brindisi():
    params = """
    {
        "brightness": 1.0,
        "color_temp": 6000,
        "palette": 1634906800552,
        "primary_pattern": 0,
        "primary_scale": 1.0,
        "primary_speed": 0.05,
        "saturation": 1.0,
        "secondary_pattern": 8,
        "secondary_scale": -8.74,
        "secondary_speed": 1.24
    }"""
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def end():
    StageLights.apply(LEDPreset(
        primary_pattern=patterns["Fade out"]
    ))


def anvil():
    apply_from_json("""
    {
        "brightness": 1.0,
        "color_temp": 6000,
        "palette": 160,
        "primary_pattern": 141,
        "primary_scale": 1.0,
        "primary_speed": 0.25,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": -0.09,
        "secondary_speed": 1.32
    }""")


def dont_stop_me():
    apply_from_json("""{
        "brightness": 1.0,
        "color_temp": 6000,
        "palette": 190,
        "primary_pattern": 141,
        "primary_scale": 1.0,
        "primary_speed": 0.25,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": -0.09,
        "secondary_speed": 1.32
    }""")


def ombra_mai_fu():
    # @todo: gradually fade from purple to red.
    # Backup:
    apply_from_json(""" {
        "brightness": 1.0,
        "color_temp": 6000,
        "palette": 1635285216783,
        "primary_pattern": 1635285209252,
        "primary_scale": 1.0,
        "primary_speed": 0.05,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": -0.09,
        "secondary_speed": 1.32
    }""")


def non_credea():
    StageLights.apply(blackout)
    # Todo: loop to gradually grow brightness to 0.9
    # White light only. Ends around the end of the cavatina.


def non_giunge():
    apply_from_json(""" {
        "brightness": 1,
        "color_temp": 6000,
        "palette": 1635285809894,
        "primary_pattern": 1634079287296,
        "primary_scale": 1.0,
        "primary_speed": 0.56,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": -0.09,
        "secondary_speed": 1.32
    }""")


def una_furtiva():
    apply_from_json(""" {
        "brightness": 1.0,
        "color_temp": 6000,
        "palette": 1635285988457,
        "primary_pattern": 100,
        "primary_scale": -3.43,
        "primary_speed": 0.16,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": -0.09,
        "secondary_speed": 1.32
    }""")


def when_i_am_laid():
    apply_from_json("""
    {
        "brightness": 1,
        "color_temp": 12000,
        "palette": 1634907211469,
        "primary_pattern": 1635286756259,
        "primary_scale": 1.0,
        "primary_speed": 0.27,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": 2.0,
        "secondary_speed": 0.59
        }""")


def es_ist_einmal():
    apply_from_json("""
    {
        "brightness": 1.0,
        "color_temp": 12000,
        "palette": 1635287289272,
        "primary_pattern": 120,
        "primary_scale": 1.0,
        "primary_speed": 0.28,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": 2.0,
        "secondary_speed": 0.59
        }""")


def mendelsohn():
    apply_from_json("""
        "params": {
        "brightness": 0.55,
        "color_temp": 8000,
        "palette": 190,
        "primary_pattern": 180,
        "primary_scale": 0.0,
        "primary_speed": 0.22,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": -5.4,
        "secondary_speed": 0.08
    }""")


def dimgh():
    apply_from_json("""
     {
        "brightness": 0.55,
        "color_temp": 8000,
        "palette": 1634910211574,
        "primary_pattern": 180,
        "primary_scale": 0.0,
        "primary_speed": 0.22,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": -5.4,
        "secondary_speed": 0.08
    }""")


def funiculi():
    apply_from_json("""
    {
        "brightness": 0.55,
        "color_temp": 8000,
        "palette": 90,
        "primary_pattern": 170,
        "primary_scale": 6.75,
        "primary_speed": 0.03,
        "saturation": 1.0,
        "secondary_pattern": 0,
        "secondary_scale": -5.4,
        "secondary_speed": 0.08
    }""")


def heia():
    apply_from_json("""
    {
        "brightness": 1.0,
        "color_temp": 5830,
        "palette": 190,
        "primary_pattern": 100,
        "primary_scale": -3.43,
        "primary_speed": 0.16,
        "saturation": 1.0,
        "secondary_pattern": 8,
        "secondary_scale": 0.51,
        "secondary_speed": 0.77
    }""")


def lippen_schweigen():
    apply_from_json("""
    {
        "brightness": 1.0,
        "color_temp": 5830,
        "palette": 1634158357712,
        "primary_pattern": 141,
        "primary_scale": 1.0,
        "primary_speed": 0.15,
        "saturation": 1.0,
        "secondary_pattern": 7,
        "secondary_scale": 0.51,
        "secondary_speed": 0.3 
    }""")


def apply_from_json(params):
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


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
    end,  # End of the first half
    anvil,  # Anvil coro
    moderation,  # Text Anne
    dont_stop_me,  # Don't stop me now
    moderation,  # Text Anne
    ombra_mai_fu,  # Ombra mai fu
    non_credea,  # Text CarrieAnne and ah non credea cavatina
    non_giunge,  # Ah non giunge
    moderation,  # Text Guillermo
    una_furtiva,  # Una furtiva lagrima
    when_i_am_laid,  # When I am laid
    es_ist_einmal,  # Es ist einmal im Leben so
    moderation,  # Interview anne and yu
    mendelsohn,  # Mendelssohn Hochzeitsmarsch
    dimgh,  # Dein ist mein ganzes Herz
    funiculi,   # Funiculi
    heia,  # Heia
    lippen_schweigen,  # Lippen schweigen
    end

)

# @todo: don't forget to handle segfaults!
