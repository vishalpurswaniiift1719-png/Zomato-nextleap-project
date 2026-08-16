# Implementation Plan

## AI-Powered Restaurant Recommendation System

> **Based on:** [problemStatement.md](./problemStatement.md) · [architecture.md](./architecture.md)  
> **Last Updated:** August 2026

---

## Roadmap Overview

```mermaid
gantt
    title 🗓️ Implementation Roadmap
    dateFormat  YYYY-MM-DD
    axisFormat  %b %d

    section Phase 1 – Foundation
    Project setup & environment       :p1a, 2026-08-15, 2d
    Dataset loading & cleaning        :p1b, after p1a, 3d
    Exploratory data analysis         :p1c, after p1b, 2d

    section Phase 2 – Core Logic
    User input handler                :p2a, after p1c, 2d
    Filtering engine                  :p2b, after p2a, 3d
    Unit tests for filters            :p2c, after p2b, 2d

    section Phase 3 – AI Integration
    LLM connection setup              :p3a, after p2c, 2d
    Prompt engineering                :p3b, after p3a, 3d
    Output parser & guardrails        :p3c, after p3b, 2d

    section Phase 4 – UI & UX
    Streamlit UI shell                :p4a, after p3c, 2d
    Recommendation cards              :p4b, after p4a, 2d
    Error states & loading            :p4c, after p4b, 1d

    section Phase 5 – Polish & Deploy
    End-to-end testing                :p5a, after p4c, 2d
    Performance optimization          :p5b, after p5a, 2d
    Deployment & documentation        :p5c, after p5b, 2d
```

---

## Phase Summary

```mermaid
flowchart LR
    classDef p1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    classDef p2 fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef p3 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef p4 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#000
    classDef p5 fill:#fce4ec,stroke:#c62828,stroke-width:2px,color:#000

    P1(["🏗️ Phase 1<br/>━━━━━━━<br/>Foundation<br/>~7 days"]):::p1
    P2(["⚙️ Phase 2<br/>━━━━━━━<br/>Core Logic<br/>~7 days"]):::p2
    P3(["🧠 Phase 3<br/>━━━━━━━<br/>AI Integration<br/>~7 days"]):::p3
    P4(["🖥️ Phase 4<br/>━━━━━━━<br/>UI & UX<br/>~5 days"]):::p4
    P5(["🚀 Phase 5<br/>━━━━━━━<br/>Polish & Deploy<br/>~6 days"]):::p5

    P1 -- "Data ready" --> P2
    P2 -- "Filters work" --> P3
    P3 -- "AI responds" --> P4
    P4 -- "App usable" --> P5
```

---

## Phase 1: Foundation & Data Ingestion

> **Goal:** Set up the project, load the dataset, and understand the data.  
> **Duration:** ~7 days  
> **Deliverable:** Clean, indexed DataFrame ready for querying

### Tasks

```mermaid
flowchart TD
    classDef todo fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    classDef done fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#000

    subgraph S1 [" 📦 1.1 Project Setup "]
        A1["Initialize Python project<br/>(pyproject.toml / requirements.txt)"]:::todo
        A2["Create folder structure<br/>src/ tests/ data/ notebooks/"]:::todo
        A3["Set up virtual environment<br/>(.venv + pip install)"]:::todo
        A4["Initialize Git repo<br/>+ .gitignore"]:::todo
    end

    subgraph S2 [" 📂 1.2 Data Loading "]
        B1["Install huggingface datasets<br/>pip install datasets"]:::todo
        B2["Download Zomato dataset<br/>ManikaSaini/zomato-restaurant-recommendation"]:::todo
        B3["Convert to Pandas DataFrame"]:::todo
        B4["Save local cache<br/>(CSV / Parquet)"]:::todo
    end

    subgraph S3 [" 🧹 1.3 Data Cleaning "]
        C1["Handle missing values<br/>(drop or fill defaults)"]:::todo
        C2["Normalize text fields<br/>(lowercase city, cuisine names)"]:::todo
        C3["Parse ratings to float<br/>(handle 'NEW', '-' values)"]:::todo
        C4["Map cost → budget tiers<br/>(low ≤500, med 501-1500, high >1500)"]:::todo
    end

    subgraph S4 [" 📊 1.4 EDA (Exploratory Analysis) "]
        D1["Distribution of restaurants<br/>per city"]:::todo
        D2["Rating distribution<br/>& outliers"]:::todo
        D3["Most common cuisines<br/>& cost ranges"]:::todo
        D4["Create summary notebook<br/>with visualizations"]:::todo
    end

    S1 --> S2 --> S3 --> S4

    style S1 fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style S2 fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style S3 fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style S4 fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
```

