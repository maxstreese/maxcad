# fridge-glide

Sliding coupling for a built-in fridge ("Einbaukühlschrank Gleitschiene",
drag-door / Schlepptür fitting): the kitchen's furniture front hangs on its own
hinges, and the fridge door follows it through a slider running in a rail. The
doors pivot about different axes, so the slider runs along the rail as they
open. Idea from
[printables 587358](https://www.printables.com/model/587358-einbaukuhlschrank-gleitschiene),
redesigned:

- **No holes in the fridge door.** The slider is a small clip around the fridge
  door's side edge on its opening side: a short leg on the front face, a thin
  web on the side face and a hook behind the back face (outside the gasket),
  pinching the door by `GRIP_INTERFERENCE`. The leg's contact face follows the
  door's curved front. A neck reaches across the gap to the head.
- **The long part on the easy door.** The rail sits on the flat furniture door,
  screwed on through a flange, and covers the whole 90 mm travel. The slider's
  head sits right at the fridge door's edge, so the pull that opens the fridge
  (breaking its seal) always acts close to the clip, closed or open.
- **Smooth and self-centring glide.** The channel is a diamond (a square
  turned 45 degrees) with the slot at its corner facing the fridge door; the
  slider's head is a 6 mm round bar. Pulled or pushed, the head wedges into a
  90 degree V, centres itself and touches on two lines; the neck never touches
  the slot. Both rail ends flare into a lead-in, and the head's ends are
  chamfered to find it.
- **Printed for smoothness.** The rail prints flat on its flange, so its layers
  run along the head's path; the slider prints standing on its web, so its head
  is a truly round vertical cylinder.

| Part | What it is |
|---|---|
| `rail` | Diamond channel on a flange, 111 mm long, for the furniture door; 3 x 2 countersunk screws |
| `slider` | Clip around the fridge door's side edge, 50 mm tall, with the neck and the 6 mm head, 16 mm long |
| `gauge` | Measuring aid, not part of the coupling: a rigid C around the fridge door's side edge with five holes for a caliper's depth rod |
| `gauge_wedge` | Wedge that holds the gauge on the door while measuring |

`glide_on_doors` shows both between the closed doors. The top and the bottom
coupling are the same two parts: print two of each. They fit doors opening on
either side: both parts are the same above and below the rail's centre line,
so the mirrored part is the same part turned over, and the printed files come
out identical. `OPENING_SIDE` (`params.py`, left as our doors open, seen from
the kitchen) only places them in the preview.

Status: **first draft, not printed**. The door's thickness, the gaps, the room
beside and behind it and the travel are measured; the curve's radius is still
a PLACEHOLDER (`params.py`). On a vertical edge only the pinch holds the clip
up; if it creeps down, add a strip of VHB tape (or a TPU pad) on the leg.

## Measured (2026-11-09)

- Door thickness at the side edge: 46.09 mm (calipers; tricky on the curve).
- Gap to the furniture door: 22 mm at the edge, 17 mm at 75 mm in.
- Space beside the side edge: at least 6 mm (the web is 2.5; the rail starts
  5 mm outside the edge).
- Room for the hook behind the back face, up to the gasket: 6 mm (the hook
  reaches in 4).
- Travel: while the doors open, the fridge door's edge moves from 30 to 120 mm
  in from the furniture door's edge, so the slider runs 90 mm along the rail,
  away from the furniture door's edge.

## Gauging the door's front

The clip's leg sits on the first 17.5 mm of the fridge door's front, and the
model only guesses that stretch: a circle of a placeholder radius through two
gaps measured between the closed doors. Calipers cannot do better, their back
jaw reaches only 6 mm in, up to the gasket. The `gauge` turns the front's shape
into depth readings, taken from the surfaces the clip sits on. `gauge_on_door`
shows it in place.

Before use, measure the gauge itself, where calipers are good: over the leg's
outer face and the hook's outer face, less the hook's thickness (drawn: 64.09
less 5, so 59.09). That is the reference.

1. Open the fridge door. Put the gauge around its side edge at a coupling's
   height: hook behind the back face, web flat against the side face, holes up.
2. Push the wedge up from below, thick end down, rib towards the door, between
   the door's front and the sloped seat in the leg, next to the web. Keep the
   web against the side face while it tightens. It should stop before it
   covers the first hole (it takes doors about 1 mm thicker or thinner than
   46.09).
3. Rest the caliper's end on the leg's outer face and read the depth to the
   door through each hole, three times each. Readings that scatter by more
   than 0.1 mm mean the gauge moves.
4. The door's thickness at a hole is the reference less the reading. The holes
   are at 3, 8, 13, 18 and 23 mm in from the side edge, counted from the web
   (the first one sits low, the next high, and so on).
5. Repeat at the other coupling's height.

Five thicknesses at each height replace `DOOR_THICKNESS`, `GAP_INWARD` and
`DOOR_RADIUS` for the clip's leg, and show whether the front is a circle there
at all. The rail only needs the curve roughly.

## Still to measure

1. **The front's shape under the clip's leg**, with the gauge (above). The
   gap at about 110 mm in would fix the curve further in (`DOOR_RADIUS`,
   placeholder 2000), but is not critical: for any radius from 800 to 6000 the
   rail keeps 4.5 to 6.1 mm off the fridge door's front. Whether the back face
   is flat (assumed).
2. **The heights** of the two couplings on the door.
3. **The edge's shape**: a rounded edge sits in the clip's sharp inside corner
   without trouble; a chamfer or a step might not.
4. **Furniture door thickness**, for the screw length (placeholder 19).

## Fitting

1. Clip the slider onto the fridge door's edge at the coupling's height.
2. Slide the rail onto the head from the rail's outer end (the end towards the
   furniture door's edge), close both doors, and with the rail level and its
   outer end 2.5 mm short of the head, mark the screw holes on the furniture door.
3. Screw the rail on; check that the doors open fully without the head
   reaching the rail's inner end.

## Hardware

- 6x countersunk wood screws 3.5 x 12 per rail (shorter than the furniture
  door is thick), into its back.
- Optional: dry PTFE spray or a little silicone grease in the channel.

## Print sheet (suggestion)

| | |
|---|---|
| Material | PETG (the clip must flex; PLA may crack when pushed over the edge) |
| Orientation | as in the 3MF: rail flat on its flange, slider standing on its web |
| Layer height | 0.2 mm |
| Walls | 4 |
| Infill | 30 % |
| Supports | none (every overhang is 45 degrees) |

The gauge prints as drawn, the C lying flat (holes sideways, no supports); the
wedge lying on its side. Any stiff material: PLA is fine for both.
