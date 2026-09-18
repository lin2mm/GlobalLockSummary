---
title: Retrofit architectures
description: The seven ways to make an existing mechanical lock smart — what changes on the door, whether the key survives, which adapters have to be designed, and the torque and force targets.
---

There are only seven fundamentally different ways to put a motor on an existing lock. Every product on the market is one of them, and which one you choose is decided by the lock you already have, not by the electronics.

The table below is generated from the catalog — each row links to a full page with adapter interfaces, design targets and failure modes.

## Choosing an architecture

Work through these in order:

1. **Is there a cylinder you can clamp or replace?** If yes, you are in the euro/oval cylinder world and [motor on the thumb-turn](retrofit/motor-on-thumbturn.html) or [integrated cylinder](retrofit/integrated-cylinder.html) both work.
2. **Is the bolt thrown by the handle or by the key?** If the handle throws it, [replacing the interior handle](retrofit/interior-handle-motor.html) is cleaner than any clamp.
3. **Is there a round bore with a thumb-turn?** Then a [surface deadbolt motor](retrofit/surface-deadbolt-motor.html) is a five-minute install with no drilling.
4. **Is it a lever lock with a keyhole in the faceplate?** There is no clean retrofit. Read the [5-lever page](locks/uk-5-lever-mortice.html) before designing anything.
5. **Is the whole lock set being replaced anyway?** Then the design problem is the lock case matrix, not an adapter — [full lock replacement](retrofit/full-lock-replacement.html).
6. **Is it a metal gate?** That is a different problem entirely — [gate actuator](retrofit/gate-actuator.html).

## The two numbers that decide the gearbox

Every architecture ends at the same question: how much torque, and how far does it rotate?

- **1.2 N·m** is the maximum key/turn torque that ANSI/BHMA A156.36 allows for a compliant auxiliary lock. Design the gearbox to beat that with margin — a worn, dirty or cold lock needs 2–2.5 N·m — but never design a motor that can exceed the lock's own mechanical limits, because then the motor breaks the lock instead of the lock stopping the motor.
- **Rotation range** is where designs quietly fail. A single deadbolt is under 180°. A multipoint system that has to retract hooks needs several full turns, and the battery budget changes completely.

## What "no door modification" really means

Adhesive mounts, clamps and spindle couplers all leave the door untouched — until they do not. Adhesive fails on hot, painted or textured surfaces. Clamps mark soft brass. Spindle couplers need the escutcheon to hide the old screw pattern.

When a product claims "no drilling", the honest engineering statement is: *no drilling, provided the door surface is X, the cylinder protrudes Y, and the spindle is Z.* Publishing that sentence is what separates a knowledge base from a product page.

## Egress is not a feature

Every architecture in this catalog keeps one hard requirement: the door must open from the inside by hand, with no power, no phone and no tool. That is a fire regulation in most jurisdictions and a common-sense rule everywhere else. A design that cannot guarantee it should not ship, whatever the convenience.

## Questions

**Which architecture is best for a designer starting out?**
Motor on the thumb-turn. The door is untouched, the mechanical key survives, the adapter is a mechanical clamp rather than a certified lock component, and the euro cylinder it attaches to is the most standardised interface in the world.

**Which is hardest?**
Full lock replacement. It changes the door, it interacts with fire certification, and the "adapter" is a matrix of lock case sizes across every market you sell into. It is also the architecture with the largest installed base in Asia.

**Why is there no architecture for lever locks?**
Because a lever lock has no cylinder and no spindle — the key operates the levers directly. There is nothing standard to drive. Replacing the case means a new door prep, which on a fire door means a new certified doorset.
