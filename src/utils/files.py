import glob
import os
from pathlib import Path

from src.core.log import logger
from src.core.paths import PATH_TEMP


def get_last_file(path_folder: str = str(PATH_TEMP)):
    """Pega o gerado/modificado arquivo da pasta

    Args:
        path_folder (str, optional): caminho da pasta.
        Defaults to str(PATH_TEMP).

    Returns:
        str: caminho do arquivo
    """
    files = glob.glob(os.path.join(path_folder, '*'))
    if not files:
        return None
    logger.info(f'Pego o último arquivo em {path_folder}')
    return max(files, key=os.path.getmtime)


def delete_file(path_file: str):
    """deleta o arquivo do caminho passado

    Args:
        path_file (str): caminho do arquivo
    """
    file = Path(path_file)
    if file.exists():
        file.unlink()
        logger.info(f'File deleted successfully {path_file}.')
    else:
        logger.warning('The file does not exist.')
