$python = if ($env:PYTHON) { $env:PYTHON } else { 'python' }
& $python "/mnt/data/calabash-2.2.0-candidate/calabash/scripts/run_calabash_bi_desktop.py" --project "/mnt/data/calabash-2.2.0-candidate/calabash/examples/living-project" @args
exit $LASTEXITCODE
