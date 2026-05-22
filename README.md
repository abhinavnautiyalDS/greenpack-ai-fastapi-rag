# GreenPack AI Service

<img width="800" height="425" alt="llm_service py-greenpack_ai_service-VisualStudioCode2026-05-2223-55-54-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/0634b824-be81-4373-aa44-0966a2cfcc27" />

## Problem Statement

The goal of this project was to build an AI-powered backend service for EPR (Extended Producer Responsibility) compliance workflows.

The system needed to:

- Accept monthly plastic declaration submissions
- Compare declarations against ERP procurement data
- Detect mismatches deterministically
- Generate AI-based compliance summaries
- Support document-based question answering using RAG
- Reduce hallucinations by grounding responses in uploaded documents

While working on this assignment, one important thing I understood was:

Not every problem should be solved using an LLM.

Some tasks are deterministic by nature, meaning:
- the output should always be predictable
- calculations should always remain accurate
- validation rules should never hallucinate

So instead of forcing LLMs everywhere, I intentionally separated:
- deterministic logic → Python
- language generation → LLM

This became one of the most important engineering decisions in the project.

---

# What I Understood From The Assignment

The assignment was not only about generating AI responses.

It was mainly testing:

- backend engineering understanding
- modular architecture
- practical LLM integration
- RAG pipeline understanding
- separation of deterministic vs AI-driven tasks
- grounded response generation
- scalable project organization

So instead of building a simple chatbot,
I tried to build a structured backend system similar to how real AI backend services are organized.

---

# Why I Did NOT Use LLM For Everything

While working on the project, I realized:

Using LLMs for tasks like:
- validation
- percentage calculations
- reconciliation
- threshold checks

would actually make the system less reliable.

For example:
- percentage difference calculation should always remain mathematically correct
- validation should always follow strict rules
- threshold mismatch detection should never hallucinate

So I implemented those parts directly in Python.

The LLM was only used for:
- generating human-readable compliance summaries
- answering document-based questions through RAG

This separation made the system more stable and practical.

---

# Tech Stack

| Component | Technology Used |
|---|---|
| Backend Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| LLM | Grok |
| Embedding Provider | Cohere Embeddings API |
| Vector Database | ChromaDB |
| RAG Framework | LangChain |
| Validation | Pydantic |

---

# Why I Chose FastAPI

I selected FastAPI because:
- lightweight and fast
- automatically generates Swagger documentation
- very clean for backend API development
- strong validation support using Pydantic

It also helped me organize endpoints properly and test APIs quickly.

---

# Why I Used SQLite

For this assignment, SQLite was enough because:
- lightweight
- simple setup
- easy local storage
- no external database setup required

The focus of the assignment was AI orchestration and backend design, not distributed database scaling.

---

# Why I Used Grok As The LLM

I used Grok for:
- compliance narrative generation
- grounded RAG answer generation

I specifically kept the LLM usage focused only on natural language tasks.

One thing I learned while building this project is:
LLMs should assist business workflows, not replace deterministic systems.

The model integration was intentionally separated inside `llm_service.py`
so the provider can easily be swapped in future.

---

# Why I Used Cohere Embeddings

Initially, I experimented with local embedding models and OpenAI embeddings.

But while testing:
- local models caused dependency issues
- OpenAI embeddings hit free-tier quota limitations

So I switched to Cohere embeddings because:
- lightweight API integration
- stable free tier
- good semantic retrieval performance
- easy LangChain compatibility

This made the RAG pipeline cleaner and more stable.

---

# Project Structure

```bash
app/
│
├── main.py
│
├── routes/
│   ├── submit.py
│   ├── summary.py
│   └── ask.py
│
├── services/
│   ├── reconciliation.py
│   ├── rag_service.py
│   ├── llm_service.py
│   └── embedding_service.py
│
├── db/
│   ├── database.py
│   └── models.py
│
├── models/
│   └── schemas.py
│
├── data/
│   ├── erp_feed.csv
│   └── rag_docs/
│
├── utils/
│   ├── helpers.py
│   ├── constants.py
│   └── percentage_calculator.py
│
├── config/
│   └── settings.py
│
└── requirements.txt
```

---

# Folder Structure Explanation

## routes/

Contains all API endpoints.

- submit.py → declaration submission endpoint
- summary.py → reconciliation summary endpoint
- ask.py → RAG question-answering endpoint

I separated routes from business logic to keep APIs clean and scalable.

---

## services/

This is the core logic layer of the project.

### reconciliation.py
Handles:
- ERP comparison
- mismatch detection
- percentage calculations
- threshold flagging

### rag_service.py
Handles:
- document loading
- chunking
- embeddings
- vector retrieval
- grounded answer generation

### llm_service.py
Handles:
- communication with the LLM
- narrative generation

### embedding_service.py
Handles:
- embedding model integration

Separating these services helped keep the architecture modular.

---

## db/

Handles:
- database connection
- SQLAlchemy models

This layer keeps storage logic isolated from API logic.

---

## models/

Contains Pydantic schemas for:
- request validation
- structured API contracts

