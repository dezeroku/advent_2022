#!/usr/bin/env bash
set -euo pipefail

RUNDIR="$(readlink -f "$(dirname "$0")")"

pushd "${RUNDIR}"
docker build -t aoc-2022-7-fun .
popd

[ -z "${DATA_FILE:-}" ] && DATA_FILE="./data"
DATA_FILE="$(readlink -f "${DATA_FILE}")"

docker run -v "${DATA_FILE}":/data -it aoc-2022-7-fun
