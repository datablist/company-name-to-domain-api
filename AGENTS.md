# API Example Guidelines

These files are learning material. Keep the API calls visible and the workflow
easy to read from top to bottom.

- Keep the basic sync and async examples self-contained.
- Only CSV examples may import the corresponding basic example.
- Use basic parameter and return type hints and clear intermediate variables.
- Keep batching in the CSV examples, with at most 10,000 inputs per task.
- Do not add frameworks, shared helpers, configurable timeouts, retries, or
  custom error handling unless explicitly requested.
- Keep verification local and mocked. Do not run paid API calls without an
  explicit request. Do not publish changes without an explicit request.

When this repository is inside the Datablist workspace, also read the example
folder instructions at `../AGENTS.md`, the workspace instructions at
`../../AGENTS.md`, and the architecture index at
`../../datablist-architecture/README.md`. Those workspace files are not part of
a standalone checkout.
