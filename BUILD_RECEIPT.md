# Build receipt

Validated on 2026-06-18.

| claim | instrument | current evidence | status | caveat |
|---|---|---|---|---|
| Main spine is tighter | `wc -w` against prior cleaned Fable | 1,099 → 731 words (`−33.5%`) | verified | Brevity does not prove behavioral quality |
| Main skill references resolve | path validator | 9/9 referenced files exist | verified | Does not judge prose correctness |
| Python scaffold is syntactically valid | `python -m py_compile` | exit status 0 | verified | Domain hooks intentionally remain unimplemented |
| Strict amount parser handles tested cases | executable assertions | 4/4: grouped currency, integer, malformed decimal, embedded text | verified | Not a complete international-currency parser |
| Skill and candidate frontmatter parse | `yaml.safe_load` | 2/2 parsed | verified | A target runtime may impose additional conventions |
| Retention requires evidence and staged evaluation | static gate checks | dedupe, quarantine, positive/negative/boundary cases, and retrospective limits present | verified | Confirms the files contain the gates, not that an agent will obey them |
| Retained skills improve future-agent performance | clean with/without-skill benchmark | not run in the target agent environment | unverified | Keep candidates staged until target-environment evals pass |
