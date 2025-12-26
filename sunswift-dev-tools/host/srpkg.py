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
#     CMakeLists.txt
#     README.md
#
# build -> for CMakeLists.txt to put artifacts and final binary
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
from typing import Optional, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

CWD = Path.cwd()
# THIS ASSUMES THAT node_registry.json is 2 directories above this script and in the repo root...
REPO_ROOT = Path(__file__).resolve().parents[2]
NODE_REG_PATH = REPO_ROOT / "node_registry.json"

@dataclass
class PkgPaths:
    pkg_name: str
    abs_pkg_path: Path

### HELPERS =====================================================================================

def die(msg: str) -> None:
    print(msg)
    sys.exit(1)
    
def dir_size(paths: PkgPaths) -> int:
    path = paths.abs_pkg_path
    return sum(
        p.stat().st_size
        for p in path.rglob("*")
        if p.is_file()
    )

def fill_readme(path: Path) -> bool:
    pass

def fill_cmakelists(path: Path) -> bool:
    pass

def fill_launch(path: Path) -> bool:
    pass

def fill_config(path: Path) -> bool:
    pass

def pkg_exist_cwd(paths: PkgPaths) -> tuple[bool, Optional[str]]:
    """Checks if package exists in CWD
    Args:
        paths (PkgPaths): dataclass which stores name and abs path of pkg
    Returns:
        tuple[bool, Optional[str]]: (true/false, RELATIVE path of where it is/None)
    """
    if paths.abs_pkg_path.exists() and paths.abs_pkg_path.is_dir():
        rel = str(paths.abs_pkg_path.relative_to(REPO_ROOT))
        return (True, rel)

    return (False, None)
            
def pkg_exist_registry(paths: PkgPaths) -> tuple[bool, Optional[str]]:
    """Checks if package exists in registry
    Args:
        paths (PkgPaths): dataclass which stores name and abs path of pkg
    Returns:
        tuple[bool, Optional[str]]: (true/false, RELATIVE path of where it is/None)
    """
    try:
        data = json.loads(NODE_REG_PATH.read_text())
        found_pkg = next((node for node in data.get("nodes", []) if node.get("name") == paths.pkg_name), None)
        if found_pkg:
            return True, found_pkg.get("path")
    except (OSError, json.JSONDecodeError, FileNotFoundError) as e:
        die(f"Error reading registry: {e}")

    return (False, None)

def create_or_delete_entry(create: bool, paths: PkgPaths) -> bool:
    """Creates or deletes node_registry entry depending on a flag.
    ASSUMES ALL CHECKING HAS BEEN DONE BEFORE
    Args:
        create (bool): flag to create or del
        paths (PkgPaths): dataclass which stores name and abs path of pkg
    Returns:
        bool: if success or not
    """
    try:
        data = json.loads(NODE_REG_PATH.read_text())
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading node registry: {e}")
        return False

    if create:
        # Add entry
        new_entry = {
            "name": paths.pkg_name,
            "type": "rti_dds",
            "path": str(paths.abs_pkg_path.relative_to(REPO_ROOT)),
            "target": "qnx"
        }
        data["nodes"].append(new_entry)
    else:
        # Delete entry
        index = next((i for i, node in enumerate(data["nodes"]) if node["name"] == paths.pkg_name), None)
        if index is None:
            print("Package does not exist (failed previous checks...)")
            return False
        data["nodes"].pop(index)
    
    # TODO: ATOMIC Write to registry
    try:
        NODE_REG_PATH.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    except OSError as e:
        print(f"An error has occured: {e}")
        return False
    
    return True

