#!/usr/bin/env bash
# Let's do it for the memes!
# Build the whole file system locally
# and run operations on it

# It takes around 40MB of space in my case
# Also it's terribly slow compared to proper solutions
# But it works!

set -euo pipefail

function starts_with() {
    local input="${1}"
    local pattern="${2}"
    echo "${input}" | grep -q "^${pattern}"
}

function calculate_dir_size() {
    # Calculate dir size by counting only the size of files in it (recursive)
    local dir_name="${1}"
    size=0
    while read -r filename; do
        file_size="$(du -b "${filename}" | cut -f1)"
        size=$(( size + file_size ))
    done <<< "$(find "${dir_name}" -type f)"

    echo "${size}"
}

function sanitize_input_data() {
    # Make sure that file ends with a newline
    # Otherwise while read logic will get mixed up
    local in_file="${1}"
    sed -i '$a\' "${in_file}"
}

function preprocess_data() {
    local in_file="${1}"
    local filesystem_root="${2}"

    while read -r line; do
        if starts_with "${line}" '\$' ; then
            local cmd="$(echo "${line}" | cut -f2 -d" ")"
            if [[ "${cmd}" == "cd" ]]; then
                local arg="$(echo "${line}" | cut -f3 -d" ")"
                # TODO: consider switch-case
                if [[ "${arg}" == "/" ]]; then
                    echo "cd ${filesystem_root}"
                elif [[ "${arg}" == ".." ]]; then
                    echo "cd .."
                else
                    echo "mkdir -p \"${arg}\" && cd \"${arg}\""
                fi
            else
                # We don't care about ls
                continue
            fi
        else
            if starts_with "${line}" 'dir'; then
               echo "mkdir -p \"$(echo "${line}" | cut -f2 -d" ")\""
            else
               local name="$(echo "${line}" | cut -f2 -d" ")"
               local size="$(echo "${line}" | cut -f1 -d" ")"
               echo "dd if=/dev/zero of=\"${name}\" bs=${size} count=1"
            fi
        fi
    done < "${in_file}"
}

function create_filesystem() {
    local data_preprocessed="${1}"
    bash "${data_preprocessed}" >/dev/null 2>&1
}

function first() {
    local filesystem_root="${1}"
    size=0
    while read -r dirname; do
        dir_size="$(calculate_dir_size "${dirname}")"
        if (( dir_size <= 100000 )); then
            size=$(( size + dir_size ))
        fi
    done <<< "$(find "${filesystem_root}" -type d)"

    echo "first: ${size}"
}

function second() {
    local filesystem_root="${1}"

    local total_disk_space=70000000
    local total_needed_disk_space=30000000
    local root_space_taken="$(calculate_dir_size "${filesystem_root}")"
    local available_disk_space=$(( total_disk_space - root_space_taken ))
    local needed_disk_space=$(( total_needed_disk_space - available_disk_space ))

    size_to_delete="${root_space_taken}"
    while read -r dirname; do
        dir_size="$(calculate_dir_size "${dirname}")"
        if (( dir_size >= needed_disk_space )); then
            if (( dir_size < size_to_delete )); then
                size_to_delete="${dir_size}"
            fi
        fi
    done <<< "$(find "${filesystem_root}" -type d)"

    echo "second: ${size_to_delete}"
}

function main() {
    [ -z "${DATA_FILE:-}" ] && DATA_FILE="./data"
    [ -z "${DATA_PREPROCESSED:-}" ] && DATA_PREPROCESSED="$(mktemp)"
    [ -z "${FILESYSTEM_ROOT:-}" ] && FILESYSTEM_ROOT="$(pwd)/filesystem"

    DATA_FILE="$(readlink -f "${DATA_FILE}")"
    DATA_PREPROCESSED="$(readlink -f "${DATA_PREPROCESSED}")"
    FILESYSTEM_ROOT="$(readlink -f "${FILESYSTEM_ROOT}")"

    # Do this so fix can be sanitized with newline properly
    local tmp_file="$(mktemp)"
    cp "${DATA_FILE}" "${tmp_file}"
    DATA_FILE="${tmp_file}"

    sanitize_input_data "${DATA_FILE}"
    preprocess_data "${DATA_FILE}" "${FILESYSTEM_ROOT}" > "${DATA_PREPROCESSED}"
    create_filesystem "${DATA_PREPROCESSED}"

    first "${FILESYSTEM_ROOT}"
    echo
    second "${FILESYSTEM_ROOT}"
}

# Detect if file is sourced or run
(return 0 2>/dev/null) || main
