#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys

import appdirs
import click
from termcolor import cprint, colored

PROGRAMS_FILE = os.path.join(
    appdirs.user_config_dir("engi", "PurpleMyst"), "programs.json"
)


def choose(programs):
    cprint(f"Choose a program to install", "blue")
    for i, program in enumerate(programs):
        cprint(f"{i + 1}. ", "yellow", end="")
        print(program["name"])

    while True:
        try:
            idx = int(input(colored("> ", "green")))
        except ValueError:
            cprint("Please enter a valid number.", "red")
            continue
        else:
            if not (0 < idx <= len(programs)):
                cprint(
                    f"Please enter a number between 1 and {len(programs)}."
                    "red"
                )
                continue

        return programs[idx - 1]


def repo_path(program):
    cache_dir = appdirs.user_cache_dir("engi", "PurpleMyst")
    return os.path.join(cache_dir, program["name"].lower())


def download(program):
    cprint(f"Checking ", "blue", end="")
    print(program["name"])

    repo = program["url"]

    path = repo_path(program)

    if os.path.exists(path):
        if os.path.exists(os.path.join(path, ".git")):
            proc = subprocess.run(["git", "-C", path, "pull"], stdout=subprocess.PIPE)
            if b"up to date" in proc.stdout.lower():
                print(program["name"], end="")
                cprint(" is up to date", "green")
                return False
        else:
            sys.exit(
                colored(
                    f"{path} already exists but is not a git repository.",
                    "red",
                )
            )

    cprint(f"Downloading ", "blue", end="")
    print(program["name"])
    proc = subprocess.run(["git", "clone", repo, path])
    proc.check_returncode()
    cprint("Downloaded ", "green", end="")
    print(program["name"])
    return True


def install(program):
    stow_dir = "/usr/local/stow/"
    package_name = program["name"].lower()

    cprint("Installing ", "blue", end="")
    print(program["name"])

    os.chdir(repo_path(program))
    for i, cmd in enumerate(program["commands"]):
        program["commands"][i] = \
            cmd.format(stow_dir=stow_dir, package_name=package_name)

    proc = subprocess.run(["sh", "-c", " && ".join(program["commands"])])

    if proc.returncode != 0:
        shutil.rmtree(repo_path(program))

    proc.check_returncode()

    cprint("Installed ", "green", end="")
    print(program["name"])


@click.group()
def cli():
    os.makedirs(os.path.dirname(PROGRAMS_FILE), exist_ok=True)
    if not os.path.exists(PROGRAMS_FILE):
        open(PROGRAMS_FILE, "w").write("[]")


@cli.command("install")
def cli_install():
    with open(PROGRAMS_FILE) as f:
        programs = json.load(f)

    cprint("Enter the name of the program.", "magenta")
    name = input(colored("> ", "green"))

    cprint("Enter the URL of the program.", "magenta")
    url = input(colored("> ", "green"))

    cprint(
        "Enter the commands you want to run to install the program, terminated by an empty line.",
        "magenta",
    )
    commands = []
    while True:
        cmd = input(colored("> ", "green"))
        if cmd:
            commands.append(cmd)
        else:
            break

    programs.append({"name": name, "url": url, "commands": commands})

    with open(PROGRAMS_FILE, "w") as f:
        json.dump(programs, f, indent=4)


@cli.command()
def upgrade():
    with open(PROGRAMS_FILE) as f:
        programs = json.load(f)

    for program in programs:
        if download(program):
            install(program)


if __name__ == "__main__":
    cli()
