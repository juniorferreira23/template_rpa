import io
from io import BytesIO

import msoffcrypto

from src.core.log import logger


def decrypt_xlsx(path_file: str, password: str) -> BytesIO | None:
    """Ler arquivos xlsx com senhas

    Args:
        path_file (str): caminho do arquivo
        password (str): senha do arquivo

    Returns:
        BytesIO: arquivo em memória
    """
    try:
        file_descrypt = io.BytesIO()

        with open(path_file, 'rb') as f:
            excel_cripto = msoffcrypto.OfficeFile(f)
            excel_cripto.load_key(password=password)

            excel_cripto.decrypt(file_descrypt)

        return file_descrypt

    except Exception as err:
        logger.error(f'Error trying to decrypt xlsx: {err}')
        raise err
