"""Shared numbers for the fridge-glide project (all in mm).

MEASURED values come from our fridge; PLACEHOLDER values are guesses to be
replaced by measurements; FIT values are clearances to tune after a print.

Coordinates (use position): x along the door's width (the direction the
slider runs), y out of the fridge door towards the furniture door, z up. The
fridge door's side edge (on its opening side) is x = 0. The parts are drawn
for a door opening on the right (the door lies at x > 0, the rail runs from the
edge to x = RAIL_LENGTH) and mirrored at the end for OPENING_SIDE = "left";
all x values below are in that drawing. At the rail's middle the door's front
face is y = 0. z = 0 is the rail's centre line.
"""

# Seen from the kitchen, the side the doors open on: the edge the clip grips.
OPENING_SIDE = "left"

# --- The doors ----------------------------------------------------------------
DOOR_THICKNESS = 50.0  # PLACEHOLDER fridge door, front face to back face at its side edge
DOOR_GAP = 28.0  # PLACEHOLDER fridge door front face to the furniture door's back face
#   (closed), at the rail's middle
# The fridge door's front is curved from side to side: a circle of DOOR_RADIUS
# seen from above, whose crown (foremost point) lies CROWN_OFFSET along +x
# from the rail's middle. The clip's front leg follows it along its whole
# length; the rail stays straight, parallel to the (flat) furniture door.
DOOR_RADIUS = 2000.0  # PLACEHOLDER
CROWN_OFFSET = 200.0  # PLACEHOLDER (the crown is near the door's middle, the rail near its edge)
# PLACEHOLDER the back face is taken as flat: the hook stays straight.
SIDE_CLEARANCE = 4.0  # PLACEHOLDER free space beside the fridge door's side edge (closed and
#   swinging): the clip's web must fit
GASKET_FROM_EDGE = 6.0  # PLACEHOLDER where the door gasket starts on the back face, in from
#   the side edge: the back hook must stay outside it
FRONT_THICKNESS = 19.0  # PLACEHOLDER furniture door (preview, and screw length)

# --- Clip around the fridge door's side edge ------------------------------------
CLIP_HEIGHT = 50.0  # along the edge: more height, more pinch and less twist
WEB_THICKNESS = 2.5  # on the door's side face; must be < SIDE_CLEARANCE
HOOK_DEPTH = 4.0  # how far the back hook reaches in along the back face; < GASKET_FROM_EDGE
HOOK_THICKNESS = 2.5
HOOK_LEAD_IN = 1.5  # 45 degree chamfer on the hook's tip, so it slides over the edge
GRIP_INTERFERENCE = 0.4  # FIT clip span this much under DOOR_THICKNESS: it pinches the door
FRONT_LEG_THICKNESS = 3.0  # leg on the front face, at the door's foremost point under it
#   (thicker where the door falls away behind it)

# --- Glide: round head in a diamond channel ----------------------------------------
# The channel's cross-section is a square turned 45 degrees (a diamond) with the
# slot at its front corner; the slider's head is a round bar. Pulled (door
# opening) the head rests in the front V, pushed (closing) in the back V: both
# ways it is wedged to the channel's centre line, touching on two lines only.
HEAD_DIAMETER = 8.0
GLIDE_CLEARANCE = 0.3  # FIT head to channel, normal to each face (the head floats 0.42 in y and z)
SLOT_WIDTH = 5.0  # where the slot leaves the channel; it widens at 45 degrees towards the front
NECK_THICKNESS = 4.0  # in z, through the slot: 0.5 clear each side when centred
CHANNEL_WALL = 2.0  # beyond the channel's back, top and bottom corners
LEAD_IN = 1.0  # the channel and slot flare by this much (normal to the faces) at both rail ends
LEAD_IN_LENGTH = 4.0  # over this length
RAIL_LENGTH = 120.0  # PLACEHOLDER covers the slider's travel while the doors open

# --- Slider (on the furniture door) ---------------------------------------------
SLIDER_LENGTH = 20.0  # along the rail
HEAD_CHAMFER = 1.0  # on the head's ends, to find the lead-in
PLATE_THICKNESS = 3.0
# One countersunk screw above and one below the rail, clear of it.
SCREW_BEYOND_RAIL = 5.0  # screw centre above the rail's top / below its bottom
PLATE_MARGIN = 6.0  # beyond each screw's centre
SCREW_HOLE = 3.8  # for 3.5 mm countersunk wood screws
SCREW_HEAD = 7.5  # countersink diameter (90 degrees)
RUN_CLEARANCE = 1.5  # minimum gap between the rail's front and the slider's plate
