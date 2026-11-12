# canyon-ep403

Replacement for the Canyon **EP403-16 "Leitungsführung"** (part E403-16), the
small plate under the bottom bracket that covers the frame's cable port. A slit
with a keyhole at its end lets it slide over a hose that is already in place;
two small screws hold it. Canyon lists it as sold out, without dimensions or a
list of frames
([product page](https://www.canyon.com/de-de/canyon-ep403-16-leitungsfuehrung/10010239.html);
it is also part of the GP7067-01 cable routing kit, "for all Canyon AL frames
with special designed clip loops").

| Part | What it is |
|---|---|
| `cover` | The plate: outline from above, flat for 10.11 mm, then bent with R 41; "Simoncello" engraved 0.4 mm into the flat outer face |

Status: **draft**. The outline and the bend come from a friend's Solid Edge
sketches of his original (2026-11-08); `params.py` marks every number as
MEASURED (his), ESTIMATE (read off his screen photos) or PLACEHOLDER.

This is a personal project, not affiliated with or endorsed by Canyon
Bicycles; "Canyon" and the part numbers only say what the part is meant to
fit. It has not been printed or fitted to a bike: use it at your own risk.

## Open questions (for whoever has the original)

1. **Thickness** (placeholder 2.0 mm).
2. **The two screw holes**: positions, diameter, screw size, or none at all
   (placeholders: Ø 2.2, 6 mm from the slit end, 5 mm either side of the slit).
3. **The 37 mm length**: measured straight across, or along the curve? The model
   reads it as straight across; along the curve, the part would be about 2.5 mm
   too long in projection.
4. **Slit width** at the keyhole and at the end (estimates 1.0 and 2.7 mm).
5. **Which side touches the frame**: the model takes the sketched curve as the
   inner (frame side) surface, with the thickness outside the bend.
6. **Which bike**.

## Print sheet (suggestion)

The 3MF comes lying on its right side, which is flat: the bend is printed in
the layer plane, true to shape, with no supports, and the layers run along the
slit's two fingers.

| | |
|---|---|
| Material | PETG or ASA (water, grit, road salt under the bottom bracket; PLA softens in sun and heat) |
| Layer height | 0.12-0.16 mm |
| Walls | 4 (at 2 mm thick, the plate is all walls anyway) |
| Infill | 100 % |
| Supports | none |
| Brim | 3-5 mm: it stands 23.5 mm tall on a 2 mm wide face |
