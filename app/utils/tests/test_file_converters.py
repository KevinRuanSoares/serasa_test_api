from django.test import TestCase
from django.core.files.base import ContentFile
from utils.file_converters import convert_base64_to_file


class ConvertBase64ToFileTestCase(TestCase):

    def test_convert_base64_to_file(self):
        base64_image = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA' \
                       'AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHx' \
                       'gljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='

        file = convert_base64_to_file(base64_image)
        self.assertIsInstance(file, ContentFile)
        self.assertTrue(file.name.endswith('.png'))
        self.assertTrue(file.read(), "O conteúdo do arquivo está vazio")
