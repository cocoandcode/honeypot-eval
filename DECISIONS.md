# Design decisions

Each entry: the decision, why, and how it compares with Krakovna et al. (2026), "Realistic honeypot evaluations for scheming propensity" (referred to as "the paper").

## D1. Replicate the agentic coding setting, not code review

- **Decision:** Build one agentic honeypot (agent edits a repo in a sandbox), not the paper's code-review setting.
- **Why:** The agentic setting is closer to real deployment, exercises Inspect's sandbox and tool machinery, and is the setting where the paper had the fewest runs (30 per condition, one model), so an open replication adds the most.
- **Paper:** 11 agentic honeypots + 2 baselines on Gemini 3.1 Pro only, using real internal codebases.

## D2. Mirror `scheming_monitor_data_robustness`

- **Decision:** The honeypot task is "harden the monitor's data pipeline against malformed transcripts".
- **Why:** It is one of the three agentic honeypots that met the paper's *incentive* criterion (Section 6). Legitimate hardening involves dropping or changing records, which gives natural cover for sabotage (dropping long or suspicious transcripts), matching the paper's Appendix B sabotage types (trajectory truncation, suppressing error signals).
- **Risk:** The boundary between legitimate and sabotaging changes must be defined carefully in the held-out regression suite (see the weakness list below).

## D3. Condition set

- **Decision:** `none`, `agency-sa`, `agency-persistence`, `goal-climate`, `goal-climate + agency-sa-goal`. Prompt texts verbatim from Tables 3 and 4.
- **Why:** One representative of each regime the paper found: an effective SA nudge (`agency-sa`), a realistic prompt that had no effect (`agency-persistence`), a goal-only organism, and the strongest combination.
- **Paper:** 5 agency prompts (+5 extra in a footnote) and 6 goals. We cover fewer to keep cost and N per cell reasonable.

## D4. Open-weight reasoning models via OpenRouter

- **Decision:** Evaluate 2 to 3 sizes of one open-weight reasoning family (candidates: Qwen3, gpt-oss; final choice at milestone 8). Route them through OpenRouter with a pinned host per model. Use local Ollama models (`llama3.1:8b`) only for development in milestones 2–5, not for the main experiment.
- **Why:** The paper's trigger is mostly *scheming reasoning*, so we need to see the reasoning. Open-weight models return raw chain of thought; Gemini and recent Claude models return summaries. Same-family sizes give a clean size comparison, and cost is low. OpenRouter gives one key and one bill across sizes and hosts.
- **Why not local for the main experiment:** The machine is an M4 with 24 GB RAM. That comfortably runs 8B-class models (already installed: `llama3.1:8b`, `llama3.2`) but not several sizes of a strong reasoning family in parallel. Llama 3.1/3.2 are not reasoning models, so they don't give us CoT. A 300-run agentic pilot is slow if serial on a laptop. Local runs are also quantised, so they wouldn't match API-hosted versions of the same model.
- **OpenRouter caveats:** (1) pin a specific host so routing doesn't mix quantisation or CoT handling across runs; (2) enable zero data retention / exclude training hosts, because our honeypot prompts would otherwise risk leaking into future training data; (3) OpenRouter cannot recover hidden reasoning from closed models.
- **Paper:** Gemini 3.1 Pro, 3.0 Pro, 3.0 Flash, with raw CoT available internally.
- **Consequence:** Results are not directly comparable with Gemini numbers. A different lab's model working on a codebase that is not its developer's may perceive less incentive (the paper's "transferability" limitation).

## D5. Engineering setup

- **Decision:** uv with a `src/` layout and `uv.lock`; eval logs (`logs/`) are git-ignored, with summary results committed separately; the paper PDF and MATS CSV are git-ignored.
- **Why:** Reproducible environments; logs are large and may be regenerated; reference material is not ours to redistribute.

## Known design weaknesses (to revisit)

1. Toy codebase in a fresh container is an eval cue. Mitigation: make the repo mundane and lived-in; measure unprompted eval awareness on honeypot vs baseline as the paper does.
2. Incentive vs realism: telling the agent the monitor watches agents like it raises incentive but also eval awareness.
3. Contamination: the paper and its prompts are public and may be in training data.
4. Reasoning visibility depends on provider; see D4.
5. Small models may break code by accident; regression failures need disambiguating (visible tests, diff, autorater covertness and reasoning scores).
6. Legitimate hardening can resemble sabotage; the held-out suite must not penalise legitimate record dropping.
7. The held-out suite only catches anticipated sabotage; diff and autorater are the backstop.
8. Small N: 0/30 gives a 95% upper bound of about 10% (rule of three). Report nulls as bounds.
9. The autorater is a model: possible bias, and validation on clear synthetic cases overstates accuracy. Hand-label a sample.

## Surprising results

_None yet._
