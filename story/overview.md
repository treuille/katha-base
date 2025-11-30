# Millbrook Haunted House Storyworld – High-Level Overview

This document explains **what this project is** at a conceptual level:
the world, the narrative logic, and how the branching six-book structure hangs together.

It is meant as an orientation guide for a coding agent so it can reason about "what's going on here" without needing to know any specific prose or page text.

### File Structure

The project data is organized as:

- `characters/` - Character definitions (6 YAML files)
- `locations/` - Location and room definitions (8 YAML files)
- `story/template.yaml` - The shared 23-page narrative template

---

## 1. Big Picture

This repository encodes a **single shared storyworld**:

- A real-world-ish place called **Millbrook** during a winter holiday.
- A **single house** that becomes mildly haunted after a strange ornament is hung on the Christmas tree.
- **Six children**, each with their own point of view and core strength.
- A **Tibetan trickster spirit** whose magic is about *mismatch* and *scrambled roles*, not gore or horror.

From this shared world, we want to generate **six parallel picture books**, each one:

- Focusing on a **different child** as the main character.
- Sharing the **same global sequence of “story beats”** (page slots) as all the others.
- Diverging in **which rooms they visit**, **which problems they fix**, and **what we see of their inner arc**.

In other words: it’s **one story, six perspectives**, all tightly synchronized.

---

## 2. The World of Millbrook and the House

The physical setting is:

- **Millbrook**, a small, wintry town in the present day.
- A **large, cozy family house** with:
  - Social spaces (living room, dining room).
  - Functional spaces (kitchen, stairs).
  - “Magic-feeling” spaces (library, playroom, sun room).
  - The surrounding **yard/driveway** used in the finale.

The tone is:

- Cozy, magical, emotionally safe.
- There *is* a spirit, but its power is always about **confusion, misalignment, and playfulness** rather than anything truly terrifying.
- The house feels like a living puzzle box: each room is a facet of the trickster spirit, expressing a different type of “wrongness” that needs to be re-aligned.

You can think of the house as a **small graph**:

- Nodes = rooms (plus the living room hub and the exterior).
- Edges = hallways / stairs / doors.
- The Christmas tree is the **source** of the problem; the exterior is the **sink** where the problem is finally discharged.

---

## 3. The Core Magical Premise

The main magical object is a **strange ornament** hung on the Christmas tree.

- It contains a **trickster spirit** whose nature is to scramble things:
  - Wrong people in wrong seats
  - Wrong gifts for wrong kids
  - Wrong story endings, wrong game rules, wrong paths, wrong seasons
- When the ornament is disturbed, this energy **fractures into multiple echoes** that slip into different rooms of the house.

Each echo manifests as a **room-specific kind of mismatch**:

- The rooms themselves become “mini-boss habitats.”
- The trickster’s influence is *local* in each room but *global* in effect: the house as a whole feels subtly wrong.

Later, the spirit is:

1. **Re-concentrated** in the living room during the climax,
2. **Captured** in a container, and
3. **Carried outside** to a new, appropriate home, where its protective side can remain while the disruptive side is contained.

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

6. **Living Room Confrontation & Spirit Battle**
   - All kids gather, the ornament is identified, and the trickster spirit erupts.
   - Each child uses what they learned in their room in a joint, big-scene sequence.
   - One child performs the final containment, but it only works because everyone else does their part.

7. **Carrying the Spirit Out & Epilogue**
   - The captured spirit is carried outside in a ritualized way (sled, airplane, etc.).
   - The house becomes peaceful again, with a gentle protective aura instead of scrambled chaos.
   - Each child returns to their ordinary world, slightly changed, having learned that:
     - Their **strongest strength** is real and valuable.
     - The house works best when everyone’s strengths are used in the right places.

---

## 7. How the Data Is Intended to Be Used

A coding agent should treat the data files (characters, pages, locations) as **three complementary views** of the same system:

- **Characters** (`characters/*.yaml`) describe:
  - Who the six kids are.
  - Which symbolic roles they play (e.g., which room they "own" as their second attempt).
  - Who their swap partner is during the pair section.

- **Locations** (`locations/*.yaml`) describe:
  - How the trickster spirit's influence manifests in each place.
  - What it means for that room to be partially vs. fully resolved.
  - Which child is ultimately the "hero" of that room.

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

---

## 8. Mental Model for Future Extensions

Some ways this architecture can be extended:

- **Add more kids** by:
  - Creating a new character file.
  - Assigning them a first/second room combination and a partner.
  - Reusing the same page skeleton.

- **Add more rooms or "facets"** by:
  - Defining new location files with new mismatch themes.
  - Inserting additional "first-attempt / crossover / second-attempt" clusters into the page sequence.

- **Alter the difficulty** by:
  - Changing what “partial success” looks like in each room.
  - Adjusting how obviously each room’s mismatch connects to a given child’s strength.

As long as the **conceptual triangle** stays clear—

- One house, one spirit source, one final banishing place.
- Six kids with strong but different passions.
- One shared spine of beats with joint, pair, and individual slots—

the system should stay coherent while remaining very flexible for generation and experimentation.

