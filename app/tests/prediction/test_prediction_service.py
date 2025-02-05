import numpy
import pytest

from app.services.prediction_service import prepare_input_tensor


def test_check_image_for_footprint_throws_exception_when_image_is_invalid(
        prediction_service,
        invalid_image_file
):
    with pytest.raises(Exception):
        prediction_service.check_image_for_footprint(invalid_image_file)

def test_classify_image_throws_exception_when_image_is_invalid(
        prediction_service,
        invalid_image_file
):
    with pytest.raises(Exception):
        prediction_service.classify_image(invalid_image_file)

def test_prepare_input_tensor_transforms_valid_image_to_a_vector_of_expected_shape(
        mocker,
        valid_image_file
):

    expected_shape_before_expansion = (100, 100, 3)
    expected_shape_after_expansion = (1, 100, 100, 3)

    spy_numpy_conversion = mocker.spy(numpy, "array")
    spy_numpy_expansion = mocker.spy(numpy, "expand_dims")

    prepare_input_tensor(valid_image_file)

    assert spy_numpy_conversion.spy_return.shape == expected_shape_before_expansion
    assert spy_numpy_conversion.call_count == 1
    assert spy_numpy_expansion.spy_return.shape == expected_shape_after_expansion
    assert spy_numpy_expansion.call_count == 1