### Folder Structure

```
zomato-recommender/
├── src/
│   ├── __init__.py
│   ├── data_loader.py        # Dataset loading & caching
│   ├── data_cleaner.py       # Preprocessing & normalization
│   ├── filter_engine.py      # Phase 2
│   ├── prompt_builder.py     # Phase 3
│   ├── llm_client.py         # Phase 3
│   ├── output_formatter.py   # Phase 3
│   └── app.py                # Phase 4 (Streamlit entry)
├── tests/
│   ├── test_data_loader.py
│   ├── test_filter_engine.py
│   └── test_prompt_builder.py
├── notebooks/
│   └── eda.ipynb              # Exploratory analysis
├── data/
│   └── .gitkeep               # Local cache (gitignored)
├── .env                       # API keys (gitignored)
├── .gitignore
├── requirements.txt
└── README.md
```

### Key Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Dataset format | Parquet (local cache) | Faster reads than CSV, smaller file size |
| Data framework | Pandas | Simple, well-documented, sufficient for ~10K rows |
| Budget tiers | Low ≤ ₹500, Medium ₹501–1500, High > ₹1500 | Based on Zomato's typical price distribution |

### Exit Criteria

- [ ] Dataset loads successfully from Hugging Face
- [ ] DataFrame has no null values in critical columns (name, city, rating, cost)
- [ ] All text fields are normalized (consistent casing)
- [ ] Budget tier column is added
- [ ] EDA notebook shows data distribution insights

---

## Phase 2: Core Filtering Logic

> **Goal:** Build the deterministic filtering engine that narrows restaurants before AI.  
> **Duration:** ~7 days  
> **Deliverable:** A function that takes user preferences → returns top 10 candidates

### Tasks

```mermaid
flowchart TD
    classDef task fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef test fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000

    subgraph S1 [" 👤 2.1 User Input Handler "]
        A1["Define UserQuery dataclass<br/>(location, budget, cuisine,<br/>min_rating, additional_prefs)"]:::task
        A2["Build input validator<br/>(check city exists, rating 0-5,<br/>budget in enum)"]:::task
        A3["Build normalizer<br/>(lowercase → title case,<br/>fuzzy cuisine matching)"]:::task
    end

    subgraph S2 [" 🔍 2.2 Filtering Engine "]
        B1["Filter by location<br/>(exact match on city)"]:::task
        B2["Filter by budget tier<br/>(map cost to tier, compare)"]:::task
        B3["Filter by cuisine<br/>(substring match in cuisines list)"]:::task
        B4["Filter by minimum rating<br/>(≥ threshold)"]:::task
        B5["Sort by rating ↓, votes ↓<br/>Return top N"]:::task
    end

    subgraph S3 [" ✅ 2.3 Testing "]
        C1["Test: Delhi + Chinese + medium<br/>→ returns expected results"]:::test
        C2["Test: unknown city<br/>→ returns empty + error msg"]:::test
        C3["Test: very restrictive query<br/>→ handles gracefully"]:::test
        C4["Test: no cuisine specified<br/>→ returns all cuisines"]:::test
    end

    S1 --> S2 --> S3

    style S1 fill:#fff3e0,stroke:#e65100,stroke-width:1px
    style S2 fill:#fff3e0,stroke:#e65100,stroke-width:1px
    style S3 fill:#fff9c4,stroke:#f57f17,stroke-width:1px
```

### API Design

```python
# src/filter_engine.py

@dataclass
class UserQuery:
    location: str                    # Required
    budget: str = "medium"           # low | medium | high
    cuisine: str = ""                # Optional, fuzzy matched
    min_rating: float = 3.0          # 0.0 – 5.0
    additional_prefs: str = ""       # Free text for LLM

def filter_restaurants(df: pd.DataFrame, query: UserQuery) -> pd.DataFrame:
    """Returns top 10 candidates sorted by rating, votes."""
    ...
```

