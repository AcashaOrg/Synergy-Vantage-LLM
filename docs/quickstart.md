# Quickstart Guide

Follow these steps to run the Synergy‑Vantage evolution loop locally.

## Installation

```bash
# Clone the repository
git clone https://github.com/AcashaOrg/Synergy-Vantage-LLM.git
cd Synergy-Vantage-LLM

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

Create a `.env` file with any required API keys (e.g. `OPENAI_API_KEY`).

## Running the Orchestrator

```bash
python src/synergy_vantage_model/orchestrator.py
```

The orchestrator will load `configs/default.yaml` and begin the propose → score → evolve loop. Logs and evaluation reports are saved in the directories defined in the config:

- Checkpoints: `checkpoints/`
- Evaluation reports: `reports/eval/`
- Audit log (DuckDB): `logs/audit.duckdb`

## Next Steps

Explore the code in `src/`, especially the orchestrator and evaluator modules, to customise the workflow.
