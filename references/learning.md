# Play: Retain verified learning — stage, test, promote

Use after the current task is complete and verified, or when explicitly asked to save a lesson as a skill. Do not run merely because a task was long.

## Extraction gate

Create a candidate only when all are true:

- **Verified:** the mechanism and solution have receipts in the proof table.
- **Reusable:** it addresses a recurring class of work, not one incident.
- **Non-obvious:** it adds discovered mechanism, boundary, or workflow beyond a routine documentation lookup.
- **Retrievable:** exact symptoms, errors, technologies, files, or context markers can be named.
- **Bounded:** near-misses and cases where it should not activate are known.
- **Safe to persist:** no credentials, private URLs, personal data, proprietary payloads, or unnecessary internal identifiers.

If any gate fails, keep a brief note if useful; do not create a skill.

## 1. Search before writing

Search project and user skill libraries by:

- candidate name and domain;
- exact error or symptom text;
- technology, file, command, function, and config markers;
- mechanism and proposed fix.

Choose deliberately:

| Existing knowledge | Action |
|---|---|
| Same trigger and mechanism | Update the existing skill |
| Same trigger, different mechanism | Create a separate skill and cross-link |
| Partial overlap, cohesive variant | Add a variant and bump minor version |
| Stale or wrong | Deprecate, preserve the disproof, and link the replacement |
| No meaningful overlap | Create a new candidate |

## 2. Choose scope

Default to **project** scope when the lesson depends on repository conventions, architecture, internal tools, or local configuration. Use **user** scope only when the trigger and procedure transfer cleanly across projects.

## 3. Stage outside the active library

Use `assets/skill_candidate_template.md`. Do not write directly into an auto-loaded skill directory.

The candidate must contain:

- a precise retrieval description;
- trigger and non-trigger conditions;
- verified mechanism and procedure;
- the observed receipt and coverage limits;
- a negative case and revalidation conditions;
- lifecycle links to related, replaced, or deprecated skills.

## 4. Evaluate in a clean context

Run the same cases **without** and **with** the candidate. At minimum include:

1. a positive trigger;
2. a near-miss negative that must not activate or mislead;
3. a boundary or version variant.

Prefer fresh sessions or isolated workers so the evaluator does not inherit the original solution. Score correctness first; then useful secondary measures such as steps, tool calls, duration, or token cost. A candidate passes only if it improves the positive case without regressing the negative or boundary cases.

When clean evaluation is unavailable, keep `status: candidate` and state the limitation. Do not promote on self-review alone.

## 5. Promote and maintain

After a passing evaluation:

- move the skill into the chosen active scope;
- set the lifecycle metadata to `active`, record the validation date, and add revalidation triggers;
- use patch for wording/fixes, minor for new compatible scenarios, and major for changed behavior or replacement;
- cross-link related skills;
- deprecate rather than silently overwrite stale guidance;
- archive when no supported environment remains.

## Retrospective mode

When explicitly asked “what did we learn?” or “save this as a skill,” identify at most three candidates, rank them by **reuse × future cost saved × evidence strength**, and run the extraction gate. Promoting none is a valid result.

## Anti-patterns

- Always-on reminders that pressure every task to produce a lesson
- Vague descriptions such as “helps with React”
- Copying official documentation without adding discovered value
- Direct writes into the live skill library
- Promotion without a negative case or clean comparison
- Treating “the fix worked once” as proof of a general rule
