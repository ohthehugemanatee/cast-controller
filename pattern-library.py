# A place to keep patterns I wrote in the led-control GUI

# palette mirrored, but with a brightness crescendo. NB you have to start the
# palette with a low HSV "V" value.
def pattern(t, dt, x, y, z, prev_state):
    pal = palette_mirrored(wave_sine(t) + x)
    brightness = pal[2]
    if t > 1:
        if prev_state[2] > 0.98:
            brightness = 1
        else:
            brightness = prev_state[2] + 0.05
    return (pal[0], pal[1], brightness), hsv