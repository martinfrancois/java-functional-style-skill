# README Guidance

- Use `Java Functional Style Skill for AI Agents` as the README title, followed by the Tessl badge
  linking to the registry page.
- Say the repository and the Tessl plugin are public.
- Do not include benchmark claims until hosted evals are rerun and documented; link the Tessl
  plugin page for published scores once the package is public.
- README examples must use domains that no eval scenario uses; the criteria validator's overlap
  scan covers SKILL.md, the references, the rule, and the README.
- Install examples should use `martinfrancois/java-functional-style`.
- Explain that the package is useful alone and as a companion to:
  - `martinfrancois/java-streams`
  - `martinfrancois/java-optionals`
- Include the ownership boundary:
  - `java-functional-style` owns general Java lambda and functional-interface style.
  - `java-streams` owns stream and collector semantics.
  - `java-optionals` owns Optional semantics.
- Do not include the old stream origin story, JFokus talk, stream benchmark claims, or stream suite
  composition notes.
