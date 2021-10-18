from server import crud


def test_filter(product_1, product_2):
    result, content_range = crud.product_crud.get_multi(filter_parameters=["name:duct 1"], sort_parameters=[])
    assert len(result) == 1
    assert content_range == "products 0-100/1"

    # Will not filter but return all results
    result, content_range = crud.product_crud.get_multi(filter_parameters=["NONEXISITANT:0"], sort_parameters=[])
    assert len(result) == 2
    assert content_range == "products 0-100/2"

    # Wild card match on all tables
    result, content_range = crud.product_crud.get_multi(filter_parameters=["Product 1"], sort_parameters=[])
    assert len(result) == 1
    assert content_range == "products 0-100/1"


def test_sort(product_1, product_2):
    result, content_range = crud.product_crud.get_multi(filter_parameters=[], sort_parameters=["name:ASC"])
    assert len(result) == 2
    assert content_range == "products 0-100/2"

    assert result[0].name == "Product 1"

    result, content_range = crud.product_crud.get_multi(filter_parameters=[], sort_parameters=["name:DESC"])
    assert len(result) == 2
    assert content_range == "products 0-100/2"

    assert result[0].name == "Product 2"

    # No Sort order
    result, content_range = crud.product_crud.get_multi(filter_parameters=[], sort_parameters=["name"])
    assert len(result) == 2
    assert content_range == "products 0-100/2"

    assert result[0].name == "Product 1"

    # Non existant column impossible to sort
    result, content_range = crud.product_crud.get_multi(filter_parameters=[], sort_parameters=["NONTRUE"])
    assert len(result) == 2
    assert content_range == "products 0-100/2"

    # Non existant column impossible to sort on nonexistant method
    result, content_range = crud.product_crud.get_multi(filter_parameters=[], sort_parameters=["NONTRUE:NONTRUE"])
    assert len(result) == 2
    assert content_range == "products 0-100/2"
