from pathlib import Path

PATH_TEMP = Path.cwd() / 'tmp'
if not PATH_TEMP.exists():
    PATH_TEMP.mkdir(parents=True, exist_ok=True)

PATH_DATA = Path.cwd() / 'data'
if not PATH_DATA.exists():
    PATH_DATA.mkdir(parents=True, exist_ok=True)
