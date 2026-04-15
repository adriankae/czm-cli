# Install

## Requirements

- Python 3.12 or newer
- A running backend API

## Recommended local install

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the CLI in editable mode:

```bash
PIP_INDEX_URL=https://pypi.org/simple python3 -m pip install -e .
```

Verify the command is available:

```bash
czm --help
```

If you install with user-site `pip`, the script may land in a user bin directory such as `~/Library/Python/3.13/bin`. Add that directory to `PATH` or use a virtual environment instead.

