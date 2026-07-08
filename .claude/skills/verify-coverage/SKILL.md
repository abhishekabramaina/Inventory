---
name: verify-coverage
description: Run the project's test suite in an isolated subprocess and report the result. Use when asked to run tests, verify test coverage, or check that the test suite passes.
context: fork
---

# verify-coverage

Runs the CCAF test suite in an isolated subprocess so it cannot mutate the active
shell or development environment.

## Execution steps

1. **Run in an isolated subprocess** — invoke the suite as its own process so
   environment variables and working state don't leak back into the session:

    ```bash
    python -m pytest
    ```

2. **Report the result** — surface the full stdout/stderr and the process exit code.

## Success criteria

- [ ] Process exits cleanly with status code `0`.
- [ ] Test output is shown to the user.

## Notes

- `tests/test.py` is currently a placeholder (`test_placeholder`) invoked directly;
  there is no coverage tooling (e.g. `coverage`/`pytest-cov`) wired up yet. When real
  coverage reporting is added, update the command above (e.g. `coverage run` +
  `coverage report`) and the success criteria to assert line/branch/function coverage.
- Testing conventions live in `.claude/rules/testing.md`.
