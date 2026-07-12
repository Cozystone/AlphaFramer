# AlphaFramer

**A spatial-context perception protocol. The eye that never keeps a frame.**

AlphaFramer turns raw camera input into the smallest honest description of a space — object
identities, where they are, the surfaces and paths through them — and **stores no frame**. It is the
perception layer meant to become the shared "reference frame" for smart glasses and humanoid robots.

## Three principles

**1. No-Frame doctrine.** A camera frame is distilled and discarded — never written to disk. Only
distilled geometry leaves: an object's label, its normalised position, its geometric *signature*
(not pixels), and the walkable affordances. Privacy is structural, not a policy toggle.

**2. Semantic-Bottleneck honesty.** *If you cannot rebuild it, you did not understand it.* AlphaFramer
does not lean on a generative model's plausible hallucinations. A deliberately **deterministic**
reconstruction is the training tool: the machine rebuilds a scene from its context alone and measures
what it lost (`reconstruction_loss`). The gaps it names — size, colour, layout — become the next
lessons. A generative decoder is barred from the truth signal on purpose.

**3. Episodic memory recombination.** Spaces you passed through become a timeline you can query.
"Where did I walk earlier?" replays the recorded geometry — the room where it was, rebuilt from
distilled structure, never from a saved image.

## What's here (v0)

| module | what it does |
|---|---|
| `object_recognition` | re-recognise the same object across sightings by its visual signature (multi-view drift-robust, conservative threshold, honest about uncertainty) |
| `spatial_memory` | record a space as distilled geometry (no frame) and rebuild it as a point-cloud scene |
| `reconstruction_loss` | the semantic-bottleneck audit — a deterministic rebuild + a topology loss + the measured curriculum |
| `face_cortex` | geometric face identity (an embedding compared by cosine; an unknown face is an honest gap, never a guessed name) |
| `geometry` | the structural shape vocabulary (a form per graph type) + LoD budget for bounded rendering |

Pure Python, no network, no frame storage. `pip install -e .` then `pytest`.

---

*AlphaFramer is the open perception protocol of the ATANOR project. The reasoning core is separate.*