This helped enforce deterministic validation.

---

## data/

Contains:
- ERP procurement feed
- RAG documents

The ERP CSV simulates procurement data coming from enterprise systems.

The rag_docs folder contains compliance-related documents used for retrieval.

---

## utils/

Contains reusable helper functions and constants.

For example:
- UUID generation
- threshold constants
- percentage calculations

---

# Complete Workflow Explanation

## Step 1 — Declaration Submission

The user submits monthly plastic declarations using `/submit`.

The payload is validated using Pydantic.

The data is then stored inside SQLite database.

---

## Step 2 — Reconciliation

The `/summary` endpoint:
- reads declaration data
- reads ERP procurement feed
- compares values category-wise
- calculates percentage mismatches
- flags categories exceeding threshold

This entire process is deterministic and handled using Python logic.

---

## Step 3 — AI Narrative Generation

After reconciliation:
- structured findings are converted into a prompt
- the LLM generates a human-readable compliance summary

This allows the system to produce readable compliance insights while keeping calculations deterministic.

---

## Step 4 — RAG Workflow

The `/ask` endpoint uses Retrieval-Augmented Generation.

Workflow:

Question
↓
Embedding Generation
↓
Vector Similarity Search
↓
Relevant Chunk Retrieval
↓
LLM Answer Generation

Only retrieved context is sent to the LLM.

This reduces hallucination risk.

---

# Hallucination Prevention

One thing I focused on carefully was avoiding hallucinated responses.

If the answer is not found inside retrieved documents,
the system returns:

> "I do not know based on the provided documents."

instead of generating fabricated answers.

This was important because compliance systems should prioritize reliability over creativity.

---

# Challenges I Faced During Development

This project involved much more debugging and engineering work than I initially expected.

Some major challenges I faced:

---

## 1. Dependency Issues

While experimenting with local embedding models,
I faced:
- PyTorch DLL issues
- version conflicts
- Windows dependency problems

This taught me the importance of dependency management in AI systems.

---

## 2. API Quota Limitations

During testing:
- OpenAI embeddings hit free-tier quota limits
- Grok API required account credits

This forced me to redesign parts of the integration layer.

Because the architecture was modular,
I could switch providers without changing business logic.

This became an important learning experience.

---

## 3. LangChain Version Changes

Some methods changed in newer LangChain versions.

For example:
- retriever APIs
- import paths
- text splitter modules

I had to debug and adapt the implementation carefully.

---

## 4. Understanding When NOT To Use LLMs

One of the biggest learnings from this project was:

Sometimes the correct engineering decision is NOT using AI.

Using deterministic Python logic for validation and reconciliation made the system more stable and predictable.

This changed how I think about practical AI system design.

---

# Future Improvements

If I continue this project further, I would like to improve:

- async database operations
- authentication and authorization
- Docker deployment
- vector DB caching
- better chunking strategies
- hybrid search retrieval
- monitoring and logging
- production-grade retry handling
- unit testing
- CI/CD pipeline
- provider fallback mechanisms
- frontend dashboard

I would also like to:
- preload vector stores during startup
- optimize retrieval latency
- improve citation quality
- add structured evaluation metrics for RAG performance

---

# What This Project Taught Me

This project taught me much more than just calling APIs.

I learned:
- modular backend design
- practical AI orchestration
- grounded retrieval systems
- separation of concerns
- deterministic vs probabilistic workflows
- debugging real-world AI integrations

Most importantly,
I learned that building reliable AI systems is not only about using LLMs,
but about knowing where NOT to use them.

---

# API Endpoints

## POST `/submit`

Stores monthly plastic declarations.

---

## GET `/summary/{producer_id}/{month}`

Performs reconciliation and generates compliance narrative.

---

## POST `/ask`

RAG-based compliance question answering.

---

# Running The Project

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run backend server

```bash
uvicorn app.main:app --reload
```

---

# Swagger Documentation

FastAPI automatically generates Swagger UI for API testing.

Open:

```bash
http://127.0.0.1:8000/docs
```

---

# Screenshots

## Swagger API Testing
<img width="1878" height="880" alt="Screenshot 2026-05-22 235646" src="https://github.com/user-attachments/assets/1c4e2c6c-1ea5-4685-85ad-67b0aba4828e" />








---

## Backend Running

<!-- ADD TERMINAL RUNNING SCREENSHOT HERE -->
<img width="800" height="425" alt="llm_service py-greenpack_ai_service-VisualStudioCode2026-05-2223-55-54-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/c2fb21ba-a5a6-410e-a9d7-dddf9e1d02d7" />


---



---

# Final Note

This project took a lot more effort than I initially expected.

A large amount of time went into:
- debugging integrations
- understanding dependency issues
- structuring services properly
- handling provider limitations
- and making the system modular enough for future changes

Even though this is a prototype system,
I tried to approach it with practical engineering thinking instead of only focusing on AI outputs.

The biggest thing I learned while building this project is:

Reliable AI systems are built by combining deterministic engineering with carefully controlled AI usage.
