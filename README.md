# ASCII Art Studio
## Instructions on how to run and test 'ASCII Art Studio'.

### Install 'pipx'
https://pipx.pypa.io/stable/how-to/install-pipx.html

### Install 'uv'
```bash
pipx install uv
```

### Sync dependencies
At this point, 'uv' will install all the packages and the app itself in a virtual environment.
```bash
uv sync
```

### Run ASCII Art Studio (aas)
```bash
uv run aas
```

### Run test
Besides running the tests, a coverage report is also created.
```bash
uv run pytest
```

### Clean up the mess
```bash
./clean
```

## Where to find the report?
'report.pdf' at the same dir as this 'README.md'.
