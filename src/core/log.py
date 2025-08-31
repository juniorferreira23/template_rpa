import logging
from pathlib import Path

PATH_LOG = Path.cwd() / 'logs'
if not PATH_LOG.exists:
    PATH_LOG.parent.mkdir(parents=True, exist_ok=True)

FILE_LOG = PATH_LOG / 'app.log'
if not FILE_LOG.exists():
    FILE_LOG.touch()

logging.basicConfig(
    filename=str(FILE_LOG),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
)

logger = logging.getLogger(__name__)
