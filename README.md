# IZI
Simple app to setup all environments you need to quick start contributing and developing for DNX.

## Quick start
Get everything you need from dnx in 3 steps.
```bash
# linux
curl -L https://github.com/DNXLabs/izi/releases/latest/download/izi_linux_amd64 -o izi

# macos
curl -L https://github.com/DNXLabs/izi/releases/latest/download/izi_macos_amd64 -o izi

chmod +x ./izi

sudo mv ./izi /usr/local/bin/izi

izi --help
```

## Usage
```
Usage: izi [OPTIONS] COMMAND [ARGS]...

  A CLI to setup all environments you need to quick start contributing and
  developing for DNX

Options:
  --help  Show this message and exit.

Commands:
  get     Download the bubbletea stack, modules and tools.
  init    Start a new project using the latest commit from all bubbletea...
  link    Create symbolic link between modules and the stack you pass as...
  mount   Rewrite all modules sources to the local modules from the stack...
  unlink  Delete symbolic link if exists between modules and the stack you...
```

## Setup

## Dependencies
- Python 3

#### Install dependencies
```bash
pip install -r requirements.txt
pip install --editable .
```

#### Run
```bash
$ izi
```

## Author
App managed by DNX Solutions.

## License
Apache 2 Licensed. See LICENSE for full details.