"""Shared numbers for the Canyon EP403-16 cover (all in mm).

Source: a friend's Solid Edge sketches of the original part (three screen
photos, 2026-11-08): a plan view of the outline and a side view of the bend.

    MEASURED     a dimension he wrote in the sketch
    ESTIMATE     read off the screen photo by pixels (about 15.8 px/mm), or
                 derived from such a reading
    PLACEHOLDER  not in the sketches at all; a guess until he measures it

Coordinates follow his sketch: x across, y along the part from the top edge
(y = 0) down to the slit end (y = -37), z up. The slit end is the rounded
"bird head" in Canyon's product photo.
"""

# --- Outline, seen from above (plan view) ------------------------------------
LENGTH = 37.0  # MEASURED top edge to slit end. Taken as projected (straight
#   across, as in his side view); if it was measured along the curve, the part
#   is about 2.5 mm too long in projection here.
TOP_EDGE = 19.78  # MEASURED straight part of the top edge, between the corner radii
TOP_CORNER_RADIUS = 2.0  # MEASURED (R 2), both top corners
LEFT_X = -7.85  # ESTIMATE the straight left side; the top width follows from it
LEFT_STRAIGHT = 19.37  # MEASURED straight left side, below the top-left corner radius
LEFT_ARC_RADIUS = 11.83  # MEASURED the arc from the left side round to the slit end
BOTTOM_FLAT = 5.12  # MEASURED flat end between the slit mouth and the bottom-right corner
#   (the right side, drawn slanted, runs from the top-right corner to the
#   bottom-right corner these two place: about 3 mm narrower at the bottom)
BOTTOM_CORNER_RADIUS = 2.0  # PLACEHOLDER bottom-right corner (drawn rounded, no number)

# --- Slit and keyhole -------------------------------------------------------
KEYHOLE_RADIUS = 1.75  # MEASURED (R 1,75)
KEYHOLE_X = 2.8  # ESTIMATE
KEYHOLE_FROM_END = 24.32  # MEASURED slit end to the keyhole, read as to its lower edge
SLIT_WIDTH_TOP = 1.0  # ESTIMATE at the keyhole
SLIT_MOUTH_LEFT_X = 2.0  # ESTIMATE where the slit meets the end, left side
SLIT_WIDTH_MOUTH = 2.7  # ESTIMATE at the end
SLIT_MOUTH_RADIUS = 0.4  # MEASURED (R 0,4) the corners of the slit's mouth

# --- Bend, seen from the side ----------------------------------------------
FLAT_LENGTH = 10.11  # MEASURED flat from the top edge before the bend starts
BEND_RADIUS = 41.0  # MEASURED (R 41) the rest of the length, bending down (-z)
THICKNESS = 2.0  # PLACEHOLDER not in the sketches. His curve is taken as the
#   frame side (inner) surface; the thickness goes on the outside of the bend.

# --- Screw holes -------------------------------------------------------------
# PLACEHOLDER all three: not in his sketch at all. Canyon's photo shows two
# small holes, one on each side of the slit, near its mouth. Drilled square
# to the surface.
HOLE_DIAMETER = 2.2
HOLE_FROM_END = 6.0  # distance from the slit end, along y
HOLE_OFFSET = 5.0  # either side of the slit's centre line, along x
