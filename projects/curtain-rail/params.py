"""Shared numbers for the curtain-rail project (all in mm).

The rail's inner shape is traced from the manufacturer's drawing, never
measured. The stopper built from these numbers was printed and fits the rail
(2026-11-09), better than copies 0.3 and 0.6 mm taller, so they stand as they are.
"""

# --- Curtain rail (Gardinia profile 4460) ----------------------------------
# Coordinates: x across the rail, z up from the rail's bottom face, rail runs along y.
# The lower (glider) channel has no flat floor: its side walls curve inward into
# the lips that form the 6 mm slot. The inner values are traced from the
# manufacturer's drawing at about 17.5 px/mm.
RAIL_WIDTH = 13.0
RAIL_HEIGHT_LEFT = 10.0
RAIL_HEIGHT_RIGHT = 8.8
RAIL_SLOT = 6.0  # opening of the lower (glider) channel
RAIL_INNER_HALF_WIDTH = 5.3  # centre to the inside of the side walls
RAIL_WEB_BOTTOM = 4.9  # underside of the web (top of the glider channel)
RAIL_WEB_TOP = 5.9
# The channel's rounded bottom: one arc on each side, from the bottom of the
# straight side wall down to the edge of the slot, meeting the wall at an
# angle (about 52 degrees off vertical), not tangentially. Fitted to points
# traced from the drawing (2026-11-08): a single arc of radius 7.2 fits them
# to 0.05 mm rms, about one pixel; an arc tangent to the wall fits 3x worse.
RAIL_CHANNEL_WALL_BOTTOM = 1.9  # where the straight side wall ends
RAIL_LIP_TOP = 0.7  # top of the lips at the slot edge
RAIL_CHANNEL_RADIUS = 7.2  # radius of the rounded bottom
# Outside of the left lower corner, as (x, z) points (preview only).
RAIL_OUTER_CURVE = [(-6.5, 1.9), (-6.35, 1.4), (-6.1, 0.94), (-5.8, 0.7), (-5.5, 0.47), (-5.1, 0.24), (-4.6, 0.0)]

# --- Fits --------------------------------------------------------------------
FIT_SLIDE = 0.3  # clearance all around between slider and channel (normal to the surface)
FIT_SLOT = 0.4  # clearance per side between stem and the 6 mm slot; keep > FIT_SLIDE so the
#   stem meets the slider's flat bottom, not its curve (the slider does the locating)

# --- Hardware --------------------------------------------------------------
# The set screw runs in a heat-set insert: CNC Kitchen M3 x 3 short. A thread
# cut by the screw itself into the plastic did not hold. From CNC Kitchen's
# "Dimensions & Design Guidelines" table (checked 2026-11-08): hole D2 4.0,
# minimum wall W 1.6, length L 3.0, outer diameter D1 4.6. A blind hole must
# be at least L + 1 mm deep; a through hole has no minimum, displaced plastic
# leaves at the far end. The stopper (4.3 mm tall) uses a through hole, which
# the set screw passes through freely.
INSERT_HOLE = 4.0  # hole diameter for the insert, through the whole part
INSERT_LENGTH = 3.0
INSERT_DIAMETER = 4.6  # outer diameter (preview only)
INSERT_MIN_WALL = 1.6  # minimum plastic around the insert

# --- Space at the rail end ------------------------------------------------
# The gap between the rail's end and the wall is about 15 mm. Every part goes
# in from that end, so none may be longer than this (includes ~2 mm margin).
MAX_PART_LENGTH = 13.0

# --- Stopper ---------------------------------------------------------------
STOPPER_LENGTH = MAX_PART_LENGTH
STOPPER_NOSE_CHAMFER = 0.6
SET_SCREW_LENGTH = 5.0  # M3x5 flat point (DIN 913 / ISO 4026)

