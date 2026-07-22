```markdown
# gcp-data-platform-blueprint Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill provides guidance on developing and maintaining Python code in the `gcp-data-platform-blueprint` repository. It covers coding conventions, commit patterns, and testing practices observed in the codebase. The repository is designed for building data platform solutions on Google Cloud Platform (GCP), focusing on maintainable, testable, and convention-driven Python code.

## Coding Conventions

### File Naming
- Use **snake_case** for all file names.
  - Example: `data_loader.py`, `etl_utils.py`

### Import Style
- Use **relative imports** within the package.
  - Example:
    ```python
    from .utils import load_config
    from ..common import logger
    ```

### Export Style
- Use **named exports**; explicitly specify what is exported from modules.
  - Example:
    ```python
    __all__ = ['DataLoader', 'process_data']
    ```

### Commit Patterns
- Use **conventional commit** messages.
- Prefix commit messages with the type, such as `fix`.
- Average commit message length: ~45 characters.
  - Example:
    ```
    fix: correct data schema validation in loader
    ```

## Workflows

_No automated workflows detected in this repository._

## Testing Patterns

- **Test Framework:** Unknown (no framework detected).
- **Test File Pattern:** Test files are named with the pattern `*.test.*`
  - Example: `data_loader.test.py`
- **Test Structure:** Place test files alongside the modules they test, using the `.test.` infix in the filename.

#### Example Test File
```python
# data_loader.test.py

from .data_loader import DataLoader

def test_load_valid_data():
    loader = DataLoader()
    result = loader.load('sample.csv')
    assert result is not None
```

## Commands
| Command | Purpose |
|---------|---------|
| /test   | Run all test files matching `*.test.*` |
| /fix    | Commit a fix using the conventional commit pattern |
```
