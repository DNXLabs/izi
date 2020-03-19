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
        if not os.path.exists('./bubbletea/' + repository):
            git.Git("./bubbletea").clone(GITLAB_BASE_URL + BUBBLETEA_REPOSITORY_URL + repository + GIT)
            print("Cloned " + repository)
        else:
            print("Skipping module" + repository + "configuration, folder already exist")

    # Modules clone action
    if not os.path.exists('modules'):
        os.makedirs('modules')

    for repository in modules_array:
        if not os.path.exists('./modules/' + repository):
            git.Git("./modules").clone(GITHUB_BASE_URL + repository + GIT)
            print("Cloned " + repository)
        else:
            print("Skipping module" + repository + "configuration, folder already exist")

    # Tools clone action
    if not os.path.exists('tools'):
        os.makedirs('tools')

    for repository in tools_array:
        if not os.path.exists('./tools/' + repository):
            git.Git("./tools").clone(GITHUB_BASE_URL + repository + GIT)
            print("Cloned " + repository)
        else:
            print("Skipping module" + repository + "configuration, folder already exist")

    # Link bubbletea with modules
    print("Checking infra-bubbletea-app-platform links")

    if not os.path.exists('./bubbletea/infra-bubbletea-app-platform/terraform-aws-db-monitoring'):
        os.symlink(os.path.abspath("modules/terraform-aws-db-monitoring"), os.path.abspath("./bubbletea/infra-bubbletea-app-platform/terraform-aws-db-monitoring"))
    if not os.path.exists('./bubbletea/infra-bubbletea-app-platform/terraform-aws-ecs'):
        os.symlink(os.path.abspath("modules/terraform-aws-ecs"), os.path.abspath("./bubbletea/infra-bubbletea-app-platform/terraform-aws-ecs"))
    if not os.path.exists('./bubbletea/infra-bubbletea-app-platform/terraform-aws-ecs-app'):
        os.symlink(os.path.abspath("modules/terraform-aws-ecs-app"), os.path.abspath("./bubbletea/infra-bubbletea-app-platform/terraform-aws-ecs-app"))
    if not os.path.exists('./bubbletea/infra-bubbletea-app-platform/terraform-aws-ecs-app-front'):
        os.symlink(os.path.abspath("modules/terraform-aws-ecs-app-front"), os.path.abspath("./bubbletea/infra-bubbletea-app-platform/terraform-aws-ecs-app-front"))
    if not os.path.exists('./bubbletea/infra-bubbletea-app-platform/terraform-aws-static-app'):
        os.symlink(os.path.abspath("modules/terraform-aws-static-app"), os.path.abspath("./bubbletea/infra-bubbletea-app-platform/terraform-aws-static-app"))

    print("Checking infra-bubbletea-domain link")

    if not os.path.exists('./bubbletea/infra-bubbletea-domain/terraform-aws-hostedzone'):
        os.symlink(os.path.abspath("modules/terraform-aws-hostedzone"), os.path.abspath("./bubbletea/infra-bubbletea-domain/terraform-aws-hostedzone"))

    print("Checking infra-bubbletea-mgmt-services link")

    if not os.path.exists('./bubbletea/infra-bubbletea-mgmt-services/terraform-aws-ecr'):
        os.symlink(os.path.abspath("modules/terraform-aws-ecr"), os.path.abspath("./bubbletea/infra-bubbletea-mgmt-services/terraform-aws-ecr"))
    if not os.path.exists('./bubbletea/infra-bubbletea-mgmt-services/terraform-aws-gitlab-runner'):
        os.symlink(os.path.abspath("modules/terraform-aws-gitlab-runner"), os.path.abspath("./bubbletea/infra-bubbletea-mgmt-services/terraform-aws-gitlab-runner"))

    print("Checking infra-bubbletea-network link")

    if not os.path.exists('./bubbletea/infra-bubbletea-network/terraform-aws-ecs'):
        os.symlink(os.path.abspath("modules/terraform-aws-ecs"), os.path.abspath("./bubbletea/infra-bubbletea-network/terraform-aws-ecs"))
    if not os.path.exists('./bubbletea/infra-bubbletea-network/terraform-aws-ecs-app'):
        os.symlink(os.path.abspath("modules/terraform-aws-ecs-app"), os.path.abspath("./bubbletea/infra-bubbletea-network/terraform-aws-ecs-app"))
    if not os.path.exists('./bubbletea/infra-bubbletea-network/terraform-aws-network'):
        os.symlink(os.path.abspath("modules/terraform-aws-network"), os.path.abspath("./bubbletea/infra-bubbletea-network/terraform-aws-network"))

    print("Checking infra-bubbletea-network-peering link")

    if not os.path.exists('./bubbletea/infra-bubbletea-network-peering/terraform-aws-vpc-peering'):
        os.symlink(os.path.abspath("modules/terraform-aws-vpc-peering"), os.path.abspath("./bubbletea/infra-bubbletea-network-peering/terraform-aws-vpc-peering"))

    print("Checking infra-bubbletea-openvpn link")

    if not os.path.exists('./bubbletea/infra-bubbletea-openvpn/terraform-aws-ecs'):
        os.symlink(os.path.abspath("modules/terraform-aws-ecs"), os.path.abspath("./bubbletea/infra-bubbletea-openvpn/terraform-aws-ecs"))
    if not os.path.exists('./bubbletea/infra-bubbletea-openvpn/terraform-aws-openvpn'):
        os.symlink(os.path.abspath("modules/terraform-aws-openvpn"), os.path.abspath("./bubbletea/infra-bubbletea-openvpn/terraform-aws-openvpn"))

    print("Checking infra-bubbletea-root link")

    if not os.path.exists('./bubbletea/infra-bubbletea-root/terraform-aws-account'):
        os.symlink(os.path.abspath("modules/terraform-aws-account"), os.path.abspath("./bubbletea/infra-bubbletea-root/terraform-aws-account"))
    if not os.path.exists('./bubbletea/infra-bubbletea-root/terraform-aws-account-security'):
        os.symlink(os.path.abspath("modules/terraform-aws-account-security"), os.path.abspath("./bubbletea/infra-bubbletea-root/terraform-aws-account-security"))
    if not os.path.exists('./bubbletea/infra-bubbletea-root/terraform-aws-audit'):
        os.symlink(os.path.abspath("modules/terraform-aws-audit"), os.path.abspath("./bubbletea/infra-bubbletea-root/terraform-aws-audit"))
    if not os.path.exists('./bubbletea/infra-bubbletea-root/terraform-aws-audit-member'):
        os.symlink(os.path.abspath("modules/terraform-aws-audit-member"), os.path.abspath("./bubbletea/infra-bubbletea-root/terraform-aws-audit-member"))
    if not os.path.exists('./bubbletea/infra-bubbletea-root/terraform-aws-audit-root'):
        os.symlink(os.path.abspath("modules/terraform-aws-audit-root"), os.path.abspath("./bubbletea/infra-bubbletea-root/terraform-aws-audit-root"))
    if not os.path.exists('./bubbletea/infra-bubbletea-root/terraform-aws-backend'):
        os.symlink(os.path.abspath("modules/terraform-aws-backend"), os.path.abspath("./bubbletea/infra-bubbletea-root/terraform-aws-backend"))
    if not os.path.exists('./bubbletea/infra-bubbletea-root/terraform-aws-billing-role'):
        os.symlink(os.path.abspath("modules/terraform-aws-billing-role"), os.path.abspath("./bubbletea/infra-bubbletea-root/terraform-aws-billing-role"))
    if not os.path.exists('./bubbletea/infra-bubbletea-root/terraform-aws-idp-gsuite'):
        os.symlink(os.path.abspath("modules/terraform-aws-idp-gsuite"), os.path.abspath("./bubbletea/infra-bubbletea-root/terraform-aws-idp-gsuite"))
    if not os.path.exists('./bubbletea/infra-bubbletea-root/terraform-aws-organization'):
        os.symlink(os.path.abspath("modules/terraform-aws-organization"), os.path.abspath("./bubbletea/infra-bubbletea-root/terraform-aws-organization"))

if __name__ == '__main__':
    clone_repositories()