# IZI
Simple app to setup all environments you need to quick start contributing and developing for DNX.

## Quick start
Get everything you need from dnx in 4 steps.

1. Download the latest release with the command.
```
# linux
curl -L https://github.com/DNXLabs/izi/releases/latest/download/izi_linux_amd64 -o izi

# macos
curl -L https://github.com/DNXLabs/izi/releases/latest/download/izi_macos_amd64 -o izi
```

2. Make the izi binary executable.
```
chmod +x ./izi
```

3. Move the binary in to your PATH.
```
sudo mv ./izi /usr/local/bin/izi
```

4. Test to ensure the version you installed is up-to-date.
```
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
pip3 install -r requirements.txt
pip3 install --editable .
```

#### Run
```bash
$ izi
```
## Creating a personal access token

#### GitLab
You can create as many personal access tokens as you like from your GitLab profile.

1. In the upper-right corner, click your avatar and select **Settings**.
2. On the **User Settings** menu, select **Access Tokens**.
3. Choose a name and optional expiry date for the token.
4. Choose the desired scopes.
5. Click the **Create personal access token** button.
6. Save the personal access token somewhere safe. Once you leave or refresh the page, you won’t be able to access it again.
7. Revoking a personal access token
8. At any time, you can revoke any personal access token by clicking the respective Revoke button under the Active Personal Access Token area.


## Author
App managed by DNX Solutions.

## License
Apache 2 Licensed. See LICENSE for full details.