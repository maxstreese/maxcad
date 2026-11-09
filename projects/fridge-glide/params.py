"""Shared numbers for the fridge-glide project (all in mm).

MEASURED values come from our fridge; PLACEHOLDER values are guesses to be
replaced by measurements; FIT values are clearances to tune after a print.

Coordinates (use position, doors closed): x along the door's width (the
direction the slider runs), y out of the fridge door towards the furniture
door, z up. The fridge door's side edge (on its opening side) is x = 0. The
parts are drawn for a door opening on the right (the fridge door lies at
x > 0) and mirrored at the end for OPENING_SIDE = "left"; all x values below
are in that drawing. At the side edge the fridge door's front face is y = 0.
z = 0 is the rail's centre line.
"""

# Seen from the kitchen, the side the doors open on: the edge the slider's clip grips.
OPENING_SIDE = "left"

# --- The doors ----------------------------------------------------------------
DOOR_THICKNESS = 46.09  # MEASURED fridge door, front face to back face at its side edge
#   (calipers; tricky on the curved door)
DOOR_GAP = 22.0  # MEASURED fridge door front face to the furniture door's back face
#   (closed), at the side edge
# The fridge door's front is curved from side to side, bulging towards the
# furniture door: the gap falls from 22 at the edge to 17 at 75 mm in. It is
# taken as a circle of DOOR_RADIUS seen from above, through those two points;
# its crown (foremost point) follows from them. The furniture door is flat.
GAP_INWARD = (75.0, 17.0)  # MEASURED (distance in from the edge, gap there)
DOOR_RADIUS = 2000.0  # PLACEHOLDER (a gap measured further in, e.g. at 110, fixes it)
# PLACEHOLDER the back face is taken as flat: the hook stays straight.
SIDE_CLEARANCE = 6.0  # MEASURED (at least) free space beside the fridge door's side edge:
#   the clip's web must fit, and the rail must not reach past it
GASKET_FROM_EDGE = 6.0  # MEASURED room for the hook behind the back face, in from the side
#   edge (up to the gasket)
FRONT_THICKNESS = 19.0  # PLACEHOLDER furniture door (preview, and screw length)
# MEASURED while the doors open, the fridge door's edge moves from 30 to 120 mm
# in from the furniture door's edge: the slider (on the fridge door) runs 90 mm
# along the rail (on the furniture door), away from the furniture door's edge.
TRAVEL = 90.0

# --- Glide: round head in a diamond channel ----------------------------------------
# The channel's cross-section is a square turned 45 degrees (a diamond) with the
# slot at its corner facing the fridge door; the slider's head is a round bar.
# Pulled (door opening) or pushed (closing), the head wedges into a 90 degree V
# and centres itself, touching on two lines only.
HEAD_DIAMETER = 6.0
GLIDE_CLEARANCE = 0.3  # FIT head to channel, normal to each face (the head floats 0.42 in y and z)
SLOT_WIDTH = 4.0  # where the slot leaves the channel; it widens at 45 degrees towards the
#   fridge door. Narrower than the head's contact lines on the slot-side faces (2.33
#   either side of its axis)
NECK_THICKNESS = 3.0  # in z, through the slot: 0.5 clear each side when centred
CHANNEL_WALL = 1.5  # beyond the channel's corners
LEAD_IN = 0.7  # the channel and slot flare by this much (normal to the faces) at both rail ends
LEAD_IN_LENGTH = 4.0  # over this length
RUN_CLEARANCE = 1.0  # minimum gap between the rail and anything on the fridge door

# --- Slider (on the fridge door): a clip around its side edge -----------------------
SLIDER_LENGTH = 16.0  # the head, along the rail; it starts at the clip's outer face
HEAD_CHAMFER = 0.6  # on the head's ends, to find the lead-in
CLIP_HEIGHT = 50.0  # along the edge: more height, more pinch and less twist
WEB_THICKNESS = 2.5  # on the door's side face; must be < SIDE_CLEARANCE
HOOK_DEPTH = 4.0  # how far the back hook reaches in along the back face; < GASKET_FROM_EDGE
HOOK_THICKNESS = 2.5
HOOK_LEAD_IN = 1.5  # 45 degree chamfer on the hook's tip, so it slides over the edge
GRIP_INTERFERENCE = 0.4  # FIT clip span this much under DOOR_THICKNESS: it pinches the door
FRONT_LEG_THICKNESS = 3.0  # leg on the front face, at the door's foremost point under it
LEG_BEYOND_HEAD = 4.0  # the leg runs on this far past the head's inner end

# --- Rail (on the furniture door) ---------------------------------------------------
RAIL_END_MARGIN = 1.0  # beyond the head's travel at each end
FLANGE_THICKNESS = 3.0  # against the furniture door; the countersinks (1.85 deep) leave 1.15
SCREW_BEYOND_RAIL = 5.0  # screw centres above and below the channel's body (countersinks clear of it)
FLANGE_MARGIN = 5.0  # flange beyond the screw centres
SCREW_FROM_END = 8.0  # the outer screws, in from the rail's ends; a third in the middle
SCREW_HOLE = 3.8  # for 3.5 mm countersunk wood screws
SCREW_HEAD = 7.5  # countersink diameter (90 degrees)
