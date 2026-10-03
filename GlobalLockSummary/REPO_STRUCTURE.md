# Repository structure

This repo is organized around a static content + build pipeline for global lock summary documentation.

```text
GlobalLockSummary/
├── README.md
├── .gitignore
├── package.json
├── build.mjs
├── serve.mjs
├── .github/
├── assets/
├── content/
├── src/
├── tests/
├── tools/
└── ...
```

## Notes

- `content/` and `src/` drive the generated output.
- `build.mjs` and `serve.mjs` are the primary build/runtime scripts.
