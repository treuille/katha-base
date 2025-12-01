# Millbrook Haunted House Storyworld – High-Level Overview

This document explains **what this project is** at a conceptual level:
the world, the narrative logic, and how the branching six-book structure hangs together.

It is meant as an orientation guide for a coding agent so it can reason about "what's going on here" without needing to know any specific prose or page text.

**For project file structure and organization, see the [README](../README.md).**

---

## 1. Big Picture

This repository encodes a **single shared storyworld**:

- **Millbrook** is a real town in upstate New York. Deep in the woods outside the town sits a large house, also called Millbrook, where **Graminy** lives.
- During the **early Christmas season**, all of her grandchildren come to the house for the holidays.
- The house becomes haunted after a strange ornament is hung on the Christmas tree.
- **Characters** inhabiting this world:
  - **Six children** (cousins and siblings: Arthur, Cullan, Emer, Hansel, Henry, and James - see `characters/*.yaml`), each with their own point of view and core strength
  - **Dorje Legpa**, a Gyalpo trickster deity (see `characters/dorje_legpa.yaml`) whose magic is about *mismatch* and *scrambled roles*, not gore or horror
  - **Regan** (see `characters/regan.yaml`), mother of Cullan and Emer, who identifies the spirit

From this shared world, we generate **six parallel picture books**, each one:

- Focusing on a **different child** as the main character
- Sharing the **same global sequence of "story beats"** (page slots) as all the others
- Diverging in **which rooms they visit**, **which problems they fix**, and **what we see of their inner arc**

In other words: it's **one story, six perspectives**, all tightly synchronized.

---

## 2. The House

Graminy's house is a **large, cozy family home** with:
- Social spaces (living room, dining room)
- Functional spaces (kitchen, stairs)
- "Magic-feeling" spaces (library, playroom, sun room)
- The surrounding **driveway and yard** used for the sky procession finale

The tone is:

- Cozy, magical, emotionally safe.
- There *is* a spirit, but its power is always about **confusion, misalignment, and playfulness** rather than anything truly terrifying.
- The house feels like a living puzzle box: each room is a facet of the trickster spirit, expressing a different type of “wrongness” that needs to be re-aligned.

---

## 3. The Core Magical Premise

The main magical object is a **strange ornament** hung on the Christmas tree.

- It contains **Dorje Legpa**, a Gyalpo trickster deity whose nature is to scramble things:
  - Wrong people in wrong seats
  - Wrong gifts for wrong kids
  - Wrong story endings, wrong game rules, wrong paths, wrong seasons
- At first, something just feels **maybe amiss** in the house—subtle wrongness that builds anticipation and creepiness.
- This unease **explodes** into distinct problems throughout the house, with each room manifesting its own **specific kind of mismatch**:
  - The rooms themselves become spaces where Dorje Legpa's influence is most concentrated.
  - The house as a whole feels subtly wrong, but each room expresses a different facet of the trickster's scrambling power.

Later, Dorje Legpa is:

1. **Re-concentrated** in the living room during the climax
2. **Captured** in a container
3. **Carried outside** to a new, appropriate home, where the protective side can remain while the disruptive side is contained

---

## 4. Narrative Architecture: Six Books, One Spine

The storytelling architecture is:

- There is **one underlying story spine** broken into a linear sequence of **page slots** (page 1, page 2, …).
- All six books share this **same sequence of slots** and **the same kind of beat** per slot (e.g., “ordinary-world intro”, “first attempt”, “pair crossover”, “climax”, “epilogue”).
- Each slot can be filled in three different ways:
  - **Joint page**: all six kids are present; the content is shared across all books.
  - **Pair page**: two specific kids appear together; that page is shared between their two books.
  - **Individual page**: we focus on one main character; content there is unique to that child’s book.

This creates a **branching-but-synchronized** structure:

- In time, all books move through the same phases:
  **cozy Christmas → first weirdness → first room attempts → crossover exchange → second room attempts → group confrontation → resolution.**
- In perspective, each book diverges in:
  - Which room each child tries first and second.
  - What exact problem the child sees in that room.
  - How they use their personal strength to fix it.

A coding agent should think of it like a **shared timeline with character-specific overlays**:

- The YAML for **pages** (`story/template.yaml`) defines the shared timeline and the "role" of each slot (joint/pair/individual, symbolic room roles).
- The YAML for **characters** (`characters/*.yaml`) defines, for each child, which rooms map onto those symbolic roles and who their pair partner is.
- The YAML for **locations** (`locations/*.yaml`) defines how each location behaves and what it means to partially vs. fully fix it.

---

## 5. The "Two Attempts" Room Logic

Each "haunted" room follows a repeating narrative pattern:

1. **First visit (first attempt):**
   - A child who does *not* have the perfect strength for this room wanders in by accident.
   - They sense something is wrong and try a **simple, surface-level fix**.
   - This visibly **weakens** the haunting but does not fully resolve it.

