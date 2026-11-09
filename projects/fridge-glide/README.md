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
| `rail` | Diamond channel on a flange, 108 mm long, for the furniture door; 3 x 2 countersunk screws |
| `slider` | Clip around the fridge door's side edge, 50 mm tall, with the neck and the 6 mm head, 16 mm long |

`glide_on_doors` shows both between the closed doors. The top and the bottom
coupling are the same two parts: print two of each. They are made for doors
opening on the left, seen from the kitchen; `OPENING_SIDE = "right"` mirrors
them.

Status: **first draft, not printed**. The door's thickness, the gaps, the room
beside and behind it and the travel are measured; the curve's radius is still
a PLACEHOLDER (`params.py`). On a vertical edge only the pinch holds the clip
up; if it creeps down, add a strip of VHB tape (or a TPU pad) on the leg.

## Measured (2026-11-09)

- Door thickness at the side edge: 46.09 mm (calipers; tricky on the curve).
- Gap to the furniture door: 22 mm at the edge, 17 mm at 75 mm in.
- Space beside the side edge: at least 6 mm (the web is 2.5; the rail starts
  3.5 mm outside the edge).
- Room for the hook behind the back face, up to the gasket: 6 mm (the hook
  reaches in 4).
- Travel: while the doors open, the fridge door's edge moves from 30 to 120 mm
  in from the furniture door's edge, so the slider runs 90 mm along the rail,
  away from the furniture door's edge.

## Still to measure

1. **The gap at about 110 mm in**, which fixes the front's curve
   (`DOOR_RADIUS`, placeholder 2000). Not critical any more: for any radius
   from 800 to 6000 the rail keeps 4.5 to 6.1 mm off the fridge door's front.
   Whether the back face is flat (assumed).
2. **The heights** of the two couplings on the door.
3. **The edge's shape**: a rounded edge sits in the clip's sharp inside corner
   without trouble; a chamfer or a step might not.
4. **Furniture door thickness**, for the screw length (placeholder 19).

## Fitting

1. Clip the slider onto the fridge door's edge at the coupling's height.
2. Slide the rail onto the head from the rail's outer end (the end towards the
   furniture door's edge), close both doors, and with the rail level and its
   outer end 1 mm short of the head, mark the screw holes on the furniture door.
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
