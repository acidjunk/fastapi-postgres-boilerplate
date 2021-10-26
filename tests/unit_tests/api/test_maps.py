from http import HTTPStatus

from server.utils.json import json_dumps


def test_map_create_with_owner(test_client, user_token_headers):
    body = {"name": "CreatedMap", "description": "desc", "size_x": 10, "size_y": 10, "status": "new"}
    response = test_client.post(
        "/api/maps/",
        data=json_dumps(body),
        headers=user_token_headers,
    )
    assert HTTPStatus.NO_CONTENT == response.status_code


def test_map_create_not_authenticated(test_client):
    body = {"name": "CreatedMap", "description": "desc", "size_x": 10, "size_y": 10, "status": "new"}
    response = test_client.post(
        "/api/maps/",
        data=json_dumps(body),
    )
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_admin_map_create(test_client, superuser_token_headers):
    body = {
        "name": "CreatedMap",
        "description": "desc",
        "size_x": 10,
        "size_y": 10,
        "status": "new",
        "created_by": None,
    }
    response = test_client.post(
        "/api/maps/admin",
        data=json_dumps(body),
        headers=superuser_token_headers,
    )
    assert HTTPStatus.NO_CONTENT == response.status_code


def test_admin_map_create_with_normal_user(test_client, user_token_headers):
    body = {
        "name": "CreatedMap",
        "description": "desc",
        "size_x": 10,
        "size_y": 10,
        "status": "new",
        "created_by": None,
    }
    response = test_client.post(
        "/api/maps/admin",
        data=json_dumps(body),
        headers=user_token_headers,
    )
    assert HTTPStatus.FORBIDDEN == response.status_code


def test_map_update_with_owner(test_client, user_token_headers, map_1):
    body = {
        "name": "UpdatedMap",
        "description": "desc",
        "size_x": 10,
        "size_y": 10,
        "status": "new",
        "end_date": "2021-10-22T17:14:41.016Z",
    }

    response = test_client.put(
        f"/api/maps/{map_1}",
        data=json_dumps(body),
        headers=user_token_headers,
    )

    assert HTTPStatus.NO_CONTENT == response.status_code


def test_map_update_with_not_owner(test_client, superuser_token_headers, map_1):
    body = {
        "name": "UpdatedMap",
        "description": "desc",
        "size_x": 10,
        "size_y": 10,
        "status": "new",
        "end_date": "2021-10-22T17:14:41.016Z",
    }

    response = test_client.put(
        f"/api/maps/{map_1}",
        data=json_dumps(body),
        headers=superuser_token_headers,
    )
    assert HTTPStatus.FORBIDDEN == response.status_code


def test_admin_map_update(test_client, superuser_token_headers, map_1):
    body = {
        "name": "UpdatedMap",
        "description": "desc",
        "size_x": 10,
        "size_y": 10,
        "status": "new",
        "end_date": "2021-10-22T17:14:41.016Z",
        "created_by": None,
    }

    response = test_client.put(
        f"/api/maps/admin/{map_1}",
        data=json_dumps(body),
        headers=superuser_token_headers,
    )
    assert HTTPStatus.NO_CONTENT == response.status_code


def test_admin_map_update_with_not_admin(test_client, user_token_headers, map_1):
    body = {
        "name": "UpdatedMap",
        "description": "desc",
        "size_x": 10,
        "size_y": 10,
        "status": "new",
        "end_date": "2021-10-22T17:14:41.016Z",
        "created_by": None,
    }

    response = test_client.put(
        f"/api/maps/admin/{map_1}",
        data=json_dumps(body),
        headers=user_token_headers,
    )
    assert HTTPStatus.FORBIDDEN == response.status_code
