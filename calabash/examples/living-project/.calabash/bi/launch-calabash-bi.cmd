@echo off
if "%PYTHON%"=="" (set PYTHON=python)
"%PYTHON%" "/mnt/data/calabash-2.2.0-candidate/calabash/scripts/run_calabash_bi_desktop.py" --project "/mnt/data/calabash-2.2.0-candidate/calabash/examples/living-project" %*
