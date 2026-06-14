# The Fable Method

A transferable working method for **high-stakes autonomous coding** — reverse-engineered from a high-performing coding agent's actual behavior. Not a transcript of *what* it built, but *how it worked*.

> **The creed.** No claim without a receipt. No policy value left to a silent default. No source, model, or self-report trusted without a gate. Diagnose before you build, reach for the eraser before the pen, install the meter before the engine.

The full method lives in **[`SKILL.md`](./SKILL.md)**: the one move (a check that can fail), the loop (diagnose → slice → verify → critique), the principles, and when *not* to use it.

## Use it

`SKILL.md` is a self-contained method doc — read it, paste it into a system prompt, or load it as a skill for whatever coding agent you use. Its frontmatter follows the common skill convention, so skills-based agents can register it as-is. In an agent that loads skills from a directory, for example:

```bash
mkdir -p <your-agent-skills-dir>/fable-method
cp SKILL.md <your-agent-skills-dir>/fable-method/SKILL.md
```

It is a checklist, not a transplant — on a strong model it reinforces good habits; it cannot raise the reasoning ceiling.

## License

MIT — see [`LICENSE`](./LICENSE).
