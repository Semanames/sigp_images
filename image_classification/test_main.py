import pytest

from .main import ImageClassifierInputValidator

mocked_files = [({'image_name': 'name', 'image': [[[255, 0, 0]]], 'average_color': 'blue'}, False),
                ({'image_name': 'name', 'image': [[[255, 0, 0]]]}, True),
                ({'image_name': 'name', 'image': [[[255, 0, 0]]], 'average_color': 'totallyredblue'}, True)]


class TestCalculatorInputValidator:

    @pytest.mark.parametrize("input_dict, is_error", mocked_files)
    def test_validate_input_file(self, input_dict, is_error):
        if is_error:
            with pytest.raises(ValueError):
                ImageClassifierInputValidator.validate_calculation_output_data(input_dict)
        else:
            assert ImageClassifierInputValidator.validate_calculation_output_data(input_dict) == input_dict
