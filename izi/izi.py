#!/usr/bin/env python3

import git
import json
import os
import sys
import fileinput
import click
import shutil
import gitlab
import time

class bcolors:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

@click.group()
def cli():
    """A CLI to setup all environments you need to quick start contributing and developing for DNX"""

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)

input_file = open(resource_path('data.json'))
json_obj   = json.load(input_file)

bubbletea_array = json_obj['bubbletea']
tools_array     = json_obj['tools']
modules_array   = json_obj['modules']

GITLAB_BASE_URL          = 'git@gitlab.com:DNXLabs/'
GITHUB_BASE_URL          = 'git@github.com:DNXLabs/'
BUBBLETEA_REPOSITORY_URL = 'bubbletea/aws-platform/'
GIT                      = '.git'
COMMIT_MESSAGE           = 'Foundation'


@cli.command(help='Download the bubbletea stack, modules and tools.')
@click.argument('stack')
def get(stack: str):
    # Bubbletea clone action
    clone_stack('bubbletea')

    # Modules clone action
    clone_modules(stack)

    # Tools clone action
    clone_tools(stack)


@cli.command(help='Start a new project using the latest commit from all bubbletea stacks.')
@click.argument('project')
def init(project: str):
    setup_stack(project)


def clone_stack(project):
    if not os.path.exists(project):
        os.makedirs(project)

    for repository in bubbletea_array:
        if not os.path.exists('./'+ project + '/' + repository):
            git.Git('./' + project).clone(GITLAB_BASE_URL + BUBBLETEA_REPOSITORY_URL + repository + GIT)
            new_repository = repository.replace('bubbletea', project)
            os.rename('./' + project + '/' + repository, './' + project + '/' + new_repository)
            print('Cloned ' + repository)
        else:
            print('Skipping module' + repository + 'configuration, folder already exist')


def setup_stack(project):
    push_to_gitlab = input("Would you like to push the repositories to GitLab? [Y/n] ")

    if push_to_gitlab.lower() == 'y' or push_to_gitlab.lower() == 'yes' or push_to_gitlab == '':
        gitlab_group_id = input("What's the GitLab group ID? ")
        gitlab_private_token = input("What's the GitLab private token? ")

        gl = gitlab.Gitlab('https://gitlab.com/', private_token=gitlab_private_token)
        gl.auth()
        push_to_gitlab = True
    else:
        push_to_gitlab = False

    if not os.path.exists(project):
        os.makedirs(project)

    for repository in bubbletea_array:
        if not os.path.exists('./'+ project + '/' + repository.replace('bubbletea', project)):
            cloned_repo = git.Git('./' + project).clone(GITLAB_BASE_URL + BUBBLETEA_REPOSITORY_URL + repository + GIT)
            print('Cloned ' + repository)
            new_repository = repository.replace('bubbletea', project)
            
            shutil.rmtree('./'+ project + '/' + repository + '/.git')
            print('Removed .git on ' + repository)

            os.rename('./' + project + '/' + repository, './' + project + '/' + new_repository)
            print('Renamed ' + repository + ' to ' + new_repository)

            repo = git.Repo.init('./' + project + '/' + new_repository)
            print('Restarted .git repository on ' + new_repository)

            if push_to_gitlab:
                group = gl.groups.get(gitlab_group_id)
                gitlab_repo = gl.projects.create({'name': new_repository, 'namespace_id': gitlab_group_id})
                print('GitLab repository created')

                origin = repo.create_remote('origin', url=gitlab_repo.ssh_url_to_repo)
                repo.git.add(A=True)
                repo.index.commit(COMMIT_MESSAGE)
                local_branch  = 'master'
                remote_branch = 'master'
                origin.push(refspec='{}:{}'.format(local_branch, remote_branch))
                print('Pushed code to repository')
        
        else:
            print('Skipping module ' + repository + ' configuration, folder already exist')

