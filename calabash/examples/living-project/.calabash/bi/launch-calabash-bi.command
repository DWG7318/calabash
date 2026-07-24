#!/usr/bin/env sh
cd "$(dirname "$0")"
exec "${PYTHON:-python3}" "/mnt/data/calabash-2.2.0-candidate/calabash/scripts/run_calabash_bi_desktop.py" --project "/mnt/data/calabash-2.2.0-candidate/calabash/examples/living-project" "$@"
