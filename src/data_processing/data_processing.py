import io
from io import BytesIO

import msoffcrypto


def decrypt_xlsx(path_file: str, password: str) -> BytesIO:
    file_descrypt = io.BytesIO()

    with open(path_file, 'rb') as f:
        excel_cripto = msoffcrypto.OfficeFile(f)
        excel_cripto.load_key(password=password)

        excel_cripto.decrypt(file_descrypt)

    return file_descrypt
