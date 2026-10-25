# ResumeAI design system: "Fitting room"

Job seekers talk about *tailoring* a resume, so the interface borrows from a
tailor's fitting: pattern-tissue paper, navy suiting, a yellow tape measure
that reads the ATS score, and tailor's chalk marking what's missing.

## Colour
| Token | Light | Dark (`.light` class, legacy name) | Use |
|---|---|---|---|
| `--bg` | `#F3EEE4` | `#171B23` | pattern-tissue ground |
| `--bg2` | `#FFFEFB` | `#1F2430` | cards, nav, sidebar |
| `--bg3` / `--bg4` | `#ECE6DA` / `#E2DACB` | `#282E3B` / `#323947` | insets, hovers |
| `--text` | `#1C2433` | `#F2EEE6` | ink |
| `--accent` | `#1F3A68` | `#8FB0E8` | navy: primary buttons, links |
| `--tape` | `#F2C230` | same | the measuring tape: score marks, section tags, active nav, popular plan |
| `--green` / `--teal` | `#2F7A4F` | `#6CC495` | found keywords, positive trends |
| `--red` / `--pink` | `#C2412D` | `#F08A75` | chalk: missing keywords, errors |
| `--amber` | `#9A6A0C` | `#E8B54A` | tips, pending |

`--grad1..3` are kept as flat colours for compatibility; there are no
gradients except the tape's tick marks.

## Type
Young Serif (single weight) for page and section headings; Instrument Sans for
UI and body, with tabular numbers in stats; IBM Plex Sans Arabic for the AR
toggle. Card and list headings use the sans at 600.

## Components
- Section labels: a short strip of tape plus sentence-case text (no tracked caps).
- Step numbers: printed on a tape tab.
- Buttons: 6px radius, navy primary; no hover lift.
- Popular plan: 2px ink border with a tape tag.
- Missing keywords: dashed chalk outline.
- Sidebar active item: tape-yellow edge (logical `inline-start`, flips in RTL).

## Motion
Hero only: the tape's red marker slides up to the score and the chalk line
draws in. Both are skipped under `prefers-reduced-motion`.
