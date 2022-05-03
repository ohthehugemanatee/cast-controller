# Playlist for the show
import sys
import json
import datetime
from time import sleep
from collections import deque
from evdev import InputDevice, ecodes, categorize
from castcontroller.ledcontrol import LEDs, LEDPreset
from castcontroller.pattern_library import palettes, patterns
from pathlib import Path


StageLights = LEDs()
position_file = Path('/tmp') / 'cast-controller'

# Helpful blackout preset
blackout = LEDPreset(
    palette=palettes["Blackout"], primary_pattern=patterns['Blackout'])


def get_saved_position():
    # Create file if it doesn't exist already
    position_file.touch(exist_ok=True)
    with open(str(position_file), mode='r') as data_file:
        try:
            position = data_file.read()
            if position:
                print(f'Loaded playlist position from {position_file}.')
            else:
                print('Creating a new datafile')
        except Exception:
            print(
                f'Saved playlist position at {position_file} is old/invalid, ignoring.')
    return position


def save_position(value):
    with open(str(position_file), 'w') as data_file:
        try:
            data_file.write(value)
            print(f'Saved settings to {position_file}.')
        except Exception:
            print(f'Could not save settings to {position_file}.')


def run_playlist(input_device):
    device = InputDevice(input_device)

    player = deque(PLAYLIST)
    if len(sys.argv) > 1:
        position = str(sys.argv[1])
    else:
        position = get_saved_position()
    if position:
        while player[0].__name__ != position:
            player.rotate(1)
    print("Starting from {}".format(player[0].__name__))
    player[0]()
    # Double-click protection: require a minimum time between clicks.
    time_limit = datetime.timedelta(seconds=1)
    # Start with a dummy timestamp for last change
    now = datetime.datetime.now()
    last_change_timestamp = now - datetime.timedelta(minutes=2)
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            now = datetime.datetime.now()
            if (now - last_change_timestamp) < time_limit:
                continue
            e = categorize(event)
            if e.keystate == e.key_up:
                
                if e.keycode == 'KEY_PAGEDOWN':
                    # Next
                    player.rotate(-1)
                elif e.keycode == 'KEY_PAGEUP':
                    # Previous
                    player.rotate(1)
                save_position(player[0].__name__)
                print("Executing {}".format(player[0].__name__))
                last_change_timestamp = now
                player[0]()
                sys.stdout.flush()


def start():
    StageLights.apply(blackout)
    return


def willkommen():
    StageLights.apply(LEDPreset(
        primary_pattern=1635425247769, 
        palette=1634158357712, 
        brightness=1,
        secondary_pattern=7))


def moderation():
    StageLights.apply(
        LEDPreset(palettes["Sunset Light"],
                  1635425452181,
                  brightness=0.55
                  ))


def zitti_zitti():
    params = """
     {
        "brightness": 1,
        "palette": 1635281872064,
        "primary_pattern": 1635426084409
    }"""
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def norma():
    params = """
    {
        "brightness": 0.6,
        "palette": 1635282276093,
        "primary_pattern": 1635426495476
        }"""

    params = json.loads(params)
    base = LEDPreset(**params)
    StageLights.apply(base)


def ganz_ohne_weiber1():
    base = LEDPreset(
        palettes["Miami"],
        1635426637210,
        brightness=0.3
    )
    StageLights.apply(base)


def granada():
    StageLights.apply(LEDPreset(
        palettes["Golden Hour"],
        1635426908951,
        primary_speed=0.19
    ))


def a_beber():
    params = """
        {
        "brightness": 0.55,
        "palette": 150,
        "primary_pattern": 1635427041369,
        "primary_speed": 0.45
        }
    """
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def vilja1():
    apply_from_json("""{
        "brightness": 1.0,
        "palette": 1634906800552,
        "primary_pattern": 1635324171757
        }""")


def vilja2():
    StageLights.apply(blackout)
    sleep(3)
    # @todo: needs a new pattern for (audience) right to left with her snaps.
    # weird flash when it goes to start the twinkle?
    # Twinkle moves too fast. when it's fading in
    base = LEDPreset(palettes["Ocean"],
                     1635427181230,
                     brightness=0,
                     secondary_pattern=8,
                     secondary_speed=0.88,
                     secondary_scale=5.71)
    StageLights.apply(base)
    while base.brightness < 1:
        brightness = base.brightness + 0.03
        base.brightness = round(brightness, 3)
        # Cap it to 1 otherwise the value wraps around.
        if base.brightness > 1:
            base.brightness = 1
        StageLights.apply(base)
        sleep(0.3)


def belle_nuit():
    params = """
        {
        "brightness": 0.55,
        "palette": 170,
        "primary_pattern": 1635427261230
        }"""
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def sempre_mobile():
    params = """
    {
        "brightness": 1.0,
        "palette": 1635283757687,
        "primary_pattern": 1635283894849,
        "primary_scale": 1.0,
        "primary_speed": 0.05
        }"""

    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def chinese_traditional():
    # glimmering alternates slow and fast.
    # second time through it eventually switched to white.
    params = """
    {
        "palette": 1651586939251,
        "primary_pattern": 1,
        "primary_scale": 1,
        "primary_speed": 0.91,
        "secondary_pattern": 0,
        "secondary_speed": 1,
        "secondary_scale": 1
    }"""
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def end():
    StageLights.apply(LEDPreset(
        primary_pattern=patterns["Fade out"]
    ))


