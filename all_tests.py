import subprocess

subprocess.run('poetry run pytest', shell=True)
subprocess.run('poetry run mypy bookkeeper', shell=True)
subprocess.run('poetry run pylint bookkeeper', shell=True)
subprocess.run('poetry run flake8 bookkeeper', shell=True)