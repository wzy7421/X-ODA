# X-ODA

Revision-support code for **X-ODA: An End-to-End Oral Diagnostic System Integrating Multimodal Explainable AI and Large Language Model Agents**.

This repository is structured to support the revised ESWA manuscript. It contains:

- author-replaceable provisional result data for the newly added review-response analyses;
- scripts to regenerate the revised manuscript tables and user-study figure;
- privacy-aware payload construction for external LLM/API calls;
- the visual-grounding prompt template used by the LangGraph agent.

No raw clinical images, patient identifiers, EHR exports, API keys, or private reviewer documents are stored in this repository.

## Quick Start

```powershell
python -m pip install -r requirements.txt
python scripts/validate_revision_results.py
python scripts/generate_revision_outputs.py --results data/provisional_revision_results.json --out outputs
```

Generated files will be written to `outputs/`:

- `table2_baseline_latency.csv`
- `table3_ood_generalization.csv`
- `table4_xai_benchmark.csv`
- `table5_agent_workflow.csv`
- `table6_user_study_stats.csv`
- `fig9_user_study_summary.png`

## Important Author Note

The numbers in `data/provisional_revision_results.json` are **provisional drafting values** prepared for manuscript revision scaffolding. Replace them with final experiment logs, statistical outputs, ethics metadata, and user-study records before journal submission.

The validation script intentionally checks reviewer-facing constraints: all six XAI methods requested in the revision are present, the OOD table contains both primary optical and CBCT rows, workflow cases sum correctly, confidence intervals are well formed, and reported percentages/latencies are in valid ranges.

## Privacy Design

The revised manuscript states that external API calls should receive only de-identified structured evidence. The helper in `src/xoda/privacy.py` enforces that policy by accepting only:

- pseudonymous case ID;
- CNN prediction label;
- calibrated confidence;
- CAM-derived morphology;
- optional non-identifying clinical note.

It rejects obvious patient identifiers and never includes raw image bytes.

## Repository Layout

```text
data/
  provisional_revision_results.json
figures/
  Fig2_XODA_graphical_abstract_gpt_image2.png
  Fig3_LLM_agent_decision_logic_gpt_image2.png
  Fig5_system_architecture_gpt_image2.png
scripts/
  generate_revision_outputs.py
  validate_revision_results.py
src/xoda/
  metrics.py
  privacy.py
  prompting.py
```
