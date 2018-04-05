import pytest
from _plotly_utils.basevalidators import CompoundArrayValidator
from plotly.graph_objs.layout import Image

# Fixtures
# --------
@pytest.fixture()
def validator():
    return CompoundArrayValidator('prop', 'layout',
                                  data_class_str='Image',
                                  data_docs='')


# Tests
# -----
def test_acceptance(validator: CompoundArrayValidator):
    val = [Image(opacity=0.5, sizex=120), Image(x=99)]
    res = validator.validate_coerce(val)

    assert isinstance(res, tuple)
    assert isinstance(res[0], Image)
    assert res[0].opacity == 0.5
    assert res[0].sizex == 120
    assert res[0].x is None

    assert isinstance(res[1], Image)
    assert res[1].opacity is None
    assert res[1].sizex is None
    assert res[1].x == 99


def test_acceptance_empty(validator: CompoundArrayValidator):
    val = [{}]
    res = validator.validate_coerce(val)

    assert isinstance(res, tuple)
    assert isinstance(res[0], Image)
    assert res[0].opacity is None
    assert res[0].sizex is None
    assert res[0].x is None


def test_acceptance_dict(validator: CompoundArrayValidator):
    val = [dict(opacity=0.5, sizex=120), dict(x=99)]
    res = validator.validate_coerce(val)

    assert isinstance(res, tuple)
    assert isinstance(res[0], Image)
    assert res[0].opacity == 0.5
    assert res[0].sizex == 120
    assert res[0].x is None

    assert isinstance(res[1], Image)
    assert res[1].opacity is None
    assert res[1].sizex is None
    assert res[1].x == 99


def test_rejection_type(validator: CompoundArrayValidator):
    val = 37

    with pytest.raises(ValueError) as validation_failure:
        validator.validate_coerce(val)

    assert "Invalid value" in str(validation_failure.value)


def test_rejection_element(validator: CompoundArrayValidator):
    val = ['a', 37]

    with pytest.raises(ValueError) as validation_failure:
        validator.validate_coerce(val)

    assert "Invalid element(s)" in str(validation_failure.value)


def test_rejection_value(validator: CompoundArrayValidator):
    val = [dict(opacity=0.5, sizex=120, bogus=100)]

    with pytest.raises(ValueError) as validation_failure:
        validator.validate_coerce(val)

    assert ("Invalid property specified for object of type "
            "plotly.graph_objs.layout.Image" in
            str(validation_failure.value))