import numpy as np
import pytest

from .main import CalculatorInputValidator, AverageColorCalculator

mocked_files = [([[[255, 0, 0]]], False),
                ([[[255, 0]]], True),
                ('image', True),
                (['image'], True),
                ([[[0.1]]], True)]

colors = [(np.array([[[255, 0, 0]]]), 'blue'),
          (np.array([[[0, 255, 0]]]), 'lime'),
          (np.array([[[0, 0, 255]]]), 'red'),
          (np.array([[[255, 255, 255]]]), 'white'),
          (np.array([[[255, 0, 255]]]), 'magenta'), ]


class TestCalculatorInputValidator:
    @pytest.mark.parametrize("input_image, is_error", mocked_files)
    def test_validate_input_file(self, input_image, is_error):
        if is_error:
            with pytest.raises(TypeError):
                CalculatorInputValidator.validate_image_input(input_image)
        else:
            assert CalculatorInputValidator.validate_image_input(input_image) == input_image


class TestAverageColorCalculator:
    @pytest.mark.parametrize("image_array, color", colors)
    def test_calculate_average_color(self, image_array, color):
        assert AverageColorCalculator(image_array).calculate_average_color() == color
