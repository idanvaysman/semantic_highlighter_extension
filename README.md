# Semantic Highlight Explorer

## Overview

Semantic Highlight Explorer is a browser-based tool that allows users to highlight text on a webpage and discover contextually related articles using semantic similarity.

The system combines:

- A Chrome extension for capturing highlighted content
- A Python backend for natural language processing
- Hybrid retrieval (lexical search + semantic ranking)
- Vector embeddings for similarity scoring

The goal of this project is to explore how modern information retrieval systems combine keyword search and semantic embeddings to return relevant results efficiently.

---

## Why This Project

Traditional search engines rely heavily on keyword matching. While effective, keyword-based retrieval can miss relevant content that uses different phrasing or vocabulary.

This project investigates how semantic embeddings can improve relevance by matching meaning rather than exact wording.

It is designed as a learning-focused system that demonstrates:

- Hybrid search architecture
- Embedding-based similarity ranking
- Retrieval system design tradeoffs
- Client–server interaction
- External API integration
- Performance and latency considerations

---

## High-Level Architecture

1. User highlights text in the browser.
2. The Chrome extension captures the highlighted text and surrounding context.
3. The extension sends this data to the backend.
4. The backend:
   - Extracts keywords for candidate retrieval
   - Retrieves a candidate pool from an external source
   - Generates embeddings for both the query and candidate articles
   - Computes similarity scores
   - Ranks and returns the most relevant results
5. The extension displays the ranked articles to the user.

---

## Tech Stack

### Frontend
- Chrome Extension (Manifest V3)
- Vanilla JavaScript

### Backend
- Python
- FastAPI
- spaCy (keyword extraction)
- sentence-transformers (embeddings)

### External Data Sources
- Academic or search APIs (configurable)

### Database (Optional / Evolving)
- PostgreSQL (e.g., Supabase)
- pgvector for vector similarity search

---

## Design Principles

- Hybrid retrieval (lexical narrowing followed by semantic ranking)
- Clear separation of concerns (extension vs backend)
- Incremental complexity (start simple, optimize later)
- Learning-oriented implementation (avoid black-box abstractions)
- Measurable performance and evaluation

---

## Current Status

This project is under active development.

Planned milestones include:

- Highlight capture and context extraction
- Candidate retrieval from external APIs
- Embedding-based similarity ranking
- Caching and performance optimization
- Optional vector indexing

---

## Future Directions

Potential extensions include:

- Improved contextual modeling
- Re-ranking strategies
- Vector database integration
- Evaluation benchmarking
- Broader domain and content support
- Enhanced UI and interaction features

---

## Running the Project

Setup instructions will be added as development progresses.
