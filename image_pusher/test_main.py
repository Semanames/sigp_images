import pytest

from main import ImageReaderInputValidator

mocked_files = [('mocked_file.bmp', True), ('mocked_file.dib', True), ('mocked_file.jpg', True),
                ('mocked_file.jpe', True), ('mocked_file.jp2', True),
                ('mocked_file.png', True), ('mocked_file.webp', True), ('mocked_file.pbm', True),
                ('mocked_file.pgm', True), ('mocked_file.ppm', True),
                ('mocked_file.pxm', True), ('mocked_file.pnm', True), ('mocked_file.sr', True),
                ('mocked_file.ras', True), ('mocked_file.tiff', True),
                ('mocked_file.tif', True), ('mocked_file.exr', True), ('mocked_file.hdr', True),
                ('mocked_file.pic', True), ('mocked_file.pdf', False),
                ('mocked_file.txt', False), ('mocked_file.bla', False), ('mocked_file.exe', False),
                ('mocked_file.csv', False)]


class TestImageReaderInputValidator:
    @pytest.mark.parametrize("input_file, return_value", mocked_files)
    def test_validate_input_file(self, input_file, return_value):
        assert ImageReaderInputValidator.validate_input_file(input_file) == return_value

