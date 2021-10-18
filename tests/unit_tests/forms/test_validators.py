import pytest
from pydantic import BaseModel, ValidationError

from server.forms.validators import unique_conlist


def test_constrained_list_good():
    class UniqueConListModel(BaseModel):
        v: unique_conlist(int, unique_items=True) = []

    m = UniqueConListModel(v=[1, 2, 3])
    assert m.v == [1, 2, 3]


def test_constrained_list_default():
    class UniqueConListModel(BaseModel):
        v: unique_conlist(int, unique_items=True) = []

    m = UniqueConListModel()
    assert m.v == []


def test_constrained_list_constraints():
    class UniqueConListModel(BaseModel):
        v: unique_conlist(int, min_items=1, unique_items=True)

    m = UniqueConListModel(v=list(range(7)))
    assert m.v == list(range(7))

    with pytest.raises(ValidationError) as exc_info:
        UniqueConListModel(v=[1, 1, 1])
    assert exc_info.value.errors() == [{"loc": ("v",), "msg": "Items must be unique", "type": "value_error"}]

    with pytest.raises(ValidationError) as exc_info:
        UniqueConListModel(v=1)
    assert exc_info.value.errors() == [{"loc": ("v",), "msg": "value is not a valid list", "type": "type_error.list"}]

    with pytest.raises(ValidationError) as exc_info:
        UniqueConListModel(v=[])
    assert exc_info.value.errors() == [
        {
            "loc": ("v",),
            "msg": "ensure this value has at least 1 items",
            "type": "value_error.list.min_items",
            "ctx": {"limit_value": 1},
        }
    ]
