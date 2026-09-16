---
title: Photo measure
description: Measure your lock from a photograph using a bank card, a coin or a tape measure as the scale reference. The photo never leaves your browser.
---

Put something of known size in the same photo as the lock, then measure on the image. Useful for backset, faceplate length, cylinder protrusion and handle screw spacing — the dimensions you can see, not the ones hidden inside the door.

{{photo}}

## How to get an accurate result

1. **Get the reference object in the same plane as the lock.** A bank card held in front of the door works. A card on the floor next to the door does not — perspective will lie to you.
2. **Photograph straight on.** Stand directly in front of the door. Angled shots distort the measurement by several millimetres, which is more than the tolerance you have.
3. **Use good light and focus.** Tap to focus on the lock edge, not the door.
4. **Measure twice with different reference objects.** A bank card is 85.6 × 53.98 mm. A tape measure in frame is better still, because it removes the reference-length assumption entirely.

## What you can and cannot measure this way

| Good from a photo | Needs the door open or the lock out |
| --- | --- |
| Faceplate length and width | Backset (door edge to keyhole centre) |
| Cylinder protrusion past the escutcheon | Centre distance (spindle to cylinder) |
| Handle screw spacing | Cylinder total length and halves |
| Escutcheon diameter | Spindle size |
| Door thickness at the edge | Lock case depth |

The right-hand column is where the real decisions are made, so treat the photo as a first pass: it tells you whether the lock looks like a euro cylinder or a lever lock, and then you open the door and measure properly with the [measuring guide](measure.html).

## Known object sizes

| Object | Size |
| --- | --- |
| Bank card (ISO/IEC 7810 ID-1) | 85.60 × 53.98 mm |
| A4 paper width | 210 mm |
| Euro coin, 2 € | 25.75 mm diameter |
| US quarter | 24.26 mm diameter |
| Singapore $1 coin | 24.5 mm diameter |
| Standard euro cylinder diameter | 33 mm across the widest point |

## Privacy

The photo is read by your browser with the FileReader API and drawn on a canvas on this page. There is no upload, no server, no analytics on the image, and closing the tab discards it. If you want to keep the measurement, use the spec-sheet button and save the text.

## Questions

**Why is there no AI photo identification?**
Because this site is currently a static site with no backend, and a static site cannot run a vision model. What it can do — and does — is give you the measurements that make identification certain. When a backend exists, photo identification will be added here, and the wizard already produces the structured spec sheet that such a model would need as output.

**Can I use this on my phone?**
Yes. Take the photo with the phone camera, then open this page and choose the file. On a small screen, pinch-zoom before clicking the two points.

**How accurate is it?**
With a straight-on photo and a card in the same plane, expect ±1–2 mm on a 200 mm measurement. Good enough to identify a lock family; not good enough to order a cylinder, which needs a calliper.
