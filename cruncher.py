import math
from PIL import Image  # PIL = pillow


TESTER = {
    'black': (0, 0, 0),
    'navy': (0, 0, 128),
    'teal': (0, 128, 128),
    'grey': (128, 128, 128),
}

TOLERANCE = 180  # read a bit online and tried myself


def distance(img, tester):
    '''Calculates the distance between two RGB points'''
    (r1, g1, b1) = img
    (r2, g2, b2) = tester

    return math.sqrt(
        (r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2
    )


def nearest_color(dominant_color):
    '''Finds the RGB value for the image'''

    # for convenience
    _TESTER_RGBS = list(TESTER.values())
    _TESTER_NAMES = list(TESTER.keys())
    
    # creates a list of ((R,G,B), distance)
    # a color makes it into the list only if below tolerance levels
    # tolerance has been set with trial and error just with the purpose
    # of testing the functionality
    relevant_colors = []
    for _test in _TESTER_RGBS:
        col_dist = (_test, distance(dominant_color, _test))
        if col_dist[1] == 0.0:
            # exact match, exit the loop, saves some computation time
            relevant_colors = [col_dist]
            break
        if col_dist[1] < TOLERANCE:
            relevant_colors.append(col_dist)

    if not relevant_colors:  # no match
        return None
    
    if len(relevant_colors) > 1:  # sorts them if there's more than one 
        relevant_colors = sorted(relevant_colors, key=lambda c : c[1])
    nearest = relevant_colors[0][0]

    return _TESTER_NAMES[_TESTER_RGBS.index(nearest)]


def cruncher(img):
    '''Main crunching task'''
    _WIDTH, _HEIGHT = (150, 150)

    im = Image.open(img)
    im = im.resize((_WIDTH, _HEIGHT), resample=0)

    # size.0 * size.1 is max maxcolors value
    # http://effbot.org/imagingbook/image.htm
    pixels = im.getcolors(im.size[0] * im.size[1])
    pixels = sorted(pixels, key=lambda px: px[0], reverse=True)
    dominant_color = pixels[0][1]

    return nearest_color(dominant_color)