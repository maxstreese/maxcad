# door-handles

Drill template for mounting handles on doors.

| Part | What it does |
|---|---|
| `drill_template` | Template for the door's top right corner; fences hook over the right and top edges, holes 28 mm from both edges and 96 mm apart |
| `drill_gauge` | Optional: holes from 5.0 to 5.4 mm to check which clearance your drill bit runs in without wobble |

Status: drill template ready to print with a 5 mm drill and 0.2 mm clearance
(`params.py`).

## Options

Where the holes go is the template's to choose (`options.py`); it builds for
any values within these limits. Everything else is a fixed number in
`params.py`.

| Option | Default | Limits | |
|---|---|---|---|
| `spacing` | 96 | 32 to 224 mm | screw centre distance of the handle |
| `edge_offset` | 28 | 20 to 100 mm | side edge of the door to the screw centre line; also the length of the fence on the top or bottom edge |
| `end_offset` | 28 | 10 to 100 mm | the corner's top or bottom edge of the door to the screw nearest to it |
| `corner` | `top_right` | `top_right`, `top_left`, `bottom_right`, `bottom_left` | the corner of the door the template hooks over, seen from the front |

Four corners make two printed parts: a template turned half round fits the
diagonally opposite corner, so `bottom_left` prints the same part as
`top_right`, and `bottom_right` the same as `top_left`. `corner` still says
where it goes: the model and the STEP sit at that corner. The template is
`end_offset + spacing + 19` mm long: at the upper limits (343 mm) longer than
most print beds.

Built and exported (`VARIANTS` in `options.py`), each with a model of its own
and its part on a door to look at (`..._on_door`):

| Variant | Options |
|---|---|
| `drill_template` | the defaults: the one in use |
| `drill_template_top_left` | `corner="top_left"` |
| `drill_template_128` | `spacing=128` |

For another configuration, add it to `VARIANTS` and give it its two `@model`
functions in `drill_template.py`. Two variants that would print the same part
are refused.

## Print sheet (suggestion)

Print each part in the orientation it comes in the 3MF; no supports needed.

| | |
|---|---|
| Material | PLA or PETG |
| Layer height | 0.2 mm |
| Walls | 4 |
| Infill | 25 % |
| Supports | none |