def clone_modules(project):
    if not os.path.exists('modules'):
        os.makedirs('modules')

    for repository in modules_array:
        tags_array = repository['tags']
        for tag in tags_array:
            if tag == project:
                if not os.path.exists('./modules/' + repository['name']):
                    git.Git('./modules').clone(GITHUB_BASE_URL + repository['name'] + GIT)
                    print('Cloned ' + repository['name'])
                else:
                    print('Skipping module' + repository['name'] + 'configuration, folder already exist')
                break


def clone_tools(project):
    if not os.path.exists('tools'):
        os.makedirs('tools')

    for repository in tools_array:
        if not os.path.exists('./tools/' + repository):
            git.Git('./tools').clone(GITHUB_BASE_URL + repository + GIT)
            print('Cloned ' + repository)
        else:
            print('Skipping module' + repository + 'configuration, folder already exist')


@cli.command(help='Create symbolic link between modules and the stack you pass as parameter.')
@click.argument('project')
def link(project: str):
    # Link project with modules
    link_infra_app_platform(project)
    link_infra_domain(project)
    link_infra_mgmt_services(project)
    link_infra_network(project)
    link_infra_network_peering(project)
    link_infra_openvpn(project)
    link_infra_root(project)


@cli.command(help='Delete symbolic link if exists between modules and the stack you pass as parameter.')
@click.argument('project')
def unlink(project: str):
    # Link project with modules
    unlink_infra_app_platform(project)
    unlink_infra_domain(project)
    unlink_infra_mgmt_services(project)
    unlink_infra_network(project)
    unlink_infra_network_peering(project)
    unlink_infra_openvpn(project)
    unlink_infra_root(project)


def link_infra_app_platform(project):
    print('Checking infra-'+ project + '-app-platform links')

    app_plataform_path = './' + project + '/infra-' + project + '-app-platform/'

    if not os.path.exists(app_plataform_path + 'terraform-aws-db-monitoring'):
        print('Linking terraform-aws-db-monitoring')
        os.symlink(os.path.abspath('modules/terraform-aws-db-monitoring'), os.path.abspath(app_plataform_path + 'terraform-aws-db-monitoring'))
    if not os.path.exists(app_plataform_path + 'terraform-aws-ecs'):
        print('Linking terraform-aws-ecs')
        os.symlink(os.path.abspath('modules/terraform-aws-ecs'), os.path.abspath(app_plataform_path + 'terraform-aws-ecs'))
    if not os.path.exists(app_plataform_path + 'terraform-aws-ecs-app'):
        print('Linking terraform-aws-ecs-app')
        os.symlink(os.path.abspath('modules/terraform-aws-ecs-app'), os.path.abspath(app_plataform_path + 'terraform-aws-ecs-app'))
    if not os.path.exists(app_plataform_path + 'terraform-aws-ecs-app-front'):
        print('Linking terraform-aws-ecs-app-front')
        os.symlink(os.path.abspath('modules/terraform-aws-ecs-app-front'), os.path.abspath(app_plataform_path + 'terraform-aws-ecs-app-front'))
    if not os.path.exists(app_plataform_path + 'terraform-aws-static-app'):
        print('Linking terraform-aws-static-app')
        os.symlink(os.path.abspath('modules/terraform-aws-static-app'), os.path.abspath(app_plataform_path + 'terraform-aws-static-app'))


def link_infra_domain(project):
    print('Checking infra-' + project + '-domain link')

    domain_path = './' + project + '/infra-' + project + '-domain/'

    if not os.path.exists(domain_path + 'terraform-aws-hostedzone'):
        print('Linking terraform-aws-hostedzone')
        os.symlink(os.path.abspath('modules/terraform-aws-hostedzone'), os.path.abspath(domain_path + 'terraform-aws-hostedzone'))


def link_infra_mgmt_services(project):
    print('Checking infra-' + project + '-mgmt-services link')

    mgmt_services = './' + project + '/infra-' + project + '-mgmt-services/'

    if not os.path.exists(mgmt_services + 'terraform-aws-ecr'):
        print('Linking terraform-aws-ecr')
        os.symlink(os.path.abspath('modules/terraform-aws-ecr'), os.path.abspath(mgmt_services + 'terraform-aws-ecr'))
    if not os.path.exists(mgmt_services + 'terraform-aws-gitlab-runner'):
        print('Linking terraform-aws-gitlab-runner')
        os.symlink(os.path.abspath('modules/terraform-aws-gitlab-runner'), os.path.abspath(mgmt_services + 'terraform-aws-gitlab-runner'))


