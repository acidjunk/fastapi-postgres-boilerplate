from http import HTTPStatus
from uuid import uuid4

import pytest

from server.db import ProductsTable
from server.utils.json import json_dumps


def test_products_get_multi(product_1, test_client):
    response = test_client.get("/api/products")

    assert HTTPStatus.OK == response.status_code
    products = response.json()

    assert 1 == len(products)


def test_product_by_id(product_1, test_client):
    response = test_client.get(f"/api/products/{product_1}")

    assert HTTPStatus.OK == response.status_code
    product = response.json()
    assert product["name"] == "Product 1"


def test_product_by_id_404(product_1, test_client):
    response = test_client.get(f"/api/products/{str(uuid4())}")
    assert HTTPStatus.NOT_FOUND == response.status_code


def test_product_create(test_client):
    p_id = uuid4()
    body = {
        "product_id": str(p_id),
        "name": "Product",
        "description": "Product description",
    }

    response = test_client.post(
        "/api/products/",
        data=json_dumps(body),
        headers={"Content_Type": "application/json"},
    )
    assert HTTPStatus.NO_CONTENT == response.status_code
    products = test_client.get("/api/products").json()
    assert 1 == len(products)


def test_product_delete(product_1, test_client):
    response = test_client.delete(f"/api/products/{product_1}")
    assert HTTPStatus.NO_CONTENT == response.status_code
    assert len(ProductsTable.query.all()) == 0