2. **Crossover moment:**
   - Kids compare experiences in a pair conversation.
   - They realize: "You'd probably be better at my room than I am," and agree to **swap rooms**.

3. **Second visit (second attempt):**
   - The child whose strength actually matches that room comes in.
   - They perceive a **deeper pattern** in what's wrong and use their core passion to solve it properly.
   - The room's echo of the spirit is **fully cleared**, and that child's self-understanding grows.

For a coding agent, the idea is:

- **First attempt** = partial success + set-up for another child.
- **Second attempt** = definitive success + character-specific payoff.
- This pattern is repeated across all haunted rooms with different kids/skills, but the same abstract shape.

---

## 6. The Flow of the Overall Story

At the highest altitude, each book goes through these phases:

1. **Ordinary World**
   - We meet the house, the holiday, and all kids at play.
   - The main child begins to feel that something about the tree is “off.”

2. **First Room Phase (First Attempts)**
   - The main child leaves the tree and stumbles into the *wrong* haunted room for them.
   - They try a simple fix and partly calm it.

3. **Pair Crossover**
   - The main child runs into their designated partner in the hallway.
   - They swap stories and agree to **swap rooms**, recognizing each other's strengths.

4. **Second Room Phase (Second Attempts)**
   - The main child now heads to the room that really matches their core strength.
   - They see the deeper pattern and solve it properly using their passion.
   - At this point, each child has "their" room where they are the final hero.

5. **Escalation to House-Level Problem**
   - As all rooms settle, the children realize something is still wrong at the house level.
   - This points them back to the living room and the tree.

6. **Living Room Confrontation & Spirit Containment**
   - All kids gather, the ornament is identified (Regan identifies it as Dorje Legpa, a Gyalpo trickster deity), and the spirit erupts.
   - Each child uses what they learned in their room in a joint, big-scene sequence.
   - The boys realize the spirit is furious because it's cramped inside the house—too big for a bedroom, it needs sky.
   - They contain the spirit (still blazing red and hilarious, complaining and wiggling) and tie it onto the bright red sled. Very funny.

7. **The Sky Procession & Spirit Transformation**
   - **Henry** jumps into the toy airplane, which becomes the "vehicle of sky."
   - **James** acts as air traffic controller on the ground: "Spirit Sled Three-Seven-Red, cleared for takeoff!"
   - **Cullan and Arthur** ride in the sled being dragged by the airplane, holding the deity in a box.
   - **Emer** trails behind on a tricycle with **Hansel** on the handlebars, pointing exultantly at the sky with his bottle.
   - The plane lifts the sled into the air—not too high, just enough for comedic effect—dragging the spirit across the lawn, up over a little bump, maybe through some clouds.
   - The moment the spirit is pulled into **open space**, it transforms:
     - His flames soften into wind
     - His weapons turn into sparkles
     - His screaming face relaxes
     - He remembers he's not a monster—he's actually a sky guardian who forgot himself
   - The spirit sees himself reflected in the sky (the sky becomes his mirror—a Tibetan-friendly metaphor where the sky itself is the mirror of nature).
   - The house becomes peaceful again, with a gentle protective aura instead of scrambled chaos.

8. **Epilogue**
   - Each child returns to their ordinary world, slightly changed, having learned that:
     - Their **strongest strength** is real and valuable.
     - The house works best when everyone's strengths are used in the right places.

---

## 7. How the Data Is Intended to Be Used

A coding agent should treat the data files (characters, pages, locations) as **three complementary views** of the same system:

- **Characters** (`characters/*.yaml`) describe:
  - Who the eight characters are (six children, Dorje Legpa, and Regan)
  - For the six children: which symbolic roles they play (e.g., which room they "own" as their second attempt) and who their swap partner is during the pair section

- **Locations** (`locations/*.yaml`) describe:
  - How Dorje Legpa's influence manifests in each place
  - What it means for that room to be partially vs. fully resolved
  - Which child is ultimately the "hero" of that room

- **Pages** (`story/template.yaml`) describe:
  - The global linear order of story beats.
  - For each slot: whether it's joint, pair, or individual.
  - Symbolic references to "first attempt location", "second attempt location", and "pair partner".

To build any of the six books, an agent can:

1. Pick a **main character**.
2. Walk through the **global page list in order**.
3. For each page:
   - If it’s **joint**, drop in shared content (possibly with minor viewpoint tweaks).
   - If it’s **pair**, generate content involving the main character and their partner.
   - If it's **individual**, plug in the correct symbolic room (first or second attempt) and use that room's behavior + the main character's traits to craft the beat.

The result is six books that:

- Share structure and major events.
- Differ only in viewpoint, room assignments, local problem/solution details, and internal emotional arc.