### Exit Criteria

- [ ] `UserQuery` dataclass validates and normalizes all inputs
- [ ] `filter_restaurants()` correctly chains location → budget → cuisine → rating filters
- [ ] Returns top 10 candidates sorted by (rating desc, votes desc)
- [ ] Handles edge cases: no matches, partial matches, unknown city
- [ ] All unit tests pass

---

## Phase 3: AI / LLM Integration

> **Goal:** Connect to an LLM, build prompts, parse responses, and add safety guardrails.  
> **Duration:** ~7 days  
> **Deliverable:** Function that takes candidates + preferences → returns ranked recommendations with explanations

### Tasks

```mermaid
flowchart TD
    classDef task fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef critical fill:#ffcdd2,stroke:#c62828,stroke-width:2px,color:#000

    subgraph S1 [" 🔌 3.1 LLM Connection "]
        A1["Install openai / google-genai SDK"]:::task
        A2["Create .env with API key<br/>(OPENAI_API_KEY or GEMINI_KEY)"]:::task
        A3["Build LLMClient wrapper class<br/>(send_prompt, handle errors)"]:::task
        A4["Test basic prompt-response<br/>roundtrip"]:::task
    end

    subgraph S2 [" 📝 3.2 Prompt Engineering "]
        B1["Write system prompt<br/>(role, rules, anti-hallucination)"]:::task
        B2["Write user prompt template<br/>(preferences + candidates JSON)"]:::task
        B3["Define output JSON schema<br/>(name, rank, reason)"]:::task
        B4["Iterate on prompt quality<br/>(test with 5+ different queries)"]:::task
    end

    subgraph S3 [" 🛡️ 3.3 Safety Guardrails "]
        C1["Validate restaurant names<br/>exist in candidate list"]:::critical
        C2["Pull cost/rating from dataset<br/>NOT from LLM output"]:::critical
        C3["Handle malformed JSON<br/>(retry once, then fallback)"]:::critical
        C4["Set temperature 0.3-0.5<br/>for grounded responses"]:::task
    end

    subgraph S4 [" 🎨 3.4 Output Formatting "]
        D1["Parse LLM JSON response"]:::task
        D2["Merge with verified dataset fields"]:::task
        D3["Build Recommendation dataclass<br/>(rank, restaurant, ai_explanation)"]:::task
    end

    S1 --> S2 --> S3 --> S4

    style S1 fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    style S2 fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    style S3 fill:#ffebee,stroke:#c62828,stroke-width:1px
    style S4 fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

### Prompt Strategy

```mermaid
flowchart LR
    classDef prompt fill:#e8eaf6,stroke:#283593,stroke-width:2px,color:#000
    classDef guard fill:#ffcdd2,stroke:#c62828,stroke-width:2px,color:#000
    classDef ok fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#000

    subgraph BUILD [" 📝 Build "]
        P["System Prompt<br/>+ User Prefs<br/>+ 10 Candidates"]:::prompt
    end

    subgraph SEND [" 📡 Send "]
        L["LLM API Call<br/>(temp=0.4, max_tokens=1000)"]:::prompt
    end

    subgraph VALIDATE [" 🛡️ Validate "]
        V1{"Valid JSON?"}:::guard
        V2{"Names exist<br/>in candidates?"}:::guard
        V3{"≤ 3 results?"}:::guard
    end

    subgraph OUTPUT [" ✅ Output "]
        O(["✅ Safe Recommendations<br/>with verified data"]):::ok
    end

    RETRY(["🔄 Retry once<br/>with stricter prompt"]):::guard
    FALLBACK(["⚠️ Fallback<br/>Raw filtered results"]):::guard

    P --> L --> V1
    V1 -- "Yes" --> V2
    V1 -- "No" --> RETRY --> V1
    V2 -- "Yes" --> V3
    V2 -- "No" --> FALLBACK
    V3 -- "Yes" --> O
    V3 -- "No" --> O

    style BUILD fill:#e8eaf6,stroke:#283593,stroke-width:1px
    style SEND fill:#e8eaf6,stroke:#283593,stroke-width:1px
    style VALIDATE fill:#fff3e0,stroke:#e65100,stroke-width:1px
    style OUTPUT fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

### Exit Criteria

