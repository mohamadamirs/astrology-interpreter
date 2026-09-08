# Domain Knowledge: Astrology Fundamentals

This document provides the foundational conceptual ontology of astrological mechanics for software engineers and AI/RAG retrieval systems. It defines core concepts, celestial physics, and non-mystical reasoning rules.

---

## 1. Mechanical Definition

A natal chart is a **2D geometric coordinate projection of the solar system as observed from a physical geographic coordinate on Earth's surface at an exact civil second in time**.

Astrological analysis operates on **4 Fundamental Pillars (The Theater Analogy)**:

```
+-------------------------------------------------------------------------+
|                       4 FUNDAMENTAL PILLARS                             |
|                                                                         |
|  1. PLANETS      -> The Actors   ("What psychological function acts?")  |
|  2. ZODIACS      -> The Costumes ("How is the energy expressed?")       |
|  3. HOUSES       -> The Stages   ("Where in life does this happen?")    |
|  4. ASPECTS      -> The Dialogue ("How do planets interact?")           |
+-------------------------------------------------------------------------+
```

---

## 2. Pillar I: Planets (*The Actors - "WHO / WHAT"*)

Planets represent core psychological drives and energetic archetypes:

| Planet / Point | Archetypal Principle | Psychological Representation |
| :--- | :--- | :--- |
| **Sun (*Surya*)** | The Monarch / Core Self | Conscious ego, purpose, will, vitality. |
| **Moon (*Chandra*)** | The Queen / Subconscious | Subconscious mind (*Manas*), emotional safety, memory, instinct. |
| **Mercury (*Budha*)** | The Messenger / Analyst | Analytical cognition (*Buddhi*), data processing, speech, communication. |
| **Venus (*Shukra*)** | The Artist / Lover | Relational value, aesthetics, social cohesion, self-worth. |
| **Mars (*Mangala*)** | The General / Warrior | Execution drive, initiative, aggression, physical kinetic energy. |
| **Jupiter (*Guru*)** | The Sage / Philosopher | Moral wisdom, expansive growth, optimism, philosophical outlook. |
| **Saturn (*Shani*)** | The Taskmaster / Stoic | Physical boundaries, strict discipline, fear, responsibility, time. |
| **Uranus** | The Rebel / Catalyst | Sudden breakthroughs, radical independence, neuro-electric restlessness. |
| **Neptune** | The Mystic / Dreamer | Boundary dissolution, imaginative vision, spirituality, illusion. |
| **Pluto** | The Alchemist / Transformer| Deep subterranean power, radical regeneration, psychological purging. |
| **Rahu (North Node)**| The Dragon's Head | Future obsession, unquenchable material drive, unconventional path. |
| **Ketu (South Node)**| The Dragon's Tail | Detachment, asceticism, innate mastery, spiritual dissolution. |

---

## 3. Pillar II: Zodiac Signs (*The Costumes - "HOW"*)

The zodiac is the 360-degree ecliptic belt divided into 12 equal sectors ($30^\circ$ each). Signs modify the **temperament and modality** of planetary expression.

### 3.1 By Elements
* **Fire (Aries, Leo, Sagittarius):** Action-oriented, dynamic, intuitive, spontaneous.
* **Earth (Taurus, Virgo, Capricorn):** Pragmatic, sensory, stable, outcome-driven.
* **Air (Gemini, Libra, Aquarius):** Conceptual, relational, analytical, objective.
* **Water (Cancer, Scorpio, Pisces):** Empathic, psychological, receptive, feeling-driven.

### 3.2 By Modalities
* **Cardinal (Aries, Cancer, Libra, Capricorn):** Initiatory drive, directional impulse.
* **Fixed (Taurus, Leo, Scorpio, Aquarius):** Structural endurance, persistence, resistance to change.
* **Mutable (Gemini, Virgo, Sagittarius, Pisces):** Adaptive, transitional, multi-tasking.

---

## 4. Pillar III: Houses (*The Stage - "WHERE"*)

Houses divide Earth's 24-hour diurnal rotation into 12 arenas of human life, anchored to the **Ascendant (Lagna)**—the degree rising on the eastern horizon at birth:

* **1st House (*Lagna*):** Physical body, constitution, immediate personality, approach to life.
* **2nd House:** Tangible personal assets, financial stability, speech, formative family.
* **3rd House:** Technical skill, tactical courage, communication, siblings.
* **4th House:** Internal psychological foundation, home, mother, private sanctuary.
* **5th House:** Pure creativity, progeny, speculative intellect, past-life merit.
* **6th House:** Work routines, technical problem-solving, friction, obstacles, somatic health.
* **7th House:** Committed partnerships, contractual alliances, one-on-one relational dynamic.
* **8th House:** Joint crises, systemic transformation, unearned assets, occult psychology.
* **9th House:** Epistemology, higher principles, world travel, teachers/mentors.
* **10th House (*MC*):** Public career, institutional authority, societal contribution.
* **11th House:** Scaled networks, communal objectives, material gains.
* **12th House:** Solitude, subconscious release, expenditure, spiritual liberation (*Moksha*).

---

## 5. Pillar IV: Geometric Aspects (*Interaction*)

Angular relationships ($\Delta\theta$) between planetary positions:
* **Conjunction ($0^\circ$):** Total energetic synthesis / fusion.
* **Opposition ($180^\circ$):** Polarized tension requiring objective balance or projection onto others.
* **Square ($90^\circ$):** Dynamic frictional crisis demanding decisive action.
* **Trine ($120^\circ$):** Effortless flow of latent talents and harmonized faculties.
* **Sextile ($60^\circ$):** Constructive opportunities activated by conscious effort.

---

## 6. Western (Sayana) vs. Vedic (Jyotish) Paradigms

| Parameter | Western (Tropical) | Vedic (Sidereal) |
| :--- | :--- | :--- |
| **Coordinate Anchor** | **Earth's Seasons (Equinox).** $0^\circ$ Aries = Vernal Equinox. | **Fixed Stars.** Accounts for precession via Ayanamsha ($\approx 24^\circ$). |
| **Primary Focus** | **Psychological Architecture.** Ego integration, behavioral shadow, modern archetypes. | **Timing & Karma (*Kala & Karma*).** Precise timing of life unfolding. |
| **Key Distinctives** | Aspect patterns (Grand Trines, T-Squares, Yods) & asteroids. | **27 Nakshatras**, **D9 Navamsha**, and **Vimshottari Dasha** hierarchies. |

---

## 7. Anti-Sycophancy & Zero-Barnum Mandate

To ensure the AI engine and RAG systems reject cold-reading flattery:
1. **Positional Causality:** Every statement must trace deterministically to:
   $$\text{Interpretation} = f(\text{Planet}, \text{Sign}, \text{House}, \text{Aspects}, \text{Dasha})$$
2. **Elimination of Universal Truisms:** Statements that apply to all humans (e.g., *"You sometimes seek privacy yet crave connection"*) are strictly prohibited.
