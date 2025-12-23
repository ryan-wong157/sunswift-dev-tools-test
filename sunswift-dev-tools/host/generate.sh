#!/usr/bin/env bash
# This script generates RTI Connext DDS code from IDL files.

if [ $# -ne 1 ]; then
    echo "Usage: $0 <path_to_idl_file>"
    exit 1
fi

rtiddsgen -language c++11 -platform "$RTI_ARCHITECTURE" "$1"