def anvil():
    # would be nice with a fade in
    apply_from_json("""
    {
        "brightness": 1.0,
        "palette": 160,
        "primary_speed": 0.25,
        "primary_pattern": 1635439528544,
        "secondary_pattern": 12,
        "secondary_speed": 0.38,
        "secondary_scale": 0.97
        }""")


def dont_stop_me():
    apply_from_json("""{
        "brightness": 1.0,
        "palette": 190,
        "secondary_pattern": 0,
        "primary_pattern": 1635439603304
        }""")


def ombra_mai_fu():
    # @todo: gradually fade from purple to red.
    # Backup:
    apply_from_json(""" {
        "palette": 1635285216783,
        "primary_pattern": 1635285209252
        }""")


def non_credea():
    base = LEDPreset(palettes["White"],
                     patterns["Static Color"],
                     brightness=0.3)
    StageLights.apply(base)


def non_giunge():
    apply_from_json(""" {
        "brightness": 1,
        "palette": 1635285809894,
        "primary_pattern": 1634079287296,
        "primary_speed": 0.27
        }""")


def una_furtiva():
    apply_from_json(""" {
        "palette": 1635285988457,
        "primary_pattern": 1,
        "primary_scale": -3.43,
        "primary_speed": 0.16
        }""")


def when_i_am_laid():
    # @todo: grow brightness
    apply_from_json("""
    {
        "palette": 1634907211469,
        "primary_pattern": 1635286756259,
        "primary_speed": 0.25
        }""")


def es_ist_einmal():
    # @todo: correct the palette
    apply_from_json("""
    {
        "palette": 1635287289272,
        "primary_pattern": 1635440199649
        }""")


def mendelsohn():
    # correct the color. No way this is right!
    apply_from_json("""
        {
        "brightness": 0.55,
        "palette": 190,
        "primary_pattern": 180
        }""")


def dimgh():
    apply_from_json("""
     {
        "brightness": 0.85,
        "palette": 1634910211574,
        "primary_pattern": 180,
        "primary_scale": 0.0,
        "primary_speed": 0.22
        }""")


def funiculi():
    apply_from_json("""
    {
        "brightness": 1,
        "palette": 90,
        "primary_pattern": 170,
        "primary_scale": 6.75,
        "primary_speed": 0.03
        }""")


def heia():
    apply_from_json("""
    {
        "brightness": 1.0,
        "palette": 190,
        "primary_pattern": 100,
        "primary_scale": -3.43,
        "primary_speed": 0.16,
        "secondary_pattern": 0,
    }""")


def lippen_schweigen():
    apply_from_json("""
    {
        "palette": 1634158357712,
        "primary_pattern": 141,
        "primary_scale": 1.0,
        "primary_speed": 0.15,
        "secondary_pattern": 7,
        "secondary_scale": 0.51,
        "secondary_speed": 0.3 
    }""")

def fledermaus_brindisi():
    # glimmering alternates slow and fast.
    # Wrong color. Should be in white.
    # second time through it eventually switched to white.
    params = """
    {
        "brightness": 1.0,
        "palette": 1651585677657,
        "primary_pattern": 0,
        "secondary_pattern": 1,
        "secondary_speed": 0.93,
        "secondary_scale": 0.04
    }"""
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))


def apply_from_json(params):
    params = json.loads(params)
    StageLights.apply(LEDPreset(**params))



PLAYLIST = (
    start,
    willkommen,  # Willkommen
    moderation,  # Eröffnungstext Anne und Till
    zitti_zitti,  # Zitti zitti  / Sempre mobile
    norma,  # Mira, o Norma cavatina
    moderation,
    ganz_ohne_weiber1,  # Ganz ohne Weiber recit
    granada,  # Granada
    moderation, # Anne and Gui text
    a_beber,  # A beber
    moderation, # Sascha moderation
    vilja1,  # Viljalied opening (cue: njet njet njet)
    vilja2,  # Viljalied starting when she says NEIN.
    moderation,  # Text but we don't know from whom.
    belle_nuit,  # Belle nuit
    moderation,
    fledermaus_brindisi, # Yu solo AND fledermaus brindisi right after.
    end, # end of the first half.

    anvil,  # Anvil coro
    moderation,  # Text Till
    dont_stop_me,  # Don't stop me now
    moderation,  # Text Anne
    ombra_mai_fu,  # Ombra mai fu
    non_credea,  # Moderation CarrieAnne and ah non credea cavatina in one cue
    non_giunge,  # Ah non giunge
    moderation,
    una_furtiva,  # Una furtiva lagrima
    moderation,  # Short when I am laid moderation 
    when_i_am_laid,  # When I am laid
    es_ist_einmal,  # Es ist einmal im Leben so
    moderation,  # Interview anne and yu
    chinese_traditional,  # Yu chinese traditional piece 
    heia,  # Heia
    dimgh,  # Dein ist mein ganzes Herz
    funiculi,   # Funiculi
    lippen_schweigen,  # Lippen schweigen
    end

)

