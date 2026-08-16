# 🍽️ Zomato AI Restaurant Recommender

An AI-powered restaurant recommendation system that combines structured data filtering with LLM-based reasoning to deliver personalized, human-readable restaurant suggestions.

## 🏗️ Architecture

```
User Preferences → Filtering Engine → LLM Prompt → AI Recommendations
                        ↑
               Zomato Dataset (10K+ restaurants)
```

See [architecture.md](./architecture.md) for the full system design.

## 📁 Project Structure

```
├── src/
│   ├── data_loader.py        # Dataset loading & caching
│   ├── data_cleaner.py       # Preprocessing & normalization
│   ├── filter_engine.py      # Deterministic filtering (Phase 2)
│   ├── prompt_builder.py     # LLM prompt construction (Phase 3)
│   ├── llm_client.py         # OpenAI / Gemini API client (Phase 3)
│   ├── output_formatter.py   # Response parsing & validation (Phase 3)
│   └── app.py                # Streamlit UI (Phase 4)
├── tests/                    # pytest test suite
├── data/                     # Local dataset cache (gitignored)
├── notebooks/                # EDA & exploration
├── docs/                     # Documentation
├── requirements.txt          # Python dependencies
└── architecture.md           # System architecture document
```

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone <repo-url>
cd zomato-recommender

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
# Edit .env and add your OpenAI or Gemini API key
```

### 3. Load Dataset

```python
from src.data_loader import load_dataset
from src.data_cleaner import clean_dataset

raw_df = load_dataset()          # Downloads from HuggingFace (first time)
clean_df = clean_dataset(raw_df) # Preprocesses and normalizes
```

### 4. Run Tests

```bash
pytest tests/ -v
```

### 5. Run App (Phase 4)

```bash
streamlit run src/app.py
```

## 📊 Dataset

- **Source:** [HuggingFace – zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)
- **Size:** ~10,000+ restaurants across major Indian cities
- **Key Fields:** Name, City, Cuisines, Rating, Cost, Votes, Online Delivery, Table Booking

## 📚 Documentation

| Document | Description |
|---|---|
| [Problem Statement](./problemStatement.md) | Original project requirements |
| [Architecture](./architecture.md) | System design & component details |
| [Implementation Plan](./implementation-plan.md) | Phase-wise development roadmap |
| [Edge Cases](./edge-cases.md) | 22 edge cases with handling strategies |
| [Evaluation Plan](./eval.md) | Testing framework & quality rubrics |

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+ / FastAPI |
| Data | Pandas + HuggingFace Datasets |
| AI | OpenAI GPT-4o / Google Gemini |
| Frontend | Streamlit |
| Deployment | Docker + Cloud Run |
