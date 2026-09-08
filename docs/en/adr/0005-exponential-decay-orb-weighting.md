# ADR-0005: Continuous Exponential Decay Function for Aspect Orb Weighting

* **Status:** Accepted  
* **Date:** 2026-09-08  
* **Deciders:** Architecture Team  

---

## Context and Problem Statement
In traditional astrology software, aspect orbs are typically handled using discrete step boundaries or hard cutoffs (e.g., if orb $< 1^\circ \rightarrow$ "Very Strong"; if orb between $1^\circ - 3^\circ \rightarrow$ "Medium"; if orb $> 5^\circ \rightarrow$ "Ignored").

Step boundaries introduce severe mathematical and user-experience defects:
1. **Cliff-Edge Anomaly:** An aspect with orb $0.99^\circ$ is weighted at $100\%$, while an aspect at $1.01^\circ$ abruptly drops to $50\%$, causing erratic score jumps between consecutive days.
2. **Under-weighting Exact Alignment:** A direct mathematical hit ($0.01^\circ$) carries disproportionately higher energetic intensity than an aspect at $2.5^\circ$, which step functions fail to capture.

## Decision Outcome
Chosen option: **Continuous Exponential Decay Formulation**:
$$W(\delta) = 10.0 \times \exp(-1.4 \times \delta)$$
Where $\delta = |\theta_{\text{transit}} - \theta_{\text{natal}}| - \theta_{\text{exact}}$ is the angular separation error in degrees.

* At exact alignment ($\delta = 0.00^\circ$): $W = 10.00$
* At close alignment ($\delta = 0.50^\circ$): $W = 4.96$
* At moderate alignment ($\delta = 1.00^\circ$): $W = 2.46$
* At wide alignment ($\delta = 3.00^\circ$): $W = 0.15$ (Effectively negligible)

If an aspect touches the active **Mahadasha** or **Antardasha** ruler, the weight is amplified by a scalar factor:
$$W_{\text{effective}} = W(\delta) \times 1.5$$

## Consequences

### Positive
* Smooth, differentiable, continuous score curves across daily transit timelines with zero cliff-edge jumps.
* Exponentially amplifies the impact of tight aspects ($\le 0.25^\circ$), aligning with empirical energetic reality.
* Integrates cleanly with programmatic time-series smoothing.

### Negative / Trade-offs
* Non-linear math is slightly less intuitive for non-technical users to manually calculate by hand than simple integer step tables.
