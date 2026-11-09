# fridge-glide

Sliding coupling for a built-in fridge ("Einbaukühlschrank Gleitschiene",
drag-door / Schlepptür fitting): the kitchen's furniture front hangs on its own
hinges, and the fridge door follows it through a slider (screwed to the
furniture door) running in a rail (on the fridge door). The doors pivot about
different axes, so the slider runs along the rail as they open. Idea from
[printables 587358](https://www.printables.com/model/587358-einbaukuhlschrank-gleitschiene),
redesigned:

- **No holes in the fridge door.** The rail is part of a clip around the
  door's side edge on its opening side: a leg on the front face, a thin web on
  the side face and a short hook behind the back face (outside the gasket),
  pinching the door by `GRIP_INTERFERENCE`. The door's front is curved from
  side to side; the leg's contact face follows that arc (`DOOR_RADIUS`) over
  its whole length. The rail runs in from the edge, straight and parallel to
  the furniture door, in front of the door's foremost point under it; near the
  edge, off the door's crown, the face is also tilted, so the leg is a wedge,
  thickest at the edge.
- **Smooth and self-centring glide.** The channel is a diamond (a square
  turned 45 degrees) with the slot at its front corner; the slider's head is a
  round bar. Pulled or pushed, the head wedges into a 90 degree V, centres
  itself and touches on two lines; the neck never touches the slot. Both rail
  ends flare into a lead-in, and the head's ends are chamfered to find it.
- **Printed for smoothness.** The rail prints standing, as mounted: the clip's
  plan lies in the layers (the strong way for its flexing), the channel and the
  rail's underside are at 45 degrees, and the layers run along the slider's
  path. The slider prints standing on one end, so its head is truly round.

| Part | What it is |
|---|---|
| `rail` | Clip around the fridge door's side edge, 50 mm tall, with the diamond channel along its front, 120 mm long |
| `slider` | Round head, neck and a plate with a countersunk screw above and below the rail, for the furniture door |

`glide_on_doors` shows both between the closed doors. The top and the bottom
coupling are the same two parts: print two of each. They are made for doors
opening on the left, seen from the kitchen; `OPENING_SIDE = "right"` mirrors
them.

Status: **first draft, not printed**. Every number about the doors is a
PLACEHOLDER (`params.py`). On a vertical edge only the pinch holds the clip up;
if it creeps down, add a TPU pad or a strip of VHB tape on the leg.

## To measure

Where the rail's middle will sit, unless said otherwise.

1. **Fridge door thickness** at its side edge, front face to back face
   (`DOOR_THICKNESS`, placeholder 50).
2. **Gap between the doors** when closed: fridge door front face to the
   furniture door's back face (`DOOR_GAP`, placeholder 28).
3. **Space beside the fridge door's side edge**, closed and while swinging, for
   the 2.5 mm web (`SIDE_CLEARANCE`, placeholder 4).
4. **Where the gasket starts** on the back face, in from the side edge: the
   hook must stay outside it (`GASKET_FROM_EDGE`, placeholder 6; hook 4).
5. **How far the slider travels** along the door from closed to fully open
   (`RAIL_LENGTH`, placeholder 120), where it sits when closed (close to the
   edge is best: opening breaks the gasket's seal there, the largest pull, and
   the shorter its lever on the clip the better), and at which heights the
   couplings go.
6. **The front's curve**: its radius (`DOOR_RADIUS`, placeholder 2000) and
   where its crown (foremost point) lies relative to the rail's middle
   (`CROWN_OFFSET`, placeholder 200: crown near the door's middle). Hold a
   straight edge across the front at the clip's height, touching the crown,
   and measure the gap at a few distances from it: R = distance² / (2 x gap);
   for a true circle the gaps at 50, 100 and 150 mm grow 1 : 4 : 9. Whether
   the back face is flat (assumed). Off the crown the rail stands further
   forward (5.1 mm with the placeholders), which the gap between the doors must
   allow.
7. **The edge's shape**: a rounded edge sits in the clip's sharp inside corner
   without trouble; a chamfer or a step might not.
8. **Furniture door thickness**, for the screw length (placeholder 19).

## Hardware

- 2x countersunk wood screws 3.5 x 12 per slider (shorter than the furniture
  door is thick), into its back.
- Optional: dry PTFE spray or a little silicone grease in the channel.

## Print sheet (suggestion)

| | |
|---|---|
| Material | PETG (the clip must flex; PLA may crack when pushed over the edge) |
| Orientation | as in the 3MF: rail standing as mounted, slider standing on one end |
| Layer height | 0.2 mm |
| Walls | 4 |
| Infill | 30 % |
| Supports | none (every overhang is 45 degrees) |