def link_infra_network(project):
    print('Checking infra-' + project + '-network link')

    network_path = './' + project + '/infra-' + project + '-network/'

    if not os.path.exists(network_path + 'terraform-aws-ecs'):
        print('Linking terraform-aws-ecs')
        os.symlink(os.path.abspath('modules/terraform-aws-ecs'), os.path.abspath(network_path + 'terraform-aws-ecs'))
    if not os.path.exists(network_path + 'terraform-aws-ecs-app'):
        print('Linking terraform-aws-ecs-app')
        os.symlink(os.path.abspath('modules/terraform-aws-ecs-app'), os.path.abspath(network_path + 'terraform-aws-ecs-app'))
    if not os.path.exists(network_path + 'terraform-aws-network'):
        print('Linking terraform-aws-network')
        os.symlink(os.path.abspath('modules/terraform-aws-network'), os.path.abspath(network_path + 'terraform-aws-network'))


def link_infra_network_peering(project):
    print('Checking infra-' + project + '-' + project + '-network-peering link')

    network_peering_path = './' + project + '/infra-' + project + '-network-peering/'

    if not os.path.exists(network_peering_path + 'terraform-aws-vpc-peering'):
        print('Linking terraform-aws-vpc-peering')
        os.symlink(os.path.abspath('modules/terraform-aws-vpc-peering'), os.path.abspath(network_peering_path + 'terraform-aws-vpc-peering'))


def link_infra_openvpn(project):
    print('Checking infra-'+ project + '-openvpn link')

    openvpn_path = './' + project + '/infra-' + project + '-openvpn/'

    if not os.path.exists(openvpn_path + 'terraform-aws-ecs'):
        print('Linking terraform-aws-ecs')
        os.symlink(os.path.abspath('modules/terraform-aws-ecs'), os.path.abspath(openvpn_path + 'terraform-aws-ecs'))
    if not os.path.exists(openvpn_path + 'terraform-aws-openvpn'):
        print('Linking terraform-aws-openvpn')
        os.symlink(os.path.abspath('modules/terraform-aws-openvpn'), os.path.abspath(openvpn_path + 'terraform-aws-openvpn'))


def link_infra_root(project):
    print('Checking infra-' + project + '-root link')

    root_path = './' + project + '/infra-' + project + '-root/'

    if not os.path.exists(root_path + 'terraform-aws-account'):
        print('Linking terraform-aws-account')
        os.symlink(os.path.abspath('modules/terraform-aws-account'), os.path.abspath(root_path + 'terraform-aws-account'))
    if not os.path.exists(root_path + 'terraform-aws-account-security'):
        print('Linking terraform-aws-account-security')
        os.symlink(os.path.abspath('modules/terraform-aws-account-security'), os.path.abspath(root_path + 'terraform-aws-account-security'))
    if not os.path.exists(root_path + 'terraform-aws-audit'):
        print('Linking terraform-aws-audit')
        os.symlink(os.path.abspath('modules/terraform-aws-audit'), os.path.abspath(root_path + 'terraform-aws-audit'))
    if not os.path.exists(root_path + 'terraform-aws-audit-member'):
        print('Linking terraform-aws-audit-member')
        os.symlink(os.path.abspath('modules/terraform-aws-audit-member'), os.path.abspath(root_path + 'terraform-aws-audit-member'))
    if not os.path.exists(root_path + 'terraform-aws-audit-root'):
        print('Linking terraform-aws-audit-root')
        os.symlink(os.path.abspath('modules/terraform-aws-audit-root'), os.path.abspath(root_path + 'terraform-aws-audit-root'))
    if not os.path.exists(root_path + 'terraform-aws-backend'):
        print('Linking terraform-aws-backend')
        os.symlink(os.path.abspath('modules/terraform-aws-backend'), os.path.abspath(root_path + 'terraform-aws-backend'))
    if not os.path.exists(root_path + 'terraform-aws-billing-role'):
        print('Linking terraform-aws-billing-role')
        os.symlink(os.path.abspath('modules/terraform-aws-billing-role'), os.path.abspath(root_path + 'terraform-aws-billing-role'))
    if not os.path.exists(root_path + 'terraform-aws-idp-gsuite'):
        print('Linking terraform-aws-idp-gsuite')
        os.symlink(os.path.abspath('modules/terraform-aws-idp-gsuite'), os.path.abspath(root_path + 'terraform-aws-idp-gsuite'))
    if not os.path.exists(root_path + 'terraform-aws-organization'):
        print('Linking terraform-aws-organization')
        os.symlink(os.path.abspath('modules/terraform-aws-organization'), os.path.abspath(root_path + 'terraform-aws-organization'))