- [ ] LLM client connects and returns valid responses
- [ ] System prompt + user prompt template produce high-quality recommendations
- [ ] Output parser validates JSON, restaurant names, and field accuracy
- [ ] Fallback mechanism works when LLM returns invalid data
- [ ] 5+ diverse test queries produce relevant, well-explained results

---

## Phase 4: User Interface

> **Goal:** Build a clean, interactive Streamlit UI.  
> **Duration:** ~5 days  
> **Deliverable:** Working web app where users can input preferences and see AI recommendations

### Tasks

```mermaid
flowchart TD
    classDef task fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#000

    subgraph S1 [" 🖥️ 4.1 UI Shell "]
        A1["Page config, title, sidebar layout"]:::task
        A2["Sidebar: location dropdown<br/>(populated from dataset cities)"]:::task
        A3["Sidebar: budget radio buttons<br/>(Low / Medium / High)"]:::task
        A4["Sidebar: cuisine selector<br/>(multiselect from dataset)"]:::task
        A5["Sidebar: rating slider (0–5)"]:::task
        A6["Sidebar: free-text input<br/>for additional preferences"]:::task
    end

    subgraph S2 [" 🃏 4.2 Recommendation Cards "]
        B1["Design card component<br/>(name, cuisine, rating, cost)"]:::task
        B2["Display AI explanation<br/>in expandable section"]:::task
        B3["Show rank badges<br/>(🥇 🥈 🥉)"]:::task
    end

    subgraph S3 [" ⚠️ 4.3 States & Feedback "]
        C1["Loading spinner<br/>while LLM processes"]:::task
        C2["Empty state<br/>(no matches found message)"]:::task
        C3["Error state<br/>(API failure, timeout)"]:::task
        C4["Success animation<br/>(cards fade in)"]:::task
    end

    S1 --> S2 --> S3

    style S1 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px
    style S2 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px
    style S3 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px
```

### UI Wireframe

```mermaid
flowchart TD
    classDef sidebar fill:#e8eaf6,stroke:#283593,stroke-width:2px,color:#000
    classDef main fill:#f5f5f5,stroke:#616161,stroke-width:2px,color:#000
    classDef card fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000

    subgraph PAGE [" 🖥️ App Layout "]
        direction LR

        subgraph SIDE [" 📋 Sidebar "]
            direction TB
            S1["📍 Location<br/>[ Delhi      ▾ ]"]:::sidebar
            S2["💰 Budget<br/>◉ Low ○ Med ○ High"]:::sidebar
            S3["🍜 Cuisine<br/>[ Chinese, Italian ]"]:::sidebar
            S4["⭐ Min Rating<br/>━━●━━━━ 3.5"]:::sidebar
            S5["💬 Extra Prefs<br/>[ family-friendly ]"]:::sidebar
            S6["🔍 Find Restaurants 🔘"]:::sidebar
            S1 --> S2 --> S3 --> S4 --> S5 --> S6
        end

        subgraph MAIN [" 🍽️ Results "]
            direction TB
            R1["🥇 Mainland China<br/>⭐ 4.5 · 🍜 Chinese · 💰 ₹1400<br/>💬 'Perfect for family dining...'"]:::card
            R2["🥈 Chung Wah<br/>⭐ 4.3 · 🍜 Chinese · 💰 ₹900<br/>💬 'Great value for money...'"]:::card
            R3["🥉 Wow! Momo<br/>⭐ 4.1 · 🍜 Chinese · 💰 ₹500<br/>💬 'Quick and budget-friendly...'"]:::card
        end
    end

    style PAGE fill:#fafafa,stroke:#bdbdbd,stroke-width:1px
    style SIDE fill:#e8eaf6,stroke:#283593,stroke-width:1px
    style MAIN fill:#f5f5f5,stroke:#616161,stroke-width:1px
```

### Exit Criteria

- [ ] Sidebar collects all 5 user preference fields
- [ ] Dropdowns/selectors are populated dynamically from the dataset
- [ ] Recommendation cards display all required fields + AI explanation
- [ ] Loading, empty, and error states are handled gracefully
- [ ] App runs locally with `streamlit run src/app.py`

---

## Phase 5: Polish, Testing & Deployment

