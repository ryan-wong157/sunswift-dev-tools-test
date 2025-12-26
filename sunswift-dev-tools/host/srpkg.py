#!/usr/bin/env python3

###############################################################################
# Sunswift High Level DDS Package generator
# Version: V0.1
# Date: 24/12/2025
# Author: Ryan Wong
#
# Creates a new package according to this structure in the directory which you
# run this script from
# 
# <package_name>/
#     build/
#     src/
#     include/
#     config/
#     launch/
#     CMakelists.txt
#     README.md
#
# build -> for CMakelists.txt to put artifacts and final binary
# src -> all your .cpp files
# include -> all your .hpp files
# config -> json files (probably) for node configs + params + choice of launch file
# launch -> containing one or more launch files
# 
# Usage in directory you want to create pkg in:
#   
###############################################################################

import argparse
import sys
import re
import shutil
import json
from datetime import datetime
from pathlib import Path

CWD = Path.cwd()
# THIS ASSUMES THAT node_registry.json is 2 directories above this script and in the repo root...
REPO_ROOT = Path(__file__).resolve().parents[2]
NODE_REG_PATH = REPO_ROOT / "node_registry.json"


### HELPERS =====================================================================================

def die(msg: str) -> None:
    print(msg)
    sys.exit(1)

def fill_readme(path: Path) -> bool:
    pass

def fill_cmakelists(path: Path) -> bool:
    pass

def fill_launch(path: Path) -> bool:
    pass

def fill_config(path: Path) -> bool:
    pass


### CORE LOGIC ==================================================================================

def pkg_create(pkg_name: str) -> None:
    """Creates directory based on structure in top comment if it doesn't already exist.
    Also registers it to node_registry.json.
    
    Args:
        pkg_name (str): pkg_name passed in from CL args
    """
    abs_pkg_path = CWD / pkg_name
    nested_dirs = ["build", "src", "include", "config", "launch"]
    files = ["CMakelists.txt", "README.md"]
    
    # Check if package already exists in cwd
    if abs_pkg_path.exists() and abs_pkg_path.is_dir():
        die(f"Package {pkg_name} already exists at {abs_pkg_path.relative_to(REPO_ROOT)}")

    # Check if it already exists in node_registry.json somewhere else
    data = json.loads(NODE_REG_PATH.read_text())
    found_pkg = next((node for node in data["nodes"] if node["name"] == pkg_name), None)
    if found_pkg:
        die(f"Package: {pkg_name} already exists at '{found_pkg["path"]}'")
        
    # Create directories and files    
    for dir in nested_dirs:
        (abs_pkg_path / dir).mkdir(parents=True)
    for file in files:
        (abs_pkg_path / file).touch()
        
    # TODO: Populate CMakeLists.txt, README.md and create launch and config templates

    # TODO: Refactor this to a function?
    new_entry = {
        "name": pkg_name,
        "type": "rti_dds",
        "path": str(abs_pkg_path.relative_to(REPO_ROOT)),
        "target": "qnx"
    }
    data["nodes"].append(new_entry)
    
    try:
        NODE_REG_PATH.write_text(
                json.dumps(data, indent=2, sort_keys=True) + "\n"
            )
    except IOError as e:
        print(f"An error has occuredL {e}")

    print("Package: create success")
    print(f"Package: '{pkg_name}' created at '{abs_pkg_path.relative_to(REPO_ROOT)}'")
    print(f"Package: registered in node_registry")


def pkg_delete(pkg_name: str) -> None:
    """Deletes directory with pkg_name if it's in the cwd, and it's a Sunswift DDS pkg
    Also unregisters it from node_registry.json
     
    Args:
        pkg_name (str): pkg_name passed in from CL args
    """ 
    abs_pkg_path = CWD / pkg_name
    
    if not (abs_pkg_path.exists() and abs_pkg_path.is_dir()):
        die(f"Package with name: '{pkg_name}' not found in current directory")

    # TODO check if it is a valid Sunswift DDS package from node_registry
    
    stats = abs_pkg_path.stat()
    print(f"Found Sunswift DDS package: {pkg_name}")
    print(f"Package size (bytes): {stats.st_size}")
    print(f"Created: {datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")}")
    res = input(f"Do you really want to delete {pkg_name} (y/n): ")
    print("-----")
    if res.lower() == "y":
        shutil.rmtree(abs_pkg_path)
        print(f"Package: {pkg_name} deleted")
        print(f"Package: {pkg_name} removed from node registry")
    else:
        print("Stopping delete...")
        sys.exit(0)
         
                
    
### MAIN =======================================================================================
def main():
    ### Command line arguments
    parser = argparse.ArgumentParser(
            description="Sunswift DDS package management tool. \
            To create and delete packages, you must be in the same directory as the package"
        )
    group = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument("pkg_name", help="Name of package to be created/deleted")
    group.add_argument("-c", "--create", action="store_true", help="Create specified package")
    group.add_argument("-d", "--delete", action="store_true", help="Remove specified package")
    group.add_argument("-f", "--find", action="store_true", help="Find specified package")
    args = parser.parse_args()
    
    pkg_name = args.pkg_name
    
    ### Validate package name
    pattern = r"^[a-z0-9_]*$"
    if not re.match(pattern, pkg_name):
        die("Invalid package name: must be in 'snake_case'")
        
    ### TODO: SANITY CHECK -> check node_registry.json exists and is in correct path. 
    # check that script is run in repo
    # warn if not in src/
    
    ### Logic based on flags
    if args.create:
        pkg_create(pkg_name)
    elif args.delete:
        pkg_delete(pkg_name)


if __name__ == "__main__":
    main()