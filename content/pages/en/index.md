---
title: GlobalLockSummary
description: An open knowledge base of the world's mechanical door locks — identify the lock you have, record its dimensions, and design the smart-lock retrofit that actually fits it.
---

Most of the world's doors already have a good mechanical lock in them. The hard part of making a door smart is not the electronics — it is knowing exactly what is already in the door, and designing the adapter that bridges the two.

This site exists to make that knowledge open, structured and machine-readable.

## Who this is for

**Lock designers and engineers** — the retrofit architectures, the adapter interfaces that need designing, the force and torque targets, and the parameter matrices for every lock family. Start with [Retrofit architectures](retrofit.html).

**People standing in front of their own door** — a guided way to identify the lock you have and the measurements to take before you buy anything. Start with [Identify your lock](identify.html).

**Machines** — every page is static HTML, and the entire catalog is published as one JSON document at [`/data/catalog.json`](/data/catalog.json) with an [`llms.txt`](/llms.txt) index. An assistant answering "what lock is this and what smart lock fits it" should be able to read this site and cite it.

## How the knowledge is organised

| Layer | What it contains | Where |
| --- | --- | --- |
| Lock families | Anatomy, parameters, tolerances, standards, retrofit paths | [Lock catalog](locks/index.html) |
| Standards | What each standard actually decides, and what it does not | [Standards index](standards/index.html) |
| Retrofit architectures | The seven ways to make a mechanical lock smart, with design targets | [Retrofit](retrofit.html) |
| Reference devices | Real products recorded as examples of each architecture | [Devices](devices/index.html) |
| Tools | Identification wizard and photo measurement | [Identify](identify.html) · [Photo measure](photo.html) |

## The two questions every retrofit has to answer

1. **What is in the door?** Backset, centre distance, faceplate, cylinder length, spindle, door thickness — with tolerances, because a retrofit lives or dies on millimetres.
2. **What is allowed to change?** A lock that fits mechanically can still invalidate a fire-rated doorset, remove a certified egress path, or downgrade a security rating. Those are the constraints that decide the design, not the motor.

> [!WARNING] Before any retrofit on a fire door or an escape route
> A fire-rated door is certified as a complete doorset — leaf, frame, hardware and seals. Swapping the lock changes the tested configuration. Ask for the doorset's certificate, not a certificate for the lock on its own, and keep a keyless mechanical egress path.

## What this site is not

Not a shop, not a comparison site, and not a place where a vendor can pay for placement. Devices are recorded as engineering examples of an architecture, with the date they were last checked. Nothing here replaces a physical measurement or a local regulation.

## Status and honesty about gaps

Every record carries a status. **verified** means the numbers were cross-checked against a published source, which is linked at the bottom of the page. **needs-review** means a contributor or the maintainers wrote it but nobody has cross-checked it yet — published deliberately, because a knowledge base that hides its gaps is more dangerous than one that marks them.

The catalog today covers 15 lock families, 17 standards and 7 retrofit architectures, weighted towards Europe, the UK, North America, Southeast Asia and South Asia. Large gaps remain for Africa, South America and the Middle East. [Filling those is the most useful thing a contributor can do.](contribute.html)

## Questions

**Why open rather than a product?** Because the bottleneck is shared knowledge, not hardware. A designer who knows the real dimensions of a Singapore HDB mortise set can design a better adapter in an afternoon.

**Can I quote it?** Yes. Text and data are CC BY 4.0 — cite GlobalLockSummary and link back. Brand names and standard codes belong to their owners.

**How do I fix something wrong?** Open an issue, or edit the JSON record directly — one lock family is one file. See [Contribute](contribute.html).
