#!/usr/bin/env bash

set -eo pipefail

# Find and change to repo root directory
OS=$(uname)
if [[ "$OS" == "Darwin" ]]; then
	# OSX uses BSD readlink
	BASEDIR="$(dirname "$0")"
else
	BASEDIR=$(readlink -e "$(dirname "$0")")
fi
cd "${BASEDIR}/../.." || exit 1

(
cd monitoring || exit 1
make image
)

./monitoring/mock_uss/run_decea_test.sh up -d

monitoring/mock_uss/wait_for_mock_uss.sh mock_uss_ridsp
monitoring/mock_uss/wait_for_mock_uss.sh mock_uss_riddp
