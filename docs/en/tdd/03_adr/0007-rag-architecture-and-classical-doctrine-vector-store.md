# ADR-0007: RAG Architecture & Classical Doctrine Vector Store

* **Status:** Accepted  
* **Date:** 2026-09-08  

## Context & Problem Statement
To satisfy the core product mandate of zero tolerance for the Barnum / Forer effect and complete elimination of hallucinations, the AI Chatbot cannot generate unconstrained text. The platform requires a *Retrieval-Augmented Generation* (RAG) architecture that strictly anchors all textual outputs in authoritative classical literature (e.g., *Brihat Parashara Hora Shastra*, *Phaladeepika*, Ptolemaic canons).

Evaluated options:
1. **Direct LLM Fine-Tuning:** Costly, susceptible to catastrophic forgetting, prone to hallucination, and lacks verifiable citation traceability.
2. **Hardcoded Rule Engines:** Brittle, combinatorial explosion of rules, and constrained user interaction.
3. **Hybrid RAG Pipeline (pgvector / ChromaDB + Low-Temperature LLM):** Index classical passages in a semantic vector store, retrieve passages matching exact user astrological coordinates, and inject them as ground-truth context.

## Decision
Adopt the **Hybrid RAG Pipeline**:
1. Classical texts are chunked and indexed with semantic embeddings and structured metadata tags (planets, signs, houses, aspect types, life domains).
2. LLM inference runs under low temperature (0.2) with strict system prompt guardrails mandating chapter citations and explicitly forbidding flattering or generic statements.
3. If the semantic similarity score falls below threshold ($< 0.65$), the system explicitly declines to speculate and informs the user that classical doctrines offer no validation.

## Consequences
* **Positive:** 0% doctrinal hallucination, transparent citation traceability, and adherence to anti-Barnum principles.
* **Trade-off:** Requires upfront corpus curation and chunking, along with vector database infrastructure.
