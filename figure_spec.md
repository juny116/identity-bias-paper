# Figure and Table Manifest for IEEE Access Draft

This file is the artifact contract for the paper draft in `paper/main.tex`.
All tables and figures should use frozen analysis outputs only. Prefer CSV or
Parquet source data plus a reproducible plotting script for every artifact.
Use percentage-point units for differences and rates in [0, 1] or percentages
consistently within each table. The manuscript currently emphasizes absolute
percentage-point effects in prose.

## Table 1: baseline-FAR-and-FRR-by-critic-dataset-interface

Data: All completed verdict-only, verdict-plus-repair, Caveat A, and Gemma
interface runs where available. Include actually wrong items for FAR and
actually correct items for FRR. Group by critic, dataset, prompt interface,
and optionally source condition if space allows. At minimum include
qwen3-no-think, gpt-oss-no-think, and Gemma if available.

Columns: critic, dataset, interface, n_wrong, FAR, FAR_CI_low, FAR_CI_high,
n_correct, FRR, FRR_CI_low, FRR_CI_high. If the journal table becomes too
wide, split source condition into an appendix table and make the main table
anonymous-only plus pooled-over-source-conditions.

Referenced in: Results subsection "Over-Acceptance Is the Dominant Baseline
Failure".

Approximate caption: "Baseline false-accept rate (FAR) on actually wrong
solutions and false-rejection rate (FRR) on actually correct solutions by critic,
dataset, and prompt interface. Confidence intervals are paired bootstrap
intervals over problem identifiers."

## Figure 1: paired-repair-inflation-two-critic

Data: Existing Phase E two-stage diagnostic for qwen3-no-think and
gpt-oss-no-think before Caveat A. Use all six source conditions and four
datasets, paired by problem_id and condition. Include FAR_verdict_only,
FAR_full_call, and paired difference for each critic.

Axes: x-axis critic; y-axis FAR. Use paired bars or connected dot pairs for
verdict-only and verdict-plus-repair. Annotate each critic with absolute
percentage-point delta: +8.9 pp for gpt-oss-no-think and +8.6 pp for
qwen3-no-think, unless recomputed frozen values differ.

Referenced in: Results subsection "Verdict+Repair Increases False Acceptance in
the Initial Two-Stage Diagnostic".

Approximate caption: "Initial two-stage diagnostic. Asking for a corrected
answer alongside the verdict increased false acceptance of wrong solutions for
both tested critics across all source conditions and datasets."

## Table 2: caveat-A-FAR-by-arm-per-critic

Data: Caveat A four-arm ablation. Include qwen3-no-think and
gpt-oss-no-think; include Gemma if the same four arms were run. Use only the
pre-specified sampled items. Results should be item-paired across arms.

Rows: critic, source_condition, dataset or pooled. Main table should have
pooled rows by critic and source condition plus an "all source conditions"
summary. Appendix version should include per-dataset rows.

Columns: n_wrong, FAR_verdict_only_instructed, FAR_verdict_only_neutral,
FAR_schema_matched, FAR_verdict_plus_repair, delta_repair_vs_neutral_pp,
CI_delta_repair_low_pp, CI_delta_repair_high_pp, delta_instructed_vs_neutral_pp,
delta_schema_vs_neutral_pp.

Referenced in: Results subsection "Caveat A Ablation: Separating Repair
Request, No-Repair Instruction, and Schema Complexity".

Approximate caption: "Caveat A prompt-interface ablation on paired sampled
items. The primary contrast is Verdict+Repair minus Verdict-Only Neutral."

## Figure 2: caveat-A-prompt-arm-forest-plot

Data: Same as Table 2, but model estimated contrasts should come from the
primary mixed-effects logistic model or paired bootstrap if model fitting fails.

Axes: y-axis critic and optionally source condition; x-axis absolute
percentage-point difference in FAR relative to Verdict-Only Neutral. Plot three
contrasts for each row: Verdict-Only Instructed minus Neutral, Schema-Matched
Verdict minus Neutral, and Verdict+Repair minus Neutral. Use a vertical zero
line and 95% confidence intervals.

Referenced in: Results subsection "Caveat A Ablation: Separating Repair
Request, No-Repair Instruction, and Schema Complexity".

Approximate caption: "Prompt-interface contrasts from the Caveat A ablation.
Positive values indicate increased false acceptance relative to the neutral
verdict-only prompt."

## Table 3: identity-condition-FAR-five-critics

Data: Main source-framing sweeps across five critic configurations. Include
self, other_model, anonymous, human, weak_model, and strong_model where
available. Use matched datasets per critic and clearly mark limited-N entries
for qwen3 think and gpt-oss-think strong_model.

Rows: critic, dataset scope, source condition.

Columns: n_wrong, FAR, FAR_CI_low, FAR_CI_high, delta_vs_anonymous_pp,
delta_CI_low_pp, delta_CI_high_pp, adjusted_p_value_for_delta if available.

Referenced in: Results subsection "Identity Labels Are Small Relative to
Interface Effects".

Approximate caption: "False-accept rates by source-framing condition. Ordinary
identity labels cluster tightly relative to the repair-interface effect, while
Weak Model framing produces a smaller skepticism effect."

## Figure 3: forest-plot-WEAK-effect-per-dataset

Data: Source-framing sweeps. For each critic and dataset, compute WEAK_MODEL
minus anonymous FAR on actually wrong solutions, paired by problem_id. Include
Gemma, qwen3-no-think, gpt-oss-no-think, and available think variants. Clearly
label sparse or limited-N points.

