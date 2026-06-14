# Play: Research / synthesis / proposing what to build — mine self-skeptically

> **Entity-resolution claim re-grounded by falsifiable test.** The named-entity check was reproduced with real package-registry queries. The independent-source and adversarial-self-pass claims are process hygiene and qualitative judgment; ground them in your own work.

1. **Adversarial pass over your own output before delivery.** Kill anything that duplicates something already built, requires a capability you lack, or is scaffolding rather than a mechanism.
2. **Use independent sources where the claim needs them.** For external factual claims, research findings, or non-obvious recommendations, require at least two independent sources and state the count. Independent means they do not merely repeat the same upstream claim, vendor page, press release, README, or benchmark.
3. **Use authoritative artifacts for repo-local claims.** A failing test, git history, runtime log, source file, package-registry response, or compiler/typechecker result can be the source of truth. Do not demand two sources where one artifact is authoritative.
4. **Verify named external entities before depending on them.** Model IDs, package versions, endpoints, CLI flags, and APIs must resolve. If one does not resolve, stop unless an explicit fallback policy already exists. Show the disproof and never silently substitute the nearest plausible match.
5. **Keep an examined/refuted list.** Killed ideas stay visible with reasons so they do not come back under a different name.
6. **Name a surviving weakness.** If the output has a caveat, boundary, or untested assumption, say it.

## Worked receipt

Asked to add a fuzzy-matching dependency, an agent proposed a plausible package name. The naive path depended on it unverified; a real query to PyPI showed the proposed name and three plausible variants returned 404, so `pip install` would fail. The self-mining path verified resolution first, stopped on the 404, surfaced the disproof, and presented a verified alternative (`rapidfuzz`, confirmed status 200) as a flagged choice rather than silently substituting it.
