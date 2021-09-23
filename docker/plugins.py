# Can only use stdlib as it will be run before `pip install`
import csv
import os
import subprocess
import sys
from argparse import ArgumentParser
from enum import Enum

INSTALL_PREREQUISITES = "install-prerequisites.sh"


class Method(str, Enum):
    DOWNLOAD = "download"
    DEPENDENCIES_BEFORE_VIPS = "dependencies_before_vips"
    DEPENDENCIES_BEFORE_PYTHON = "dependencies_before_python"
    INSTALL = "install"


def load_plugin_list(csv_content):
    if type(csv_content) is str:
        csv_content = csv_content.split("\n")
    plugins = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(csv_content, skipinitialspace=True)
    ]
    return plugins


def enabled_plugins(plugins):
    return [plugin for plugin in plugins if plugin['enabled'] != "0"]


def download_plugins(plugins, install_path):
    for plugin in plugins:
        print(f"Download {plugin['name']}")

        path = os.path.join(install_path, plugin['name'])
        command = f"git clone {plugin['git_url']} {path}"
        if plugin['git_branch']:
            command += f" && cd {path} && git checkout {plugin['git_branch']}"

        output = subprocess.run(command, shell=True, check=True)
        print(output.stdout)
        print(output.stderr)


def run_install_func_for_plugins(plugins, install_path, func):
    for plugin in plugins:
        print(f"Run {func} for {plugin['name']}")

        path = os.path.join(install_path, plugin['name'])
        command = f"bash {INSTALL_PREREQUISITES} {func}"
        output = subprocess.run(command, shell=True, check=True, cwd=path)
        print(output.stdout)
        print(output.stderr)


def install_python_plugins(plugins, install_path):
    for plugin in plugins:
        print(f"Install {plugin['name']}")

        path = os.path.join(install_path, plugin['name'])
        if os.path.exists(os.path.join(path, "requirements.txt")):
            command = f"pip install -r requirements.txt"
        else:
            command = f"pip install -e ."
        output = subprocess.run(command, shell=True, check=True, cwd=path)
        print(output.stdout)
        print(output.stderr)


if __name__ == '__main__':
    parser = ArgumentParser(prog="PIMS Plugins installer")
    parser.add_argument('--plugin_csv', help="Plugin list CSV content", nargs='*')
    parser.add_argument('--install_path', help="Plugin installation absolute path")
    parser.add_argument('--method', help="What method to apply",
                        choices=[
                            Method.DOWNLOAD,
                            Method.DEPENDENCIES_BEFORE_VIPS,
                            Method.DEPENDENCIES_BEFORE_PYTHON,
                            Method.INSTALL
                        ])
    params, other = parser.parse_known_args(sys.argv[1:])

    plugins = enabled_plugins(load_plugin_list(params.plugin_csv))

    os.makedirs(params.install_path, exist_ok=True)

    if params.method == Method.DOWNLOAD:
        download_plugins(plugins, params.install_path)
    elif params.method == Method.INSTALL:
        install_python_plugins(plugins, params.install_path)
    else:
        run_install_func_for_plugins(
            plugins, params.install_path, params.method
        )