Axes: y-axis critic/dataset pair; x-axis WEAK minus anonymous FAR difference
in percentage points. Negative values mean WEAK reduces false acceptance. Use
95% paired bootstrap CIs and a vertical zero line.

Referenced in: Results subsection "Low-Competence Framing Is a Modest and
Asymmetric Skepticism Cue".

Approximate caption: "Effect of low-competence source framing on false
acceptance. Weak Model framing generally reduces FAR, but the magnitude varies
by critic and dataset."

## Figure 4: weak-strong-asymmetry-by-critic

Data: Matched source-framing runs containing anonymous, weak_model, and
strong_model for Gemma, qwen3-no-think, and gpt-oss-no-think. Use matched
datasets per critic. Include qwen3/gpt-oss think variants only in appendix if
strong_model is sparse.

Axes: x-axis critic; y-axis FAR delta versus anonymous in percentage points.
For each critic, show two bars or points: WEAK-anonymous and STRONG-anonymous,
with confidence intervals. Negative WEAK and near-zero STRONG should be visible.

Referenced in: Results subsection "Low-Competence Framing Is a Modest and
Asymmetric Skepticism Cue".

Approximate caption: "The Strong Model falsifier does not mirror the Weak Model
effect. Low-competence framing acts as an asymmetric skepticism cue rather than
a clean monotonic competence axis."

## Table 4: verdict-vs-repair-stage-WEAK-effects

Data: Two-stage diagnostics for qwen3-no-think and gpt-oss-no-think. If Caveat A
neutral verdict-only results supersede original verdict-only results, include
both original and neutral variants in separate columns or footnote. Compute
WEAK_MODEL minus anonymous FAR at the initial verdict stage and final/full-call
stage.

Rows: critic, stage/interface, n_wrong_anonymous, n_wrong_weak.

Columns: FAR_anonymous, FAR_weak, delta_weak_minus_anonymous_pp,
CI_delta_low_pp, CI_delta_high_pp.

Referenced in: Results subsection "Framing Effects Do Not Always Occur at the
Same Stage".

Approximate caption: "Stage-specific Weak Model effects. Source framing reduces
initial false acceptance for qwen3-no-think but not for gpt-oss-no-think,
indicating critic-dependent mechanisms."

## Table 5: gated-pipeline-outcome-breakdown

Data: Minimal mitigation experiment comparing one-shot Verdict+Repair against
gated Verdict-Then-Repair. Use the same sampled items as the Caveat A ablation
for anonymous and self conditions, at minimum qwen3-no-think and
gpt-oss-no-think. Include Gemma only if run.

Rows: critic, source_condition, pipeline, dataset or pooled.

Columns: n_wrong, wrong_accepted_rate, wrong_rejected_unrepaired_rate if any,
wrong_repaired_correct_rate, wrong_repaired_incorrect_rate, n_correct,
correct_accepted_rate, false_rejected_rate, harmful_correction_rate.

Referenced in: Results subsection "Gated Verdict-Then-Repair as a Minimal
Mitigation".

Approximate caption: "Outcome decomposition for the standard one-shot
Verdict+Repair pipeline and the gated Verdict-Then-Repair pipeline. The gated
pipeline tests whether logging verdicts before repair reduces false acceptance
without unacceptable side effects."

## Table 6: gemma-cross-critique-interface-results

Data: Gemma verdict-repair or Caveat A ablation on gpt-oss-think solutions.
If only anonymous was run, table should be anonymous-only. If anonymous,
other_model, and weak_model were run, include all three conditions. Use four
datasets and the same wrong/correct sample targets as the main ablation.

Rows: dataset and pooled summary, optionally source condition.

Columns: n_wrong, FAR_verdict_only_neutral, FAR_schema_matched,
FAR_verdict_plus_repair, delta_repair_vs_neutral_pp, CI_delta_low_pp,
CI_delta_high_pp, n_correct, FRR_verdict_only_neutral, FRR_verdict_plus_repair.

Referenced in: Results subsection "Cross-Critique Generalization with Gemma".

Approximate caption: "Gemma cross-critique prompt-interface results on
gpt-oss-think solutions. The table tests whether the repair-interface effect
extends beyond self-critique."

## Appendix Table A1: mixed-effects-model-coefficients

Data: Primary mixed-effects logistic regression and fallback cluster-robust
models if applicable.

Columns: outcome, model specification, coefficient/contrast, estimate log-odds,
odds ratio, standard error, confidence interval, p-value, adjustment family.

Referenced in: Methods "Statistical Analysis" and Appendix "Additional Tables".

Approximate caption: "Model-based estimates for primary and secondary contrasts.
Absolute percentage-point effects are reported in the main text; odds ratios
are included for completeness."

## Appendix Figure A1: per-dataset-repair-interface-effects

Data: Caveat A ablation, per critic and dataset.

Axes: y-axis critic/dataset pair; x-axis Verdict+Repair minus Verdict-Only
Neutral FAR in percentage points. Include confidence intervals and zero line.

Referenced in: Appendix and optionally Results if heterogeneity is important.

Approximate caption: "Per-dataset repair-interface effects from the Caveat A
ablation."

## Appendix Table A2: parse-failure-and-token-summary

Data: All critique logs used in main analyses.

Columns: critic, interface, source_condition, dataset, n_calls, parse_failures,
parse_failure_rate, mean_prompt_tokens, mean_completion_tokens.

Referenced in: Limitations and Methods "Logging Schema and Answer Checking".

Approximate caption: "Parse failure and token usage summary for critique calls
included in the analysis."