def unlink_infra_app_platform(project):
    print('Checking infra-'+ project + '-app-platform links')

    app_plataform_path = './' + project + '/infra-' + project + '-app-platform/'

    if os.path.exists(app_plataform_path + 'terraform-aws-db-monitoring'):
        print('Unlinking terraform-aws-db-monitoring')
        os.unlink(os.path.abspath(app_plataform_path + 'terraform-aws-db-monitoring'))
    if os.path.exists(app_plataform_path + 'terraform-aws-ecs'):
        print('Unlinking terraform-aws-ecs')
        os.unlink(os.path.abspath(app_plataform_path + 'terraform-aws-ecs'))
    if os.path.exists(app_plataform_path + 'terraform-aws-ecs-app'):
        print('Unlinking terraform-aws-ecs-app')
        os.unlink(os.path.abspath(app_plataform_path + 'terraform-aws-ecs-app'))
    if os.path.exists(app_plataform_path + 'terraform-aws-ecs-app-front'):
        print('Unlinking terraform-aws-ecs-app-front')
        os.unlink(os.path.abspath(app_plataform_path + 'terraform-aws-ecs-app-front'))
    if os.path.exists(app_plataform_path + 'terraform-aws-static-app'):
        print('Unlinking terraform-aws-ecs-app-front')
        os.unlink(os.path.abspath(app_plataform_path + 'terraform-aws-static-app'))


def unlink_infra_domain(project):
    print('Checking infra-' + project + '-domain link')

    domain_path = './' + project + '/infra-' + project + '-domain/'

    if os.path.exists(domain_path + 'terraform-aws-hostedzone'):
        print('Unlinking terraform-aws-hostedzone')
        os.unlink(os.path.abspath(domain_path + 'terraform-aws-hostedzone'))


def unlink_infra_mgmt_services(project):
    print('Checking infra-' + project + '-mgmt-services link')

    mgmt_services_path = './' + project + '/infra-' + project + '-mgmt-services/'

    if os.path.exists(mgmt_services_path + 'terraform-aws-ecr'):
        print('Unlinking terraform-aws-ecr')
        os.unlink(os.path.abspath(mgmt_services_path + 'terraform-aws-ecr'))
    if os.path.exists(mgmt_services_path + 'terraform-aws-gitlab-runner'):
        print('Unlinking terraform-aws-gitlab-runner')
        os.unlink(os.path.abspath(mgmt_services_path + 'terraform-aws-gitlab-runner'))


def unlink_infra_network(project):
    print('Checking infra-' + project + '-network link')

    network_path = './' + project + '/infra-' + project + '-network/'

    if os.path.exists(network_path + 'terraform-aws-ecs'):
        print('Unlinking terraform-aws-ecs')
        os.unlink(os.path.abspath(network_path + 'terraform-aws-ecs'))
    if os.path.exists(network_path + 'terraform-aws-ecs-app'):
        print('Unlinking terraform-aws-ecs')
        os.unlink(os.path.abspath(network_path + 'terraform-aws-ecs-app'))
    if os.path.exists(network_path + 'terraform-aws-network'):
        print('Unlinking terraform-aws-network')
        os.unlink(os.path.abspath(network_path + 'terraform-aws-network'))


