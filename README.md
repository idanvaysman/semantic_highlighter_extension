# ResearchAI

**ResearchAI** is a Chrome extension designed to assist academic research by capturing context from webpages and retrieving relevant scholarly articles using semantic similarity and AI-based ranking.

The system combines a lightweight browser extension with a Python backend that retrieves academic papers and ranks them based on how closely they relate to highlighted content on a webpage.

The goal of the project is to explore how modern information retrieval systems can combine traditional search with semantic embeddings to return more meaningful research results.

---

# Motivation

Most search tools rely heavily on **keyword matching**, which can miss relevant research when different terminology or phrasing is used.

ResearchAI explores how **semantic similarity models** can improve retrieval by comparing the meaning of text rather than relying solely on exact keyword overlap.

The project is designed to help users move directly from reading online material to discovering **relevant academic papers**. Instead of manually searching through academic databases, users can highlight a passage on any webpage and retrieve related research articles.

To make access easier for students, the system also integrates with the **University of California, Santa Cruz (UCSC) library proxy**. When available, article links are routed through the UCSC proxy so students with valid UCSC accounts can access institutional subscriptions without manually navigating the library website.

---

# System Architecture

ResearchAI follows a **client–server architecture** consisting of two main components: a browser extension and a backend retrieval service.

---

## Browser Extension

The Chrome extension captures contextual information from the active webpage, including:

- highlighted text selected by the user  
- the surrounding paragraph  
- page title  
- page URL  

This information is sent to the backend to generate a research query.

The extension communicates with the backend through HTTP requests and displays returned results inside the Chrome side panel.

---

## Backend Retrieval Service

The backend is responsible for retrieving academic papers and ranking them based on relevance.

The process works as follows:

1. The extension sends the captured context to a `/search` endpoint.
2. The backend sends a query to academic data sources such as **OpenAlex**.
3. A set of related research papers is returned.
4. Embeddings are generated for the highlighted text and each paper using a sentence-transformer model.
5. Similarity scores are calculated to measure semantic relevance.
6. A **cross-encoder re-ranking model** performs a second pass to refine the ranking of results.
7. The ranked papers are returned to the extension.

This multi-stage ranking approach improves relevance by combining **fast embedding similarity with deeper cross-encoder analysis**.

---

# Tech Stack

## Frontend
- Chrome Extension (Manifest V3)
- Vanilla JavaScript
- Chrome Side Panel API

## Backend
- Python
- FastAPI

## Machine Learning / NLP
- sentence-transformers for semantic embeddings
- cross-encoder model for re-ranking search results
- cosine similarity for embedding comparison

## External Data Sources
- OpenAlex academic paper API

## Database (Planned)
- PostgreSQL
- pgvector for vector similarity search

---

# Data Flow

1. A user highlights text on a webpage.
2. The extension captures the highlighted text and surrounding context.
3. The context is sent to the backend `/search` endpoint.
4. The backend retrieves related research papers from OpenAlex.
5. Embeddings are generated for the query and each paper.
6. Similarity scores are calculated.
7. A cross-encoder model refines the ranking of results.
8. Ranked results are returned to the extension.
9. When available, article links are routed through the **UCSC library proxy** to allow institutional access.

---

# Key Engineering Concepts

### Semantic Similarity Ranking

The system uses vector embeddings to measure how closely research papers relate to the highlighted passage. This allows relevant research to be discovered even when different wording is used.

### Cross-Encoder Re-Ranking

After initial similarity scoring, a cross-encoder model performs a second ranking pass.  
This model evaluates the query and each paper together, allowing it to capture deeper contextual relationships.

### Context-Aware Queries

Instead of relying only on keywords, the system captures both the **highlighted text and the surrounding paragraph**, providing richer context for retrieving relevant research papers.

### Modular System Design

The browser extension and backend services are independent components.  
This architecture allows improvements to the retrieval pipeline without requiring changes to the extension.

### Integration with Academic Infrastructure

By routing links through the **UCSC library proxy**, the system allows students to access subscription-based research papers using their university authentication.

---

# Current Status

The project currently supports:

- capturing highlighted text and surrounding context from webpages  
- retrieving academic papers using the OpenAlex API  
- semantic similarity ranking of research papers  
- cross-encoder re-ranking for improved relevance  
- communication between the Chrome extension and Python backend  
- routing research links through the UCSC proxy for institutional access  

---

# Future Improvements

Planned improvements include:

- **Keyword extraction using spaCy** to generate more precise search queries from highlighted text  
- **Vector database integration** using pgvector or FAISS for faster similarity search  
- **Query expansion techniques** to improve recall  
- **Caching and latency optimizations** for faster responses  
- **Evaluation benchmarks** to measure retrieval performance  

Keyword extraction with spaCy would allow the system to automatically identify key phrases and nouns within highlighted passages, improving the quality of queries sent to academic search APIs.

---

# Running the Project

Setup instructions will be added as development progresses.
