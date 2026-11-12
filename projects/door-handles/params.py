"""Shared numbers for the door-handles project (all in mm).

Values marked PLACEHOLDER are guesses. FIT values get tuned from the drill gauge.
Where the holes go (handle spacing, distances from the door's edges, which
corner) is not here: those are the template's options, in options.py.
"""

# --- Doors and handles -----------------------------------------------------
DOOR_THICKNESS = 19.0  # PLACEHOLDER (only used for the preview; doors must be > TEMPLATE_FENCE_DEPTH)
DRILL = 5.0  # drill bit for the handle screws

# --- Fits (FIT: tune with drill_gauge) -------------------------------------
DRILL_CLEARANCE = 0.2  # added to the drill diameter for the guide holes

# --- Drill template --------------------------------------------------------
TEMPLATE_PLATE = 4.0  # plate thickness = guide length for the drill
TEMPLATE_FENCE = 4.0  # fence wall thickness
TEMPLATE_FENCE_DEPTH = 15.0  # how far the fences reach down the door edges
TEMPLATE_FENCE_CORNER_GAP = 15.0  # fences end this far before the door corner
TEMPLATE_MARGIN = 15.0  # plate material beyond the outer holes
TEMPLATE_CORNER_RELIEF = 1.5  # groove in the inside corners for rounded door edges