> **Goal:** Harden the app, optimize performance, and deploy.  
> **Duration:** ~6 days  
> **Deliverable:** Production-ready app deployed to the cloud

### Tasks

```mermaid
flowchart TD
    classDef task fill:#fce4ec,stroke:#c62828,stroke-width:2px,color:#000
    classDef deploy fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000

    subgraph S1 [" ✅ 5.1 End-to-End Testing "]
        A1["Happy path test<br/>(Delhi + Chinese + medium)"]:::task
        A2["Edge case: no results"]:::task
        A3["Edge case: LLM timeout"]:::task
        A4["Edge case: invalid input"]:::task
    end

    subgraph S2 [" ⚡ 5.2 Performance "]
        B1["Cache dataset in memory<br/>(load once at startup)"]:::task
        B2["Add response caching<br/>(same query → cached LLM result)"]:::task
        B3["Measure latency<br/>(target < 3 seconds)"]:::task
    end

    subgraph S3 [" 🚀 5.3 Deployment "]
        C1["Create Dockerfile"]:::deploy
        C2["Add Streamlit Cloud config<br/>(or Railway / Render)"]:::deploy
        C3["Set environment variables<br/>(API keys via secrets)"]:::deploy
        C4["Deploy & smoke test"]:::deploy
    end

    subgraph S4 [" 📖 5.4 Documentation "]
        D1["Write README.md<br/>(setup, usage, screenshots)"]:::deploy
        D2["Add inline code comments"]:::deploy
        D3["Record demo GIF / video"]:::deploy
    end

    S1 --> S2 --> S3 --> S4

    style S1 fill:#fce4ec,stroke:#c62828,stroke-width:1px
    style S2 fill:#fff3e0,stroke:#e65100,stroke-width:1px
    style S3 fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    style S4 fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

### Deployment Checklist

| Step | Command / Action | Verify |
|---|---|---|
| Build Docker image | `docker build -t zomato-rec .` | Image builds without errors |
| Run locally | `docker run -p 8501:8501 zomato-rec` | App accessible at localhost:8501 |
| Push to registry | `docker push <registry>/zomato-rec` | Image appears in registry |
| Deploy to cloud | Streamlit Cloud / Railway deploy | Public URL works |
| Set secrets | Add `OPENAI_API_KEY` in platform secrets | LLM calls succeed |
| Smoke test | Run 3 different queries on production | All return valid recommendations |

### Exit Criteria

- [ ] All end-to-end tests pass (happy path + edge cases)
- [ ] Average response time < 3 seconds
- [ ] App deployed and accessible via public URL
- [ ] README with setup instructions, screenshots, and demo
- [ ] Code is clean, commented, and pushed to Git

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM API costs spike | Medium | High | Cache identical queries, cap tokens, set budget alerts |
| LLM hallucinates restaurant data | High | High | Always pull numbers from dataset, validate names against candidates |
| Dataset has poor quality data | Medium | Medium | Thorough EDA in Phase 1, robust cleaning pipeline |
| LLM rate limits hit during demo | Low | High | Implement retry with backoff, have cached demo responses as fallback |
| Streamlit performance degrades | Low | Medium | Cache dataset in `st.cache_data`, minimize re-runs |

---

## Dependencies

```mermaid
flowchart LR
    classDef lib fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    classDef ext fill:#fce4ec,stroke:#c62828,stroke-width:2px,color:#000

    subgraph PYTHON [" 🐍 Python Libraries "]
        P1["pandas"]:::lib
        P2["datasets<br/>(huggingface)"]:::lib
        P3["openai / google-genai"]:::lib
        P4["streamlit"]:::lib
        P5["python-dotenv"]:::lib
        P6["pytest"]:::lib
    end

    subgraph EXTERNAL [" 🔌 External Services "]
        E1["Hugging Face Hub<br/>(dataset download)"]:::ext
        E2["OpenAI API / Gemini API<br/>(LLM inference)"]:::ext
        E3["Streamlit Cloud<br/>(hosting)"]:::ext
    end

    style PYTHON fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style EXTERNAL fill:#fce4ec,stroke:#c62828,stroke-width:1px
```

### `requirements.txt`

```
pandas>=2.0
datasets>=2.14
openai>=1.0
streamlit>=1.28
python-dotenv>=1.0
pytest>=7.0
```
