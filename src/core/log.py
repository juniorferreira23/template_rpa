import logging
from pathlib import Path

LOG_PATH = Path(__file__).parent.parent.parent / 'logs' / 'app.log'
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
)

logger = logging.getLogger(__name__)
