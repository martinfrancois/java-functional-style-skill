# Public Metadata And OSS Readiness

Keep the repository open-source-ready even while private.

## Plugin Metadata

- Package: `martinfrancois/java-functional-style`
- Repository: `https://github.com/martinfrancois/java-functional-style-skill`
- License: MIT
- Entrypoint: `README.md`
- Private: `true`

Preferred summary:

```text
Java functional style guidance for lambdas, method references, identity functions, callbacks, and functional interfaces.
```

Preferred description:

```text
Help AI coding agents write, review, and refactor Java lambdas, method references, functional interfaces, identity functions, suppliers, predicates, consumers, and callbacks with behavior-preserving readability.
```

## Safety

- Do not commit secrets, private hosted eval artifacts, private logs, local machine paths, or
  non-public tokens.
- Real Tessl publishes run only through the release workflow.
- Tessl publish dry-runs are allowed.
- `.tessl-plugin/plugin.json` must keep `"private": true` until explicitly changed.
