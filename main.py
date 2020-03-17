import git
import json
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

input_file = open(resource_path('repos.json'))
json_obj   = json.load(input_file)

bubbletea_array = json_obj['bubbletea']
tools_array     = json_obj['tools']
modules_array   = json_obj['modules']

GITLAB_BASE_URL          = "git@gitlab.com:DNXLabs/"
GITHUB_BASE_URL          = "git@github.com:DNXLabs/"
BUBBLETEA_REPOSITORY_URL = "bubbletea/aws-platform/"
GIT                      = ".git"


def clone_repositories():
    # Bubbletea clone action
    if not os.path.exists('bubbletea'):
        os.makedirs('bubbletea')
        for repository in bubbletea_array:
            git.Git("./bubbletea").clone(GITLAB_BASE_URL + BUBBLETEA_REPOSITORY_URL + repository + GIT)
            print("Cloned " + repository)
    else:
        print("Skipping bubbletea configuration, folder already exist")

    # Modules clone action
    if not os.path.exists('modules'):
        os.makedirs('modules')
        for repository in modules_array:
            git.Git("./modules").clone(GITHUB_BASE_URL + repository + GIT)
            print("Cloned " + repository)
    else:
        print("Skipping modules configuration, folder already exist")

    # Tools clone action
    if not os.path.exists('tools'):
        os.makedirs('tools')
        for repository in tools_array:
            git.Git("./tools").clone(GITHUB_BASE_URL + repository + GIT)
            print("Cloned " + repository)
    else:
        print("Skipping tools configuration, folder already exist")

if __name__ == '__main__':
    clone_repositories()