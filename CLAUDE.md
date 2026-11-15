# CLAUDE.md

See **[AGENTS.md](AGENTS.md)** for everything about this repository: what it
is, the file layout, how the `!include` wiring works, the YAML conventions,
naming/language rules, secrets handling, and the validate/deploy/commit
workflows.

Two things worth repeating here:

- This configuration drives a real house. `./deploy-kubernetes.sh` pushes it to
  the live Home Assistant instance — only run it when explicitly asked.
- There is no linter or test suite. Verify that YAML parses and that every
  entity id you reference actually exists before claiming a change works.
