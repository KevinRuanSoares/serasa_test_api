import base64
import hashlib
from django.core.files.base import ContentFile


def convert_base64_to_file(base64_string):
    """
    Converte uma string base64 em um objeto ContentFile e gera um nome de arquivo
    baseado em um hash do conteúdo da imagem.

    :param base64_string: String codificada em base64 representando uma imagem.
    :return: Um objeto ContentFile que representa a imagem.
    """
    format, imgstr = base64_string.split(';base64,')
    ext = format.split('/')[-1]
    data = base64.b64decode(imgstr)
    hash_object = hashlib.sha256(data)
    hex_dig = hash_object.hexdigest()
    file_name = f"{hex_dig}.{ext}"
    return ContentFile(data, name=file_name)