def safe_rmdir(paths: PkgPaths) -> None:
    """Absolutely every error check again just to confirm before deletion. 
    In case any bugs in error checking happen before. Then deletes
    Args:
        paths (PkgPaths): dataclass which stores name and abs path of pkg
    """
    if not paths.abs_pkg_path.exists():
        die("Delete: Path does not exist")
        
    if not paths.abs_pkg_path.is_dir():
        die("Delete: Path is not a directory")
    
    try:
        # Check if path is within repository 
        paths.abs_pkg_path.relative_to(REPO_ROOT)
    except ValueError:
        die("Path not within SRP8-130_EMBD_High_Level repository")
    
    if paths.abs_pkg_path == REPO_ROOT or paths.abs_pkg_path == "/":
        die("wtf are u doing man")
        
    shutil.rmtree(paths.abs_pkg_path)

### CORE LOGIC ==================================================================================

def pkg_create(paths: PkgPaths) -> None:
    """Creates directory based on structure in top comment if it doesn't already exist.
    Also registers it to node_registry.json.
    
    Args:
        paths (PkgPaths): dataclass which stores name and abs path of pkg
    """
    nested_dirs = ["build", "src", "include", "config", "launch"]
    files = ["CMakeLists.txt", "README.md"]
    
    # Check if pkg already exists (assumes registry is correct)
    res1, location1 = pkg_exist_cwd(paths)
    res2, location2 = pkg_exist_registry(paths)
    if res1 or res2:
        location = location1 if location1 is not None else location2
        die(f"Package: {paths.pkg_name} already exists at '{location}'")

    # Create directories and files    
    for dir in nested_dirs:
        (paths.abs_pkg_path / dir).mkdir(parents=True)
    for file in files:
        (paths.abs_pkg_path / file).touch()
    
    ### EVERYTHING AFTER HERE NEEDS TO ROLLBACK THE DIRECTORY CREATION IF FAILS
    # TODO: Populate CMakeLists.txt, README.md and create launch and config templates

    # Create node_registry entry
    res = create_or_delete_entry(True, paths)
    if not res:
        die("Error creating node registry entry\nExiting...")

    print("Package: create success")
    print(f"Package: '{paths.pkg_name}' created at '{paths.abs_pkg_path.relative_to(REPO_ROOT)}'")
    print(f"Package: registered in node_registry")


def pkg_delete(paths: PkgPaths) -> None:
    """Deletes directory with PkgPaths.pkg_name if it's in the cwd, and it's a Sunswift DDS pkg
    Also unregisters it from node_registry.json
     
    Args:
        paths (PkgPaths): dataclass which stores name and abs path of pkg
    """     
    # Check if pkg exists
    res1, location1 = pkg_exist_cwd(paths)
    res2, location2 = pkg_exist_registry(paths)
    if not res1:
        die(f"Package: {paths.pkg_name} is not in current directory")
    if not res2:
        die(f"Package: {paths.pkg_name} is not in the node registry")
    
    stats = paths.abs_pkg_path.stat()
    print(f"Found Sunswift DDS package: {paths.pkg_name} at '{location1}'")
    print(f"Package size (bytes): {dir_size(paths)}")
    print(f"Created: {datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")}")
    res = input(f"Do you really want to delete {paths.pkg_name} (y/n): ")
    print("-----")
    if res.lower() == "y":
        safe_rmdir(paths)
        
        ### EVERYTHING AFTER HERE NEEDS TO ROLLBACK THE DIRECTORY DELETTION IF FAILS
        res = create_or_delete_entry(False, paths)
        if not res:
            die(f"Error deleting node from registry\nExiting...")
        print(f"Package: {paths.pkg_name} deleted")
        print(f"Package: {paths.pkg_name} removed from node registry")
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
    
    # Make paths objects
    abs_pkg_path = CWD / pkg_name
    paths = PkgPaths(pkg_name, abs_pkg_path)

    ### TODO: SANITY CHECK -> check node_registry.json exists and is in correct path. 
    # check that script is run in repo
    # warn if not in src/
    
    ### Logic based on flags
    if args.create:
        pkg_create(paths)
    elif args.delete:
        pkg_delete(paths)
    # TODO: find and mv flags

if __name__ == "__main__":
    main()