def unlink_infra_network_peering(project):
    print('Checking infra-' + project + '-' + project + '-network-peering link')

    network_peering_path = './' + project + '/infra-' + project + '-network-peering/'

    if os.path.exists(network_peering_path + 'terraform-aws-vpc-peering'):
        print('Unlinking terraform-aws-vpc-peering')
        os.unlink(os.path.abspath(network_peering_path + 'terraform-aws-vpc-peering'))


def unlink_infra_openvpn(project):
    print('Checking infra-'+ project + '-openvpn link')

    openvpn_path = './' + project + '/infra-' + project + '-openvpn/'

    if os.path.exists(openvpn_path + 'terraform-aws-ecs'):
        print('Unlinking terraform-aws-ecs')
        os.unlink(os.path.abspath(openvpn_path + 'terraform-aws-ecs'))
    if os.path.exists(openvpn_path + 'terraform-aws-openvpn'):
        print('Unlinking terraform-aws-ecs')
        os.unlink(os.path.abspath(openvpn_path + 'terraform-aws-openvpn'))


def unlink_infra_root(project):
    print('Checking infra-' + project + '-root link')

    root_path = './' + project + '/infra-' + project + '-root/'

    if os.path.exists(root_path + 'terraform-aws-account'):
        print('Unlinking terraform-aws-account')
        os.unlink(os.path.abspath(root_path + 'terraform-aws-account'))
    if os.path.exists(root_path + 'terraform-aws-account-security'):
        print('Unlinking terraform-aws-account-security')
        os.unlink(os.path.abspath(root_path + 'terraform-aws-account-security'))
    if os.path.exists(root_path + 'terraform-aws-audit'):
        print('Unlinking terraform-aws-audit')
        os.unlink(os.path.abspath(root_path + 'terraform-aws-audit'))
    if os.path.exists(root_path + 'terraform-aws-audit-member'):
        print('Unlinking terraform-aws-audit-member')
        os.unlink(os.path.abspath(root_path + 'terraform-aws-audit-member'))
    if os.path.exists(root_path + 'terraform-aws-audit-root'):
        print('Unlinking terraform-aws-audit-root')
        os.unlink(os.path.abspath(root_path + 'terraform-aws-audit-root'))
    if os.path.exists(root_path + 'terraform-aws-backend'):
        print('Unlinking terraform-aws-backend')
        os.unlink(os.path.abspath(root_path + 'terraform-aws-backend'))
    if os.path.exists(root_path + 'terraform-aws-billing-role'):
        print('Unlinking terraform-aws-billing-role')
        os.unlink(os.path.abspath(root_path + 'terraform-aws-billing-role'))
    if os.path.exists(root_path + 'terraform-aws-idp-gsuite'):
        print('Unlinking terraform-aws-idp-gsuite')
        os.unlink(os.path.abspath(root_path + 'terraform-aws-idp-gsuite'))
    if os.path.exists(root_path + 'terraform-aws-organization'):
        print('Unlinking terraform-aws-organization')
        os.unlink(os.path.abspath(root_path + 'terraform-aws-organization'))

@cli.command(help='Rewrite all modules sources to the local modules from the stack you pass as parameter.')
@click.argument('project')
def mount(project: str):
    for subdir, dirs, files in os.walk(project):
        for file in files:
            if file.endswith('.tf'):
                print(os.path.join(subdir, file))
                mount_file = open(os.path.abspath(os.path.join(subdir, '.mount-' + file)), 'wt')
                for line in open(os.path.abspath(os.path.join(subdir, file))):
                    replaced = False
                    for repository in modules_array:
                        if 'git::https://github.com/DNXLabs/' + repository['name'] in line:
                            mount_file.write('  source = "./' + repository['name'] + '"')
                            replaced = True
                            print(line)
                            break
                    if not replaced:
                        mount_file.write(line)
                os.remove(os.path.abspath(os.path.join(subdir, file)))
                os.rename(os.path.abspath(os.path.join(subdir, '.mount-' + file)), os.path.abspath(os.path.join(subdir, file)))

if __name__ == '__main__':
    cli()