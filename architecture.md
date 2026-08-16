# Architecture Document

## AI-Powered Restaurant Recommendation System (Zomato Use Case)

> **Version:** 1.0  
> **Last Updated:** August 2026  
> **Source:** [problemStatement.md](./problemStatement.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Component Deep Dive](#3-component-deep-dive)
4. [Data Model](#4-data-model)
5. [API Contract](#5-api-contract)
6. [Prompt Engineering Strategy](#6-prompt-engineering-strategy)
7. [Request Lifecycle (End-to-End)](#7-request-lifecycle-end-to-end)
8. [Error Handling & Edge Cases](#8-error-handling--edge-cases)
9. [Non-Functional Requirements](#9-non-functional-requirements)
10. [Recommended Tech Stack](#10-recommended-tech-stack)
11. [Deployment Architecture](#11-deployment-architecture)
12. [Future Enhancements](#12-future-enhancements)

---

## 1. Overview

The system is an AI-powered restaurant recommendation service that combines **structured data filtering** with **LLM-based reasoning** to produce personalized, human-readable restaurant suggestions.

**Core Idea:** Rather than showing raw search results, we use an LLM to *think* about the filtered restaurants and explain *why* each one is a good match — turning a database query into a concierge-like experience.

---

## 2. High-Level Architecture

### 2.1 System Context Diagram

Shows how external actors interact with the system boundary.

```mermaid
flowchart LR
    classDef external fill:#fce4ec,stroke:#c62828,stroke-width:2px,color:#000
    classDef system fill:#e3f2fd,stroke:#1565c0,stroke-width:3px,color:#000

    subgraph ACTORS [" 🌍  External Actors "]
        direction TB
        User(["👤 End User<br/>━━━━━━━━━<br/>Sends dining preferences"]):::external
        HF(["🤗 Hugging Face<br/>━━━━━━━━━<br/>Hosts restaurant dataset"]):::external
        LLM_API(["🧠 LLM Provider<br/>━━━━━━━━━<br/>OpenAI / Google Gemini"]):::external
    end

    subgraph CORE [" 🍽️  Our System "]
        System["🍽️ Restaurant<br/>Recommendation<br/>System"]
    end

    User -- "📋 'I want cheap Italian<br/>food in Delhi'" --> System
    System -- "🏆 Top 3 picks with<br/>AI explanations" --> User
    HF -- "📦 10,000+ restaurant<br/>records (CSV)" --> System
    System -- "📝 Structured prompt<br/>with candidates" --> LLM_API
    LLM_API -- "✨ Ranked list +<br/>personalized reasons" --> System

    style ACTORS fill:#fff0f0,stroke:#c62828,stroke-width:1px,stroke-dasharray: 5
    style CORE fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style System fill:#bbdefb,stroke:#1565c0,stroke-width:3px,color:#000
```

### 2.2 Internal Component Diagram

Shows the modules *inside* the system and how data flows between them.

```mermaid
flowchart TD
    classDef user fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    classDef data fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef ai fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef process fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#000

    User(["👤 You (Hungry User)"]):::user
    Database[("📂 Zomato Menu Data<br/>(All Restaurants)")]:::data
    Filter{"🔍 Search Engine<br/>(Finds matching places)"}:::process
    Prompt["📝 AI Instruction Maker<br/>(Translates data for AI)"]:::process
    LLM(("🧠 AI Brain (LLM)<br/>(Thinks & Decides)")):::ai
    Output(["🍽️ Your Perfect Match<br/>(Top Picks + Explanations)"]):::user

    User -->|1. 'I want spicy Chinese food'| Filter
    Database -->|Provides all options| Filter
    Filter -->|2. Shortlist of 5 places| Prompt
    Prompt -->|3. Asks AI to pick the best| LLM
    LLM -->|4. Writes a personalized review| Output
    Output -.->|5. Reads recommendation| User
```

---

## 3. Component Deep Dive

### 3.1 Data Ingestion Layer

| Aspect | Detail |
|---|---|
| **Source** | [Hugging Face – zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation) |
| **Format** | CSV / Parquet via `datasets` library |
| **Trigger** | On application startup (or scheduled refresh) |
| **Processing** | Clean nulls, normalize text (lowercase city/cuisine names), map cost to budget tiers, parse ratings to float |

**Key fields extracted:**

| Field | Type | Example |
|---|---|---|
| `restaurant_name` | string | `"Barbeque Nation"` |
| `location` / `city` | string | `"Delhi"` |
| `cuisines` | list[string] | `["North Indian", "Chinese"]` |
| `average_cost_for_two` | int | `1200` |
| `aggregate_rating` | float | `4.3` |
| `votes` | int | `1542` |
| `has_online_delivery` | bool | `true` |
| `has_table_booking` | bool | `true` |

### 3.2 User Input Handler

Responsible for collecting, validating, and normalizing user preferences before they reach the filtering engine.

```mermaid
flowchart LR
    classDef input fill:#e8eaf6,stroke:#283593,stroke-width:2px,color:#000
    classDef validate fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000
    classDef output fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#000

    subgraph STEP1 [" 📥 Step 1: Receive "]
        A(["📋 Raw User Input<br/>━━━━━━━━━━━<br/>📍 Location: delhi<br/>💰 Budget: cheap<br/>🍜 Cuisine: chinese"]):::input
    end

    subgraph STEP2 [" 🛡️ Step 2: Validate "]
        B["✅ Validator<br/>━━━━━━━━━━━<br/>• Is location valid?<br/>• Is budget a known tier?<br/>• Is rating 0–5?"]:::validate
    end

    subgraph STEP3 [" 🔧 Step 3: Normalize "]
        C["🔧 Normalizer<br/>━━━━━━━━━━━<br/>• delhi → Delhi<br/>• cheap → low<br/>• chinese → Chinese"]:::validate
    end

    subgraph STEP4 [" ✅ Step 4: Output "]
        D(["📦 Clean Query Object<br/>━━━━━━━━━━━<br/>Ready for filtering"]):::output
    end

    A --> B --> C --> D

    style STEP1 fill:#e8eaf6,stroke:#283593,stroke-width:1px
    style STEP2 fill:#fff9c4,stroke:#f57f17,stroke-width:1px
    style STEP3 fill:#fff9c4,stroke:#f57f17,stroke-width:1px
    style STEP4 fill:#c8e6c9,stroke:#2e7d32,stroke-width:1px
```

**Input Fields & Validation Rules:**

| Field | Required | Validation | Default |
|---|---|---|---|
| `location` | Yes | Must match a known city in dataset | — |
| `budget` | No | One of `low`, `medium`, `high` | `medium` |
| `cuisine` | No | Fuzzy-matched against known cuisines | Any |
| `min_rating` | No | Float between 0.0 and 5.0 | `3.0` |
| `additional_prefs` | No | Free text (max 200 chars) | Empty |

**Budget Tier Mapping:**

| Tier | Cost for Two (₹) |
|---|---|
| Low | ≤ 500 |
| Medium | 501 – 1500 |
| High | > 1500 |

### 3.3 Filtering Engine (Integration Layer)

This is the deterministic core that narrows thousands of restaurants to a manageable shortlist before passing them to the LLM.

**Why filter first?**
- LLMs have token limits — we can't send 10,000 restaurants.
- Deterministic filtering is faster and cheaper than LLM inference.
- Ensures factual accuracy (the LLM can't hallucinate a restaurant that doesn't exist in the data).

**Filtering Pipeline:**

```mermaid
flowchart TD
    classDef step fill:#e0f7fa,stroke:#00695c,stroke-width:2px,color:#000
    classDef decision fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef result fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef start fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#000

    subgraph INPUT [" 📂 Raw Data "]
        A(["📂 Full Dataset<br/>━━━━━━━━━━━<br/>~10,000 restaurants"]):::start
    end

    subgraph FILTERS [" 🔍 Filter Pipeline — each step narrows the list "]
        direction TB
        B{"📍 Filter 1: Location<br/>━━━━━━━━━━━<br/>e.g. Keep only Delhi<br/>10,000 → 2,500"}:::decision
        C{"💰 Filter 2: Budget<br/>━━━━━━━━━━━<br/>e.g. Keep only ≤ ₹1500<br/>2,500 → 800"}:::decision
        D{"🍜 Filter 3: Cuisine<br/>━━━━━━━━━━━<br/>e.g. Keep only Chinese<br/>800 → 120"}:::decision
        E{"⭐ Filter 4: Min Rating<br/>━━━━━━━━━━━<br/>e.g. Keep only ≥ 3.5<br/>120 → 45"}:::decision
        B --> C --> D --> E
    end

    subgraph RANK [" 📊 Sort & Pick "]
        F["📊 Sort by Rating ↓<br/>then by Votes ↓"]:::step
        G(["🏆 Top 10 Candidates<br/>━━━━━━━━━━━<br/>Ready for AI"]):::result
        F --> G
    end

    A --> B
    E --> F

    style INPUT fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style FILTERS fill:#fff8e1,stroke:#e65100,stroke-width:1px
    style RANK fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

**Filter Order Rationale:** Location is the most restrictive filter (eliminates the most rows), so it runs first for performance. Rating is last because it's a soft preference.

### 3.4 LLM Prompt Builder

Transforms the shortlisted restaurant data + user preferences into a well-structured prompt for the LLM.

**Prompt Template Structure:**

```mermaid
flowchart TD
    classDef sys fill:#e8eaf6,stroke:#283593,stroke-width:2px,color:#000
    classDef usr fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef out fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000

    subgraph PROMPT [" 📝 Complete Prompt Sent to LLM "]
        direction TB

        subgraph SYS [" 🎭 System Prompt — Sets the AI's personality "]
            S1["🎭 Role: Restaurant expert"]:::sys
            S2["🚫 Rule: Only use provided data"]:::sys
            S3["📄 Rule: Return valid JSON"]:::sys
        end

        subgraph USR [" 👤 User Prompt — The actual question "]
            U1["📋 User Preferences<br/>location, budget, cuisine, rating"]:::usr
            U2["📂 Candidate Restaurants<br/>JSON array of 10 shortlisted places"]:::usr
            U3["📐 Output Format<br/>name, rank, reason"]:::usr
        end
    end

    subgraph RESPONSE [" ✨ Expected LLM Output "]
        R1(["🏆 Ranked Top 3<br/>with personalized<br/>explanations"]):::out
    end

    SYS --> USR
    USR --> R1

    style PROMPT fill:#f5f5f5,stroke:#616161,stroke-width:2px
    style SYS fill:#e8eaf6,stroke:#283593,stroke-width:1px
    style USR fill:#fff3e0,stroke:#e65100,stroke-width:1px
    style RESPONSE fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

### 3.5 Recommendation Engine (LLM)

| Aspect | Detail |
|---|---|
| **Provider** | OpenAI (GPT-4o) / Google (Gemini 1.5 Pro) |
| **Task** | Rank candidates, generate explanations |
| **Input** | Structured prompt from Prompt Builder |
| **Output** | JSON array of ranked restaurants with `reason` field |
| **Temperature** | 0.3 – 0.5 (creative enough to write varied explanations, but grounded) |
| **Max Tokens** | ~1000 (enough for top 3–5 recommendations with explanations) |

### 3.6 Output Formatter & Display

Parses the LLM response, merges it back with verified structured data (to prevent any hallucinated numbers), and renders it to the user.

**Output Card Structure (per restaurant):**

```mermaid
flowchart TD
    classDef header fill:#1565c0,stroke:#0d47a1,stroke-width:2px,color:#fff
    classDef info fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#000
    classDef ai fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef badge fill:#fff3e0,stroke:#e65100,stroke-width:1px,color:#000

    subgraph CARD [" 🃏 Recommendation Card "]
        direction TB

        H["🏪 Mainland China"]:::header

        subgraph DETAILS [" Quick Info "]
            direction LR
            D1["📍 Delhi"]:::badge
            D2["🍜 Chinese, Asian"]:::badge
            D3["⭐ 4.5 / 5.0"]:::badge
            D4["💰 ₹1,400 for two"]:::badge
        end

        subgraph AI_BOX [" 💬 Why AI Picked This "]
            EX["This place is perfect for your love<br/>of spicy Chinese food. Their Sichuan<br/>menu is highly rated and fits your<br/>budget perfectly."]:::ai
        end

        H --> DETAILS --> AI_BOX
    end

    style CARD fill:#f5f5f5,stroke:#1565c0,stroke-width:2px
    style DETAILS fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style AI_BOX fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

---

## 4. Data Model

### 4.1 Entity Relationship

```mermaid
erDiagram
    USER_QUERY {
        string location
        string budget
        string cuisine
        float min_rating
        string additional_prefs
    }

    RESTAURANT {
        string id PK
        string name
        string city
        string cuisines
        int avg_cost_for_two
        float rating
        int votes
        bool online_delivery
        bool table_booking
    }

    RECOMMENDATION {
        string restaurant_id FK
        int rank
        string ai_explanation
        float relevance_score
    }

    USER_QUERY ||--o{ RECOMMENDATION : "generates"
    RESTAURANT ||--o{ RECOMMENDATION : "appears in"
```

### 4.2 Data Dictionary

| Entity | Field | Type | Description |
|---|---|---|---|
| `USER_QUERY` | `location` | string | Target city for dining |
| `USER_QUERY` | `budget` | enum | `low` / `medium` / `high` |
| `USER_QUERY` | `cuisine` | string | Preferred cuisine type |
| `USER_QUERY` | `min_rating` | float | Minimum acceptable rating (0–5) |
| `USER_QUERY` | `additional_prefs` | string | Free-text preferences |
| `RESTAURANT` | `id` | string | Unique identifier |
| `RESTAURANT` | `name` | string | Restaurant name |
| `RESTAURANT` | `city` | string | City/location |
| `RESTAURANT` | `cuisines` | string | Comma-separated cuisine list |
| `RESTAURANT` | `avg_cost_for_two` | int | Average cost in ₹ |
| `RESTAURANT` | `rating` | float | Aggregate rating |
| `RESTAURANT` | `votes` | int | Number of user votes |
| `RECOMMENDATION` | `rank` | int | LLM-assigned rank (1 = best) |
| `RECOMMENDATION` | `ai_explanation` | string | LLM-generated justification |

---

## 5. API Contract

### 5.1 `POST /recommend`

**Request Body:**

```json
{
  "location": "Delhi",
  "budget": "medium",
  "cuisine": "Chinese",
  "min_rating": 3.5,
  "additional_prefs": "family-friendly, quick service"
}
```

**Success Response (200):**

```json
{
  "query": { ... },
  "recommendations": [
    {
      "rank": 1,
      "restaurant": {
        "name": "Mainland China",
        "city": "Delhi",
        "cuisines": ["Chinese", "Asian"],
        "avg_cost_for_two": 1400,
        "rating": 4.5,
        "votes": 2031,
        "online_delivery": true,
        "table_booking": true
      },
      "ai_explanation": "Mainland China is an excellent match for your request. Their authentic Sichuan and Cantonese menu is highly rated (4.5★), fits comfortably within your medium budget at ₹1,400 for two, and they're known for being family-friendly with spacious seating."
    }
  ],
  "meta": {
    "total_filtered": 42,
    "model_used": "gpt-4o",
    "latency_ms": 1830
  }
}
```

**Error Response (422) — No Matches:**

```json
{
  "error": "no_matches",
  "message": "No restaurants found matching all your criteria. Try broadening your location or budget.",
  "suggestions": ["Try 'any' cuisine", "Lower minimum rating to 3.0"]
}
```

---

## 6. Prompt Engineering Strategy

### 6.1 System Prompt

```text
You are a friendly restaurant recommendation expert. You will receive:
1. A user's dining preferences
2. A list of candidate restaurants with their details

Your job:
- Rank the top 3 restaurants that best match the user's preferences.
- For each, write a 2-3 sentence explanation in a warm, conversational tone.
- ONLY use information from the provided restaurant data. Do NOT invent details.
- Return your response as a valid JSON array.
```

### 6.2 User Prompt Template

```text
## User Preferences
- Location: {location}
- Budget: {budget} (₹{budget_range})
- Cuisine: {cuisine}
- Minimum Rating: {min_rating}
- Other: {additional_prefs}

## Candidate Restaurants
{candidates_json}

## Instructions
Return a JSON array of the top 3 recommendations. Each item should have:
- "name": restaurant name (must match exactly from the data)
- "rank": 1, 2, or 3
- "reason": your explanation for why this restaurant is a great fit
```

### 6.3 Anti-Hallucination Guardrails

| Guardrail | Implementation |
|---|---|
| Grounded data only | System prompt explicitly says "ONLY use provided data" |
| Name verification | Output parser checks that returned names exist in the candidate list |
| Number verification | Cost and rating in the display are pulled from the dataset, NOT the LLM output |
| Structured output | JSON mode enforced to prevent free-form deviation |

---

## 7. Request Lifecycle (End-to-End)

```mermaid
sequenceDiagram
    actor User as 👤 Hungry User
    participant UI as 🖥️ Frontend
    participant API as ⚙️ Backend API
    participant Filter as 🔍 Filtering Engine
    participant DB as 📂 Data Store
    participant Builder as 📝 Prompt Builder
    participant LLM as 🧠 LLM API
    participant Formatter as 🎨 Output Formatter

    rect rgb(227, 242, 253)
        Note over User,UI: 1️⃣ User Interaction
        User ->> UI: 📋 Enter preferences (location, budget, cuisine)
        UI ->> API: 📡 POST /recommend {query}
    end

    rect rgb(255, 243, 224)
        Note over API,DB: 2️⃣ Data Filtering (Fast, Deterministic)
        API ->> Filter: 🔎 Pass validated query
        Filter ->> DB: 🗄️ SELECT matching restaurants
        DB -->> Filter: 📊 2,500 rows match location
        Note right of Filter: Narrows to 45 after<br/>budget + cuisine + rating
        Filter -->> API: 🏆 Top 10 candidates
    end

    rect rgb(232, 245, 233)
        Note over API,LLM: 3️⃣ AI Processing (Slow, Intelligent)
        API ->> Builder: 📋 Preferences + 10 candidates
        Builder ->> LLM: 📝 Structured prompt
        Note right of LLM: AI thinks about soft<br/>preferences like ambiance<br/>and ranks candidates
        LLM -->> Builder: ✨ JSON with top 3 + reasons
    end

    rect rgb(243, 229, 245)
        Note over API,Formatter: 4️⃣ Verify & Format
        Builder -->> API: 📄 Parsed recommendations
        API ->> Formatter: 🔒 Merge AI output + verified data
        Note right of Formatter: Prices & ratings come<br/>from dataset, NOT the LLM
        Formatter -->> API: 📦 Final response payload
    end

    rect rgb(227, 242, 253)
        Note over User,UI: 5️⃣ Display Results
        API -->> UI: 📡 JSON response
        UI -->> User: 🍽️ Show recommendation cards
    end
```

---

## 8. Error Handling & Edge Cases

| Scenario | Behavior |
|---|---|
| **No restaurants match filters** | Return friendly message with suggestions to broaden criteria. Skip LLM call entirely. |
| **Very few matches (< 3)** | Proceed with available candidates. LLM explains it found limited options. |
| **LLM timeout / failure** | Return filtered results without AI explanations. Show fallback message: "AI insights temporarily unavailable." |
| **LLM returns invalid JSON** | Retry once with stricter prompt. If still invalid, fall back to raw filtered results. |
| **LLM hallucinates a restaurant name** | Output parser drops any recommendation whose name doesn't match the candidate list. |
| **Unknown location entered** | Return 422 error with list of supported cities from the dataset. |
| **Rate limit exceeded (LLM API)** | Queue the request and retry with exponential backoff. Show loading indicator to user. |

---

## 9. Non-Functional Requirements

| Requirement | Target | Strategy |
|---|---|---|
| **Latency** | < 3 seconds end-to-end | Pre-filter aggressively, use streaming LLM responses, cache dataset in memory |
| **Accuracy** | 100% for structured data (cost, rating) | Always display data from the dataset, never from LLM output |
| **Availability** | 99.5% uptime | Graceful degradation — if LLM is down, serve filtered results without explanations |
| **Scalability** | Support 100 concurrent users | Stateless API, horizontal scaling, async LLM calls |
| **Security** | No data leakage | LLM API key stored in env vars, user input sanitized before prompt injection |
| **Cost** | Minimize LLM API spend | Cache repeated identical queries, limit candidates to top 10, cap output tokens |

---

## 10. Recommended Tech Stack

```mermaid
flowchart TD
    classDef fe fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    classDef be fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#000
    classDef ai fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef data fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef infra fill:#eceff1,stroke:#37474f,stroke-width:2px,color:#000

    subgraph PRESENTATION [" 🖥️ Presentation Layer "]
        FE(["🖥️ Streamlit<br/>━━━━━━━<br/>Rapid prototype UI<br/>with built-in widgets"]):::fe
        FE2(["⚛️ Next.js<br/>━━━━━━━<br/>Production-grade<br/>React frontend"]):::fe
    end

    subgraph APPLICATION [" ⚙️ Application Layer "]
        BE(["🐍 FastAPI<br/>━━━━━━━<br/>Async Python API<br/>Auto-generated docs"]):::be
    end

    subgraph INTELLIGENCE [" 🧠 AI Layer "]
        LC(["🔗 LangChain<br/>━━━━━━━<br/>Prompt templates<br/>Output parsing"]):::ai
        LLMP(["✨ GPT-4o / Gemini<br/>━━━━━━━<br/>Reasoning engine"]):::ai
    end

    subgraph DATALAYER [" 📂 Data Layer "]
        PD(["🐼 Pandas<br/>━━━━━━━<br/>Filtering and<br/>transformation"]):::data
        HF(["🤗 HuggingFace<br/>━━━━━━━<br/>Dataset source"]):::data
    end

    subgraph INFRA [" ☁️ Infrastructure "]
        DK(["🐳 Docker<br/>━━━━━━━<br/>Containerized<br/>deployment"]):::infra
        CR(["☁️ Cloud Run<br/>━━━━━━━<br/>Auto-scaling"]):::infra
        LS(["📊 LangSmith<br/>━━━━━━━<br/>LLM observability"]):::infra
    end

    FE & FE2 --> BE
    BE --> LC --> LLMP
    BE --> PD --> HF
    BE --> DK --> CR
    BE -.-> LS

    style PRESENTATION fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style APPLICATION fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px
    style INTELLIGENCE fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    style DATALAYER fill:#fff3e0,stroke:#e65100,stroke-width:1px
    style INFRA fill:#eceff1,stroke:#37474f,stroke-width:1px
```

| Layer | Technology | Why |
|---|---|---|
| **Frontend** | Streamlit (prototype) or Next.js (production) | Streamlit enables rapid prototyping with built-in widgets; Next.js for a polished UI |
| **Backend API** | Python + FastAPI | Async support, auto-generated docs, great for ML/AI workflows |
| **Data Processing** | Pandas + HuggingFace `datasets` | Native Hugging Face integration, powerful filtering & transformation |
| **LLM Integration** | LangChain or direct OpenAI/Gemini SDK | LangChain for prompt templating, chaining, and output parsing |
| **LLM Provider** | OpenAI GPT-4o or Google Gemini 1.5 Pro | High quality reasoning and instruction following |
| **Deployment** | Docker → Cloud Run / Railway / Render | Containerized, auto-scaling, cost-effective for prototypes |
| **Observability** | LangSmith or structured logging | Trace prompts, latency, and LLM responses for debugging |

---

## 11. Deployment Architecture

```mermaid
flowchart LR
    classDef cloud fill:#e8eaf6,stroke:#283593,stroke-width:2px,color:#000
    classDef service fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef external fill:#fce4ec,stroke:#c62828,stroke-width:2px,color:#000
    classDef cache fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000

    subgraph CLIENT [" 🌐 Client Side "]
        Browser(["🌐 User Browser<br/>━━━━━━━━<br/>Web / Mobile"]):::external
    end

    subgraph EDGE [" ☁️ Edge Layer "]
        CDN["☁️ CDN<br/>━━━━━━━━<br/>Static Assets<br/>JS, CSS, Images"]:::cloud
        LB["⚖️ Load Balancer<br/>━━━━━━━━<br/>Round-robin traffic<br/>distribution"]:::cloud
    end

    subgraph COMPUTE [" ⚙️ Compute Layer (Auto-Scaling) "]
        API1["⚙️ API Pod 1<br/>━━━━━━━━<br/>FastAPI"]:::service
        API2["⚙️ API Pod 2<br/>━━━━━━━━<br/>FastAPI"]:::service
        Cache["💾 Redis Cache<br/>━━━━━━━━<br/>Caches repeated<br/>query results"]:::cache
    end

    subgraph EXTERNAL [" 🔌 External Services "]
        LLM_API(["🧠 LLM API<br/>━━━━━━━━<br/>OpenAI / Gemini"]):::external
        HF(["🤗 Hugging Face<br/>━━━━━━━━<br/>Dataset Source"]):::external
    end

    Browser -- "HTML/JS" --> CDN
    Browser -- "API calls" --> LB
    LB --> API1
    LB --> API2
    API1 & API2 -- "Check cache first" --> Cache
    API1 & API2 -- "If cache miss" --> LLM_API
    HF -. "⏰ Nightly sync" .-> API1

    style CLIENT fill:#fce4ec,stroke:#c62828,stroke-width:1px
    style EDGE fill:#e8eaf6,stroke:#283593,stroke-width:1px
    style COMPUTE fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    style EXTERNAL fill:#fff3e0,stroke:#e65100,stroke-width:1px
```

---

## 12. Future Enhancements

| Enhancement | Description | Impact |
|---|---|---|
| **Conversational mode** | Multi-turn chat for refining preferences ("Show me cheaper options") | Better UX |
| **Vector search (RAG)** | Embed restaurant descriptions and use semantic similarity search before LLM | Better matching for vague queries |
| **User history** | Remember past preferences and orders for personalized future recommendations | Higher relevance |
| **Review summarization** | Feed user reviews into the LLM for richer explanations | Deeper insights |
| **Multi-language support** | Serve recommendations in Hindi, Tamil, etc. | Wider reach |
| **A/B testing** | Compare different prompt strategies and LLM models for quality | Continuous improvement |
