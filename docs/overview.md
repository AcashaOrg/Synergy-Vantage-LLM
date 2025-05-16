# Project Documentation Overview

The **Synergy-Vantage Measure / Corrector Model** is an experimental framework
for iteratively improving code and text artifacts with the assistance of large
language models (LLMs). It follows a "propose → score → evolve" methodology
that gradually refines a population of candidate solutions.

## Core Components

- **Proposer Ensemble**  
  A set of LLMs (e.g. GPT-4o-Mini and GPT-4o-Pro) used to generate new program
  candidates. Breadth models create a wide variety of ideas while depth models
  refine the most promising ones.
- **Evaluator Cascade**  
  A tiered scoring pipeline that runs heuristics, unit tests and LLM-based
  critics. Failing candidates can optionally be flagged for human review.
- **Evolution Orchestrator**  
  Coordinates the loop. It loads configuration, seeds the program database,
  invokes proposers and evaluators, archives results and promotes winners.
- **Program DB**  
  Stores candidate programs, scores and audit information so that progress can be
  tracked over time.
- **Observability Layer**  
  Metrics and logs emitted via Prometheus and a DuckDB audit log to provide
  transparency into the system's behaviour.

## Propose → Score → Evolve Loop

1. **Seed Program DB** with initial examples or load an existing population.
2. **Sample prompts & hyper-mutations** from configuration or prior runs.
3. **Generate candidates** using the Proposer Ensemble.
4. **Evaluate candidates** through the Evaluator Cascade.
5. **Select top performers** and archive failures for later study.
6. **Promote winners** back into the Program DB (and optionally emit pull
   requests upstream).
7. **Iterate** until a fitness delta falls below a threshold or a token budget is
   exhausted.

This loop allows the project to gradually measure alignment and quality, then
correct or refine generated programs with feedback from both automated tests and
LLM critics.
