# curtain-rail

Stopper for a curtain rail (Gardinia profile 4460). It sits entirely inside the
lower (glider) channel and is clamped anywhere along the rail with a set screw.

| Part | What it does |
|---|---|
| `stopper` | The stopper: follows the channel's rounded bottom, clamped by an M3 set screw pressing against the web |
| `gauge_width` | Three wide flat stairs: width between the channel's straight walls, 9.2–12.0 mm |
| `gauge_slot` | Three narrow flat stairs: width of the slot, 4.6–7.4 mm |
| `gauge_height` | Three tall stairs: rail underside to the web's underside, 3.6–6.4 mm |

Every part is at most 13 mm long: the gap between the rail end and the wall is
about 15 mm, and everything goes in from that end.

Status: **draft**. The channel's inner shape is traced from the manufacturer's
drawing (see `params.py`), so measure it with the gauges first.

## Measuring

Each gauge is a plain stair of five steps, 0.2 mm apart. Hold it against the
rail end, smallest step first, and push it in until it stops (the height
gauge with its bottom flush with the rail's underside, through the slot). The
last step inside the rail is the measurement; the true value lies between it
and the next step.

The three stairs of a kind are numbered by small dimples in their right side
wall, one per step starting at the back (largest) step: 1 dimple = gauge 1 =
smallest sizes. Side by side, each one starts 0.2 mm above where the previous
one ends. Step `n` (counted from the front, starting at 1) of gauge `g`
measures

    start + ((g - 1) * 5 + n - 1) * 0.2     start: width 9.2, slot 4.6, height 3.6

Example: the second width stair stops with its third step in the rail, so the
width is at least 9.2 + (5 + 2) * 0.2 = 10.6 mm.

Then update `params.py`: width / 2 -> `RAIL_INNER_HALF_WIDTH`, slot ->
`RAIL_SLOT`, height -> `RAIL_WEB_BOTTOM`. Print one stopper and adjust
`FIT_SLIDE` if it is too tight or loose.

## Hardware

- 1x heat-set insert, CNC Kitchen M3 x 3 short, per stopper. Press it into
  the 4.0 mm hole in the flat top face with a soldering iron, flush with the
  face (it must not stand proud: that face rests against the rail's web).
- 1x M3x5 set screw, flat point (DIN 913 / ISO 4026), per stopper, screwed
  into the insert from below (through the free hole in the stem). Turn it in
  until its tip is just below the top face before inserting the stopper into
  the rail. Tighten with a 1.5 mm hex key through the slot, snug only.

  (A screw cutting its own thread into a 2.5 mm hole did not hold.)

## Print sheet (suggestion)

Print each part in the orientation it comes in the 3MF (flat top on the bed);
no supports needed.

| | |
|---|---|
| Material | PETG (or PLA) |
| Layer height | 0.2 mm (the height stairs' steps land on 0.2 mm layer lines) |
| Walls | 4 |
| Infill | 100 % (the parts are tiny; solid gives the insert the most to grip) |
| Supports | none |
